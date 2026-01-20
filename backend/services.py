from typing import Sequence
from .models import AssessmentScore, Criteria, Vulnerability
from .database import db


def calculate_integral_score(assessment_id: int) -> float:
    """
    1) Получение оценок по критериям.
    2) Нормализация 0–100.
    3) Применение весов.
    4) Расчёт интегрального показателя.
    """
    rows = (
        db.session.query(AssessmentScore, Criteria)
        .join(Criteria, AssessmentScore.criteria_id == Criteria.criteria_id)
        .filter(AssessmentScore.assessment_id == assessment_id)
        .all()
    )

    if not rows:
        return 0.0

    weighted_sum = 0.0
    total_weight = 0.0

    for score, crit in rows:
        normalized = (score.score_value / crit.max_score) * 100.0
        weighted_sum += normalized * crit.weight
        total_weight += crit.weight

    if total_weight == 0:
        return 0.0

    return weighted_sum / total_weight


def classify_security_level(integral: float) -> str:
    """
    Пример шкалы:
    0–40  – низкий уровень,
    40–70 – средний,
    70–100 – высокий.
    """
    if integral < 40:
        return "низкий"
    if integral < 70:
        return "средний"
    return "высокий"


def find_critical_vulnerabilities(
    min_severity: float = 7.0,
) -> Sequence[Vulnerability]:
    """
    Критическими считаются уязвимости с уровнем severity >= min_severity.
    """
    return (
        db.session.query(Vulnerability)
        .filter(Vulnerability.severity_level >= min_severity)
        .order_by(Vulnerability.severity_level.desc())
        .all()
    )

