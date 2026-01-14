from SPARQLWrapper import SPARQLWrapper, JSON
from config import ENDPOINT_URL, VALIDATION_REPORT_URI


def execute_sparql_query(query):
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        return sparql.query().convert()["results"]["bindings"]
    except Exception as e:
        print(f"SPARQL query error: {e}")
        return []


def get_constraints_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT ?component (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> ;
                 sh:sourceConstraintComponent ?component .
    }}
    GROUP BY ?component
    ORDER BY DESC(?count)
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        raw_component = row["component"]["value"]
        count = int(row["count"]["value"])

        name = raw_component.split("#")[-1] if "#" in raw_component else raw_component.split("/")[-1]

        display_name = name.replace("ConstraintComponent", "")

        data.append({
            "constraint": display_name,
            "fullUri": raw_component,
            "count": count
        })

    return data


def get_total_occurrences_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> .
    }}
    """
    results = execute_sparql_query(query)
    return int(results[0]["count"]["value"]) if results else 0


def get_most_violated_subject_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT ?focusNode (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> ;
                 sh:focusNode ?focusNode .
    }}
    GROUP BY ?focusNode
    ORDER BY DESC(?count)
    LIMIT 1
    """
    results = execute_sparql_query(query)
    if not results:
        return {"subject": "-", "count": 0}

    raw_subject = results[0]["focusNode"]["value"]
    count = int(results[0]["count"]["value"])

    display_subject = raw_subject.split("/")[-1] if "/" in raw_subject else raw_subject.split("#")[-1]

    return {"subject": display_subject, "fullUri": raw_subject, "count": count}


def get_unique_subjects_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT (COUNT(DISTINCT ?focusNode) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> ;
                 sh:focusNode ?focusNode .
    }}
    """
    results = execute_sparql_query(query)
    return int(results[0]["count"]["value"]) if results else 0


def get_triggered_constraints_count_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT (COUNT(DISTINCT ?component) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> ;
                 sh:sourceConstraintComponent ?component .
    }}
    """
    results = execute_sparql_query(query)
    return int(results[0]["count"]["value"]) if results else 0


def get_most_common_constraint_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT ?component (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> ;
                 sh:sourceConstraintComponent ?component .
    }}
    GROUP BY ?component
    ORDER BY DESC(?count)
    LIMIT 1
    """
    results = execute_sparql_query(query)
    if not results:
        return {"constraint": "-", "count": 0}

    raw_component = results[0]["component"]["value"]
    count = int(results[0]["count"]["value"])

    local_name = raw_component.split("#")[-1] if "#" in raw_component else raw_component.split("/")[-1]

    display_name = local_name.replace("ConstraintComponent", "")

    return {"constraint": display_name, "count": count}


def get_top_violated_subjects(encoded_path, limit=5):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?subject (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:focusNode ?subject ;
                 sh:resultPath ?path .
      FILTER(STR(?path) = "{encoded_path}")
    }}
    GROUP BY ?subject
    ORDER BY DESC(?count)
    LIMIT {limit}
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        subject_iri = row["subject"]["value"]
        count = int(row["count"]["value"])

        display_subject = (
            subject_iri.split("#")[-1]
            if "#" in subject_iri
            else subject_iri.split("/")[-1]
        )

        data.append({
            "subject": display_subject,
            "count": count
        })

    return data


def get_top_violated_constraint_types(encoded_path, limit=5):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?constraintComponent (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:sourceConstraintComponent ?constraintComponent ;
                 sh:resultPath ?path .
      FILTER(STR(?path) = "{encoded_path}")
    }}
    GROUP BY ?constraintComponent
    ORDER BY DESC(?count)
    LIMIT {limit}
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        constraint_iri = row["constraintComponent"]["value"]
        count = int(row["count"]["value"])

        # Shorten for display (same style as paths/subjects)
        display_constraint = (
            constraint_iri.split("#")[-1]
            if "#" in constraint_iri
            else constraint_iri.split("/")[-1]
        )

        data.append({
            "constraint": display_constraint,
            "count": count
        })

    return data


def get_top_violation_types(encoded_path, limit=5):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?message (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultMessage ?message ;
                 sh:resultPath ?path .
      FILTER(STR(?path) = "{encoded_path}")
      # Optional: filter out empty or uninformative messages
      FILTER(BOUND(?message) && ?message != "")
    }}
    GROUP BY ?message
    ORDER BY DESC(?count)
    LIMIT {limit}
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        message = row["message"]["value"]
        count = int(row["count"]["value"])

        display_message = message.strip()
        if len(display_message) > 45:
            display_message = display_message[:42] + "..."

        data.append({
            "message": display_message,
            "count": count
        })

    return data


def get_triples_with_violations_for_path(path_uri):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT ?focusNode (GROUP_CONCAT(?message; separator=" | ") AS ?messages)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath <{path_uri}> ;
                 sh:focusNode ?focusNode .
      OPTIONAL {{ ?violation sh:resultMessage ?message }}
    }}
    GROUP BY ?focusNode
    ORDER BY ?focusNode
    LIMIT 100
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        focus = row["focusNode"]["value"]
        messages = row.get("messages", {}).get("value", "No message")
        display_subject = focus.split("/")[-1] if "/" in focus else focus.split("#")[-1]

        data.append({
            "subject": display_subject,
            "fullSubject": focus,
            "violations": [{"message": msg.strip()} for msg in messages.split("|") if msg.strip()]
        })

    return data
