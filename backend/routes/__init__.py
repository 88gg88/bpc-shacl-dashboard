from flask import Blueprint

from .landing_routes import landing_bp
from .homepage_routes import homepage_bp
from .shapes_overview_routes import shapes_overview_bp
from .shape_view_routes import shape_view_bp

from .class_view_routes import class_view_bp

from .property_path_overview_routes import property_path_overview_bp
from .property_path_view_routes import property_path_view_bp

blueprints = [
    landing_bp,
    homepage_bp,
    shapes_overview_bp,
    shape_view_bp,
    class_view_bp,
    property_path_overview_bp,
    property_path_view_bp,
]
