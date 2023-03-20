from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.enums.user import UserRole
from app.services import user as service_user

from ._common import has_role, paginated, to_dict

application_user = Blueprint("application_user", __name__)


@application_user.route("/")
@jwt_required()
@has_role([UserRole.ADMIN])
@to_dict()
@paginated(nbr_results_max=10)
def list_(nbr_results: int, page_nbr: int):
    return service_user.list_(nbr_results=nbr_results, page_nbr=page_nbr)


@application_user.route("/<uuid>")
@jwt_required()
@has_role([UserRole.ADMIN])
@to_dict()
def get(uuid: str):
    return service_user.get(uuid=uuid)
