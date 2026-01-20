from flask import Blueprint, request, jsonify
from backend.database import db
from backend.models import Object

bp_objects = Blueprint("objects", __name__, url_prefix="/api/objects")


@bp_objects.get("/")
def list_objects():
    objs = Object.query.all()
    data = [
        {
            "object_id": o.object_id,
            "object_name": o.object_name,
            "object_type": o.object_type,
            "location": o.location,
            "owner_organization": o.owner_organization,
            "creation_date": o.creation_date.isoformat(),
        }
        for o in objs
    ]
    return jsonify(data)


@bp_objects.post("/")
def create_object():
    payload = request.json or {}
    obj = Object(
        object_name=payload.get("object_name"),
        object_type=payload.get("object_type"),
        location=payload.get("location"),
        owner_organization=payload.get("owner_organization"),
    )
    db.session.add(obj)
    db.session.commit()
    return jsonify({"object_id": obj.object_id}), 201
