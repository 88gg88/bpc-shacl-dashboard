from flask import Blueprint, jsonify, request
from functions.class_view_service import (
    get_class_overview,
    get_class_details
)
class_view_bp = Blueprint("class_view", __name__, url_prefix="/api/class-view")


@class_view_bp.route("/overview", methods=["GET"])
def overview():
    return jsonify(get_class_overview())


@class_view_bp.route("/details", methods=["GET"])
def details():
    class_id = request.args.get("class")
    if not class_id:
        return jsonify({"error": "class parameter required"}), 400
    return jsonify(get_class_details(class_id))
