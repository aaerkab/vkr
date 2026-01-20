from flask import Blueprint, jsonify, request
from backend.services import find_critical_vulnerabilities
from backend.models import Assessment, Object
from backend.database import db
from backend.services import classify_security_level

bp_analytics = Blueprint("analytics", __name__, url_prefix="/api/analytics")


@bp_analytics.get("/overview")
def overview():
    """Сводная аналитика по всем объектам.

    Возвращает данные, удобные для построения общего дашборда:
    - сколько объектов всего
    - распределение по уровням защищенности (по последней оценке)
    - средний интегральный показатель (по последним оценкам)
    - топ объектов с наименьшей защищенностью

    Примечание: если у объекта нет оценок, он попадает в категорию "нет данных".
    """

    limit = int(request.args.get("limit", 5))

    # Подзапрос: последняя дата оценки для каждого объекта
    latest = (
        db.session.query(
            Assessment.object_id.label("object_id"),
            db.func.max(Assessment.assessment_date).label("max_date"),
        )
        .group_by(Assessment.object_id)
        .subquery()
    )

    # Присоединяем последнюю оценку к объектам (LEFT JOIN, чтобы не потерять объекты без оценок)
    latest_assessments = (
        db.session.query(Object, Assessment)
        .outerjoin(latest, Object.object_id == latest.c.object_id)
        .outerjoin(
            Assessment,
            db.and_(
                Assessment.object_id == latest.c.object_id,
                Assessment.assessment_date == latest.c.max_date,
            ),
        )
        .all()
    )

    total_objects = len(latest_assessments)
    by_level = {"высокий": 0, "средний": 0, "низкий": 0, "нет данных": 0}
    latest_scores = []
    objects_rank = []

    for obj, assessment in latest_assessments:
        score = assessment.overall_score if assessment else None
        if score is None:
            level = "нет данных"
        else:
            level = classify_security_level(float(score))
            latest_scores.append(float(score))
            objects_rank.append((float(score), obj, assessment))

        by_level[level] = by_level.get(level, 0) + 1

    avg_latest_score = (sum(latest_scores) / len(latest_scores)) if latest_scores else None

    objects_rank.sort(key=lambda x: x[0])
    worst = objects_rank[: max(0, limit)]
    worst_objects = [
        {
            "object_id": obj.object_id,
            "object_name": obj.object_name,
            "object_type": obj.object_type,
            "location": obj.location,
            "owner_organization": obj.owner_organization,
            "latest_assessment_date": a.assessment_date.isoformat() if a else None,
            "overall_score": score,
            "security_level": classify_security_level(score),
        }
        for score, obj, a in worst
    ]

    return jsonify(
        {
            "total_objects": total_objects,
            "by_security_level": by_level,
            "avg_latest_score": avg_latest_score,
            "worst_objects": worst_objects,
        }
    )


@bp_analytics.get("/critical-vulnerabilities")
def critical_vulnerabilities():
    vulns = find_critical_vulnerabilities()
    data = [
        {
            "vulnerability_id": v.vulnerability_id,
            "name": v.vulnerability_name,
            "description": v.vulnerability_description,
            "affected_component": v.affected_component,
            "severity_level": v.severity_level,
        }
        for v in vulns
    ]
    return jsonify(data)


@bp_analytics.get("/integral-time-series/<int:object_id>")
def integral_time_series(object_id: int):
    """
    Ряд значений интегрального показателя по датам оценок
    (для графика временных рядов на фронтенде).
    """
    rows = (
        db.session.query(Assessment)
        .filter(Assessment.object_id == object_id)
        .order_by(Assessment.assessment_date.asc())
        .all()
    )
    data = [
        {
            "date": a.assessment_date.isoformat(),
            "overall_score": a.overall_score,
        }
        for a in rows
    ]
    return jsonify(data)
