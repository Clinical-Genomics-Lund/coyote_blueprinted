from flask import Blueprint

# Blueprint configuration
main_bp = Blueprint("main_bp", __name__, template_folder="templates", static_folder="static")

from coyote.blueprints.main import views  # noqa: F401, E402
