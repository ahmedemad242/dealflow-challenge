from flask import Blueprint
from apifairy import response, arguments

from dealflow.schemas import PaginatedCollection, PaginatedQueryParams
from dealflow.api.freelancers.schemas import FreelancerSchema, FreelancerFilterSchema
from dealflow.api.freelancers.business import retrievePaginatedFreelancers

freelancers_bp = Blueprint("freelancers", __name__)
freelancers_schema = FreelancerSchema(many=True)
paginated_freelancers_schema = PaginatedCollection(freelancers_schema)


@freelancers_bp.route("/freelancers", methods=["GET"])
@arguments(PaginatedQueryParams(FreelancerFilterSchema))
@response(paginated_freelancers_schema)
def all(freelancerPagination):
    """Retrieve all users"""

    limit = freelancerPagination.get("limit", 25)
    offset = freelancerPagination.get("offset", 0)
    firstname = freelancerPagination.get("firstname", None)
    lastname = freelancerPagination.get("lastname", None)
    email = freelancerPagination.get("email", None)

    return retrievePaginatedFreelancers(
        limit=limit, offset=offset, firstname=firstname, lastname=lastname, email=email
    )
