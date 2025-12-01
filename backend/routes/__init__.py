from flask import Blueprint

# Import all blueprints
from .shapes_overview_routes import shapes_overview_bp
from .landing_routes import landing_bp
from .homepage_routes import homepage_bp
from .shape_view_routes import shape_view_bp
from .class_view_routes import class_view_bp
from .class_overview_routes import class_overview_bp

# List of all blueprints to be registered in the app
blueprints = [
    shapes_overview_bp,
    landing_bp,
    homepage_bp,
    shape_view_bp,
    class_view_bp,
    class_overview_bp
]
