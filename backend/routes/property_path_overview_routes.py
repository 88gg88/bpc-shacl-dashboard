from flask import Blueprint, jsonify, request

from functions.property_path_overview_service import (
    get_total_violations, get_total_violated_paths,
    get_most_violated_path, get_most_violated_constraint,
    get_top_violated_paths, get_path_type_distribution, get_top_violated_constraints,
    get_property_path_details)

property_path_overview_bp = Blueprint("property_path_overview", __name__, url_prefix="/api/property-path")


@property_path_overview_bp.route("/total-violations", methods=["GET"])
def total_violations():
    try:
        count = get_total_violations()
        return jsonify({"totalViolations": count})
    except Exception as e:
        print(f"Error in total-violations endpoint: {e}")
        return jsonify({"totalViolations": 0}), 400


@property_path_overview_bp.route("/violated-paths-count", methods=["GET"])
def violated_paths_count():
    try:
        count = get_total_violated_paths()
        return jsonify({"totalViolatedPaths": count})
    except Exception as e:
        print(f"Error in violated-paths-count endpoint: {e}")
        return jsonify({"totalViolatedPaths": 0}), 400


@property_path_overview_bp.route("/most-violated-path", methods=["GET"])
def most_violated_path():
    try:
        result = get_most_violated_path()
        return jsonify({
            "mostViolatedPath": result["path"],
            "violationCount": result["count"]
        })
    except Exception as e:
        print(f"Error in most-violated-path endpoint: {e}")
        return jsonify({
            "mostViolatedPath": "N/A",
            "violationCount": 0
        }), 400


@property_path_overview_bp.route("/most-violated-constraint", methods=["GET"])
def most_violated_constraint():
    try:
        result = get_most_violated_constraint()
        return jsonify({
            "mostViolatedConstraint": result["constraint"],
            "violationCount": result["count"]
        })
    except Exception as e:
        print(f"Error in most-violated-constraint endpoint: {e}")
        return jsonify({
            "mostViolatedConstraint": "N/A",
            "violationCount": 0
        }), 400


@property_path_overview_bp.route("/top-violated-paths", methods=["GET"])
def top_violated_paths():
    try:
        data = get_top_violated_paths(10)
        return jsonify({"topPaths": data})
    except Exception as e:
        print(f"Error in top-violated-paths endpoint: {e}")
        return jsonify({"topPaths": []}), 400


@property_path_overview_bp.route("/path-type-distribution", methods=["GET"])
def path_type_distribution():
    try:
        data = get_path_type_distribution()
        return jsonify({"pathTypes": data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"pathTypes": []}), 400


@property_path_overview_bp.route("/top-violated-constraints", methods=["GET"])
def top_violated_constraints():
    try:
        data = get_top_violated_constraints(10)
        return jsonify({"topConstraints": data})
    except Exception as e:
        print(f"Error in top-violated-constraints endpoint: {e}")
        return jsonify({"topConstraints": []}), 400


@property_path_overview_bp.route("/path-details", methods=["GET"])
def path_details():
    page = int(request.args.get("page", 1))
    page_size = int(request.args.get("page_size", 10))
    sort_by = request.args.get("sort_by", "violations")
    sort_order = request.args.get("sort_order", "desc")

    try:
        data = get_property_path_details(page, page_size, sort_by, sort_order)
        return jsonify(data)
    except Exception as e:
        print(f"Error in path-details: {e}")
        return jsonify({"items": [], "total": 0}), 500
