from flask import Blueprint, jsonify, request

class_overview_bp = Blueprint("class_overview", __name__)


@class_overview_bp.route("/my-new-endpoint", methods=["GET"])
def example():
    param= request.args.get ("param", default="default_value")
    return jsonify({"message": f"You sent: {param}"})
