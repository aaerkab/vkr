from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models import Assessment, AssessmentScore
from backend.services import calculate_integral_score, classify_security_level

bp_assessments = Blueprint("assessments", __name__, url_prefix="/api/assessments")


@bp_assessments.post("/")
def create_assessment():
    payload = request.json or {}
    object_id = payload["object_id"]
    scores = payload.get("scores", [])

    assessment = Assessment(object_id=object_id)
    db.session.add(assessment)
    db.session.flush()

    for s in scores:
        score = AssessmentScore(
            assessment_id=assessment.assessment_id,
            criteria_id=s["criteria_id"],
            score_value=s["score_value"],
            notes=s.get("notes"),
        )
        db.session.add(score)

    db.session.commit()

    integral = calculate_integral_score(assessment.assessment_id)
    assessment.overall_score = integral
    db.session.commit()

    level = classify_security_level(integral)

    return jsonify(
        {
            "assessment_id": assessment.assessment_id,
            "overall_score": integral,
            "security_level": level,
        }
    ), 201
