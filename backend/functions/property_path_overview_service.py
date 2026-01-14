from SPARQLWrapper import SPARQLWrapper, JSON
from config import ENDPOINT_URL, VALIDATION_REPORT_URI, SHAPES_GRAPH_URI


def execute_sparql_query(query):
    sparql = SPARQLWrapper(ENDPOINT_URL)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        return sparql.query().convert()["results"]["bindings"]
    except Exception as e:
        print(f"SPARQL query error: {e}")
        return []


def get_total_violations():
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath ?path .
    }}
    """
    results = execute_sparql_query(query)
    return int(results[0]["count"]["value"]) if results else 0


def get_total_violated_paths():
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT (COUNT(DISTINCT ?path) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath ?path .
    }}
    """
    results = execute_sparql_query(query)
    return int(results[0]["count"]["value"]) if results else 0


def get_most_violated_path():
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?path (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath ?path .
    }}
    GROUP BY ?path
    ORDER BY DESC(?count)
    LIMIT 1
    """
    results = execute_sparql_query(query)
    if not results:
        return {"path": "N/A", "count": 0}

    raw_path = results[0]["path"]["value"]
    count = int(results[0]["count"]["value"])

    if "#" in raw_path:
        pretty_path = raw_path.split("#")[-1]
    elif "/" in raw_path:
        pretty_path = raw_path.split("/")[-1]
    else:
        pretty_path = raw_path

    return {"path": pretty_path, "count": count}


def get_most_violated_constraint():
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?component (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:sourceConstraintComponent ?component .
    }}
    GROUP BY ?component
    ORDER BY DESC(?count)
    LIMIT 1
    """
    results = execute_sparql_query(query)
    if not results:
        return {"constraint": "N/A", "count": 0}

    raw_component = results[0]["component"]["value"]
    count = int(results[0]["count"]["value"])

    local_name = raw_component.split("#")[-1] if "#" in raw_component else raw_component.split("/")[-1]

    clean_name = local_name.replace("ConstraintComponent", "")

    return {"constraint": clean_name, "count": count}


def get_top_violated_paths(limit=10):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?path (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath ?path .
    }}
    GROUP BY ?path
    ORDER BY DESC(?count)
    LIMIT {limit}
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        raw_path = row["path"]["value"]
        count = int(row["count"]["value"])

        display_path = raw_path.split("#")[-1] if "#" in raw_path else raw_path.split("/")[-1]

        data.append({"path": display_path, "count": count})

    return data


def get_path_type_distribution():
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

    SELECT ?type (COUNT(?ps) AS ?count)
    FROM <{SHAPES_GRAPH_URI}>
    WHERE {{
      ?ps a sh:PropertyShape ;
          sh:path ?path .
      BIND(
        COALESCE(
          IF(isIRI(?path), "IRI",
          IF(EXISTS {{?path sh:inversePath ?x}}, "Inverse",
          IF(EXISTS {{?path sh:alternativePath ?x}}, "Alternative",
          IF(EXISTS {{?path sh:zeroOrMorePath ?x}}, "ZeroOrMore",
          IF(EXISTS {{?path sh:oneOrMorePath ?x}}, "OneOrMore",
          IF(EXISTS {{?path sh:zeroOrOnePath ?x}}, "ZeroOrOne",
          IF(EXISTS {{?path rdf:rest ?y}}, "Sequence", "Other"))))))),
          "IRI"
        ) AS ?type
      )
    }}
    GROUP BY ?type
    ORDER BY DESC(?count)
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        ptype = row["type"]["value"]
        count = int(row["count"]["value"])
        data.append({"type": ptype, "count": count})

    return data


def get_top_violated_constraints(limit=10):
    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?component (COUNT(?violation) AS ?count)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:sourceConstraintComponent ?component .
    }}
    GROUP BY ?component
    ORDER BY DESC(?count)
    LIMIT {limit}
    """
    results = execute_sparql_query(query)

    data = []
    for row in results:
        raw_component = row["component"]["value"]
        count = int(row["count"]["value"])

        name = raw_component.split("#")[-1] if "#" in raw_component else raw_component.split("/")[-1]

        display_name = name.replace("ConstraintComponent", "")

        data.append({"constraint": display_name, "count": count})

    return data


def get_property_path_details(page=1, page_size=10, sort_by="violations", sort_order="desc"):
    offset = (page - 1) * page_size

    order_dir = "DESC" if sort_order.lower() == "desc" else "ASC"

    query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>

    SELECT ?path (COUNT(?violation) AS ?violations)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath ?path .
    }}
    GROUP BY ?path
    ORDER BY {order_dir}(?violations)
    OFFSET {offset}
    LIMIT {page_size}
    """

    results = execute_sparql_query(query)

    data = []
    for row in results:
        raw_path = row["path"]["value"]
        violations = int(row["violations"]["value"])

        if raw_path == "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
            display_path = "rdf:type"
        else:
            display_path = raw_path.split("#")[-1] if "#" in raw_path else raw_path.split("/")[-1]

        data.append({
            "path": display_path,
            "rawPath": raw_path,
            "violations": violations
        })

    count_query = f"""
    PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT (COUNT(DISTINCT ?path) AS ?total)
    FROM <{VALIDATION_REPORT_URI}>
    WHERE {{
      ?violation a sh:ValidationResult ;
                 sh:resultPath ?path .
    }}
    """
    count_result = execute_sparql_query(count_query)
    total = int(count_result[0]["total"]["value"]) if count_result else 0

    return {"items": data, "total": total}
