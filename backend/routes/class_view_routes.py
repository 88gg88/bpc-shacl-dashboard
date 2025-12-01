from flask import Blueprint, jsonify, request

class_view_bp = Blueprint("class_view", __name__)

@class_view_bp.route("/my-new-endpoint", methods=["GET"])
def example():
    param = request.args.get("param", default="default_value")
    return jsonify({"message": f"You sent: {param}"})