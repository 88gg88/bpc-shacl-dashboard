from flask import Blueprint, jsonify, request

property_path_overview_bp = Blueprint("property_path_overview", __name__)

# @my_new_page_bp.route("/my-new-endpoint", methods=["GET"])
# def example():
#  param = request.args.get("param", default="default_value")
# return jsonify({"message": f"You sent: {param}"})