ENDPOINT_URL = "http://localhost:8890/sparql"


AUTH_REQUIRED = False
USERNAME = ""
PASSWORD = ""

TRIPLE_STORE_TYPE = "virtuoso"

SHAPES_GRAPH_URI = "http://ex.org/ShapesGraph"
VALIDATION_REPORT_URI = "http://ex.org/ValidationReport"

SHACL_FEATURES = [
    "http://www.w3.org/ns/shacl#class",
    "http://www.w3.org/ns/shacl#datatype",
    "http://www.w3.org/ns/shacl#NodeKind",
    "http://www.w3.org/ns/shacl#minCount",
    "http://www.w3.org/ns/shacl#maxCount",
    "http://www.w3.org/ns/shacl#minExclusive",
    "http://www.w3.org/ns/shacl#minInclusive",
    "http://www.w3.org/ns/shacl#maxExclusive",
    "http://www.w3.org/ns/shacl#maxInclusive",
    "http://www.w3.org/ns/shacl#minLength",
    "http://www.w3.org/ns/shacl#maxLength",
    "http://www.w3.org/ns/shacl#pattern",
    "http://www.w3.org/ns/shacl#languageIn",
    "http://www.w3.org/ns/shacl#uniqueLang",
    "http://www.w3.org/ns/shacl#equals",
    "http://www.w3.org/ns/shacl#disjoint",
    "http://www.w3.org/ns/shacl#lessThan",
    "http://www.w3.org/ns/shacl#lessThanOrEquals",
    "http://www.w3.org/ns/shacl#not",
    "http://www.w3.org/ns/shacl#and",
    "http://www.w3.org/ns/shacl#or",
    "http://www.w3.org/ns/shacl#xone",
    "http://www.w3.org/ns/shacl#node",
    "http://www.w3.org/ns/shacl#qualifiedMinCount",
    "http://www.w3.org/ns/shacl#qualifiedMaxCount",
    "http://www.w3.org/ns/shacl#closed",
    "http://www.w3.org/ns/shacl#hasValue",
    "http://www.w3.org/ns/shacl#in"
]

DATA_DIR_IN_DOCKER = "/data"
DOCKER_CONTAINER_NAME = "virtuoso"

STORE_CONFIG = {
    "virtuoso": {
        "isql_path": "/usr/local/virtuoso-opensource/bin/isql",
        "isql_port": 1111,
        "bulk_load_enabled": True,
    },
    "fuseki": {
        "admin_endpoint": "http://localhost:3030/$/",
        "bulk_load_enabled": False,
    },
    "stardog": {
        "admin_endpoint": "http://localhost:5820",
        "database": "shacldb",
        "bulk_load_enabled": True,
    }
}