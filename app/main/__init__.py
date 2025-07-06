from flask import Blueprint

main = Blueprint("main", __name__)

from app.main import errors, views  # noqa: E402
from app.models import Permission


@main.app_context_processor
def inject_permissions():
    return {"Permission": Permission}
