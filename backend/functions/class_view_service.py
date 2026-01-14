from .virtuoso_service import run_sparql_query

SHAPES_GRAPH = "http://ex.org/ShapesGraph"
VALIDATION_GRAPH = "http://ex.org/ValidationReport"
def _get_last_part(iri: str) -> str:
    if not iri:
        return ""
    if "#" in iri:
        return iri.split("#")[-1]
    return iri.split("/")[-1]


def get_class_overview():
    query= f"""PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?class
           (COUNT(DISTINCT ?nodeShape) AS ?shapes)
           (COUNT(DISTINCT ?focusNode) AS ?instances)
           (COUNT(?v) AS ?violations)
    WHERE {{
      GRAPH <{SHAPES_GRAPH}> {{
        ?nodeShape sh:targetClass ?class ;
                   sh:property ?propertyShape .}}
      GRAPH <{VALIDATION_GRAPH}> {{?v a sh:ValidationResult ;
           sh:sourceShape ?propertyShape ;
           sh:focusNode ?focusNode ;
           sh:resultSeverity sh:Violation .}}}}    
    GROUP BY ?class
    ORDER BY DESC(?violations)"""
    results = run_sparql_query(query)
    classes = []
    total_violations = 0
    for row in results:
        cls = row["class"]["value"]
        shapes = int(row.get("shapes", {}).get("value", 0))
        instances = int(row.get("instances", {}).get("value", 0))
        violations = int(row.get("violations", {}).get("value", 0))
        total_violations += violations
        classes.append(

            {
                "class":cls,
                "instances":instances,
                "shapes":shapes,
                "violations":violations,
            }
        )
    total_classes = len(classes)
    avg_violations = total_violations / total_classes \
        if total_classes else 0
    return {
        "totalClasses":total_classes,
        "totalViolations": total_violations,
        "avgViolationsPerClass": round(avg_violations, 2),
        "mostViolatedClass": classes[0] ["class"] if classes else None,
        "classes": classes,
        "topInstances": sorted(classes, key=lambda x: x["instances"], reverse=True)[:5],
        "topViolations": sorted(classes, key=lambda x: x["violations"], reverse=True)[:5],
    }


def get_class_details(class_uri: str):
    query = f"""PREFIX sh: <http://www.w3.org/ns/shacl#>
    SELECT ?v ?focusNode ?path ?constraint ?message ?value
    WHERE {{
    
      GRAPH <{SHAPES_GRAPH}> {{
        ?nodeShape sh:targetClass <{class_uri}> ;
                   sh:property ?propertyShape .}}
      GRAPH <{VALIDATION_GRAPH}> {{
        ?v a sh:ValidationResult ;
           sh:sourceShape ?propertyShape ;
           sh:focusNode ?focusNode ;
           sh:resultSeverity sh:Violation .

        OPTIONAL {{ ?v sh:resultPath ?path .}}
        OPTIONAL {{ ?v sh:sourceConstraintComponent ?constraint . }}
        OPTIONAL {{ ?v sh:resultMessage ?message . }}
        OPTIONAL {{ ?v sh:value ?value . }}}}
    }}"""
    results = run_sparql_query(query)
    focus_nodes = {}
    paths = {}
    constraints = {}
    instance_details = {}
    for row in results:
        fn = row.get("focusNode", {}).get("value")
        if not fn:
            continue

        focus_nodes[fn] = focus_nodes.get(fn, 0) + 1
        path =row.get("path", {}).get("value")
        constraint = row.get("constraint", {}).get("value")
        msg = row.get("message", {}).get( "value")
        value = row.get("value", {}).get("value")

        if path:
            paths[path] = paths.get(path, 0) + 1
        if constraint:
            constraints[constraint] = constraints.get(constraint, 0) + 1

        if fn not in instance_details:
            instance_details[fn] = {

                "node": fn,
                "violations": [],
            }

        instance_details[fn]["violations"].append(
            {
                "property": _get_last_part(path) if path else "unknown",
                "path": path,
                "message": msg or "Violation",
                "constraint": _get_last_part(constraint) if constraint else None,
                "constraintUri": constraint,
                "value": value,
                "valueShort": _get_last_part(value) if value else None,
            }
        )

    total_violations = sum(focus_nodes.values())

    constraint_definitions = [
        {"constraint": _get_last_part(k), "count": v}
        for k, v in sorted(constraints.items(), key=lambda x: x[1], reverse=True)
    ]

    instances_payload = []
    for fn, info in instance_details.items():
        instances_payload.append(
            {
                "node": fn,
                "violations": info["violations"],}
        )
    instances_payload.sort(key=lambda x: len(x.get("violations", [])), reverse=True)
    return {
        "class": class_uri,"totalInstances":len(focus_nodes),"instancesWithViolations": len(focus_nodes),"totalViolations": total_violations,"violatedProperties": len(paths),
        "constraintsTriggered": len(constraints),"mostAffectedInstance": max(focus_nodes, key=focus_nodes.get) if focus_nodes else None,"mostViolatedPath": max(paths, key=paths.get) if paths else None,"mostTriggeredConstraint": max(constraints, key=constraints.get) if constraints else None,
        "topInstances": [
            {"instance": k, "violations": v}
            for k,v in sorted(focus_nodes.items(), key=lambda x: x[1], reverse=True)[:30]],
        "topPaths": [
            {"path": k, "violations": v}
            for k,v in sorted(paths.items(), key=lambda x: x[1], reverse=True)[:30]],
        "topConstraints": [
            {"constraint": k, "count":v}
            for k,v in sorted(constraints.items(), key=lambda x: x[1], reverse=True)[:30]],
        "constraintDefinitions": constraint_definitions,
        "instances": instances_payload,
    }
