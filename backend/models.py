from datetime import datetime
from .database import db


class Object(db.Model):
    __tablename__ = "objects"

    object_id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(255), nullable=False)
    object_type = db.Column(db.String(100))
    location = db.Column(db.String(255))
    owner_organization = db.Column(db.String(255))
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)

    assessments = db.relationship("Assessment", backref="object", lazy=True)


class Criteria(db.Model):
    __tablename__ = "criteria"

    criteria_id = db.Column(db.Integer, primary_key=True)
    criteria_name = db.Column(db.String(255), nullable=False)
    criteria_category = db.Column(db.String(100))
    max_score = db.Column(db.Float, nullable=False, default=100.0)
    weight = db.Column(db.Float, nullable=False, default=1.0)
    description = db.Column(db.Text)


class Assessment(db.Model):
    __tablename__ = "assessments"

    assessment_id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("objects.object_id"), nullable=False)
    assessment_date = db.Column(db.DateTime, default=datetime.utcnow)
    assessor_id = db.Column(db.Integer, nullable=True)
    overall_score = db.Column(db.Float)

    scores = db.relationship("AssessmentScore", backref="assessment", lazy=True)


class AssessmentScore(db.Model):
    __tablename__ = "assessment_scores"

    score_id = db.Column(db.Integer, primary_key=True)
    assessment_id = db.Column(
        db.Integer, db.ForeignKey("assessments.assessment_id"), nullable=False
    )
    criteria_id = db.Column(
        db.Integer, db.ForeignKey("criteria.criteria_id"), nullable=False
    )
    score_value = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)


class Threat(db.Model):
    __tablename__ = "threats"

    threat_id = db.Column(db.Integer, primary_key=True)
    threat_name = db.Column(db.String(255), nullable=False)
    threat_description = db.Column(db.Text)
    threat_probability = db.Column(db.Float)
    threat_impact = db.Column(db.Float)


class Vulnerability(db.Model):
    __tablename__ = "vulnerabilities"

    vulnerability_id = db.Column(db.Integer, primary_key=True)
    vulnerability_name = db.Column(db.String(255), nullable=False)
    vulnerability_description = db.Column(db.Text)
    affected_component = db.Column(db.String(255))
    severity_level = db.Column(db.Float)


class Countermeasure(db.Model):
    __tablename__ = "countermeasures"

    measure_id = db.Column(db.Integer, primary_key=True)
    measure_name = db.Column(db.String(255), nullable=False)
    measure_type = db.Column(db.String(100))
    implementation_cost = db.Column(db.Float)
    effectiveness_level = db.Column(db.Float)
