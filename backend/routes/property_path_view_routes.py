from flask import Blueprint, jsonify
from functions.property_path_view_service import (
    get_constraints_for_path,
    get_total_occurrences_for_path,
    get_unique_subjects_for_path, get_most_violated_subject_for_path,
    get_triggered_constraints_count_for_path, get_most_common_constraint_for_path,
    get_top_violated_subjects,
    get_top_violated_constraint_types,
    get_top_violation_types,
    get_triples_with_violations_for_path)

property_path_view_bp = Blueprint("property_path_view", __name__, url_prefix="/api/property-path-view")

@property_path_view_bp.route("/constraints/<path:path_uri>", methods=["GET"])
def constraints(path_uri):
    try:
        # The frontend sends raw URI with : replaced by _ for routing
        decoded_uri = path_uri.replace("_", ":")
        data = get_constraints_for_path(decoded_uri)
        return jsonify({"constraints": data})
    except Exception as e:
        print(f"Error in constraints endpoint: {e}")
        return jsonify({"constraints": []}), 400

@property_path_view_bp.route("/total-occurrences/<path:path_uri>", methods=["GET"])
def total_occurrences(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        count = get_total_occurrences_for_path(decoded_uri)
        return jsonify({"totalOccurrences": count})
    except Exception as e:
        print(f"Error in total-occurrences: {e}")
        return jsonify({"totalOccurrences": 0}), 400

"""@property_path_view_bp.route("/violating-triples-count/<path:path_uri>", methods=["GET"])
def violating_triples_count(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        count = get_violating_triples_count_for_path(decoded_uri)
        return jsonify({"violatingTriples": count})
    except Exception as e:
        print(f"Error in violating-triples-count: {e}")
        return jsonify({"violatingTriples": 0}), 400"""

@property_path_view_bp.route("/most-violated-subject/<path:path_uri>", methods=["GET"])
def most_violated_subject(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        result = get_most_violated_subject_for_path(decoded_uri)
        return jsonify(result)
    except Exception as e:
        print(f"Error in most-violated-subject: {e}")
        return jsonify({"subject": "—", "count": 0}), 400

@property_path_view_bp.route("/unique-subjects/<path:path_uri>", methods=["GET"])
def unique_subjects(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        count = get_unique_subjects_for_path(decoded_uri)
        return jsonify({"uniqueSubjects": count})
    except Exception as e:
        print(f"Error in unique-subjects: {e}")
        return jsonify({"uniqueSubjects": 0}), 400

@property_path_view_bp.route("/triggered-constraints-count/<path:path_uri>", methods=["GET"])
def triggered_constraints_count(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        count = get_triggered_constraints_count_for_path(decoded_uri)
        return jsonify({"triggeredConstraintsCount": count})
    except Exception as e:
        print(f"Error in triggered-constraints-count: {e}")
        return jsonify({"triggeredConstraintsCount": 0}), 400

@property_path_view_bp.route("/most-common-constraint/<path:path_uri>", methods=["GET"])
def most_common_constraint(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        result = get_most_common_constraint_for_path(decoded_uri)
        return jsonify(result)
    except Exception as e:
        print(f"Error in most-common-constraint: {e}")
        return jsonify({"constraint": "—", "count": 0}), 400

@property_path_view_bp.route("/top-violated-subjects/<path:path_uri>", methods=["GET"])
def top_violated_subjects(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        result = get_top_violated_subjects(decoded_uri, limit=5)
        return jsonify({"topSubjects": result})
    except Exception as e:
        print(f"Error in top-violated-subjects endpoint: {e}")
        return jsonify({"topSubjects": []}), 400

@property_path_view_bp.route("/top-violated-constraints/<path:path_uri>", methods=["GET"])
def top_violated_constraints(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        result = get_top_violated_constraint_types(decoded_uri, limit=5)
        return jsonify({"topConstraints": result})
    except Exception as e:
        print(f"Error in top-violated-constraints endpoint: {e}")
        return jsonify({"topConstraints": []}), 400

@property_path_view_bp.route("/top-violated-messages/<path:path_uri>", methods=["GET"])
def top_violated_messages(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        result = get_top_violation_types(decoded_uri, limit=5)
        return jsonify({"topMessages": result})
    except Exception as e:
        print(f"Error in top-violated-messages endpoint: {e}")
        return jsonify({"topMessages": []}), 400

@property_path_view_bp.route("/triples-with-violations/<path:path_uri>", methods=["GET"])
def triples_with_violations(path_uri):
    try:
        decoded_uri = path_uri.replace("_", ":")
        data = get_triples_with_violations_for_path(decoded_uri)
        return jsonify({"triples": data})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"triples": []}), 400