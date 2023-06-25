"""
Business logic for the Freelancer API
"""

from flask import abort
from dealflow.models.freelancer import Freelancer


def retrievePaginatedFreelancers(
    offset=0, limit=10, firstname=None, lastname=None, email=None
):
    """
    Returns a list of freelancers
    -----
    parameters:
        page - int
        limit - int
        name - String
        email - String
        phone - String
    """

    if offset < 0 or limit < 0:
        abort(400, "Invalid pagination parameters")

    if limit > 25:
        limit = 25

    query = Freelancer.query

    if firstname:
        query = query.filter(Freelancer.firstname.ilike(f"%{firstname}%"))
    if lastname:
        query = query.filter(Freelancer.lastname.ilike(f"%{lastname}%"))
    if email:
        query = query.filter(Freelancer.email.ilike(f"%{email}%"))

    total = query.count()
    freelancers = query.offset(offset).limit(limit).all()

    return {
        "pagination": {
            "offset": offset,
            "limit": limit,
            "count": len(freelancers),
            "total": total,
        },
        "data": freelancers,
    }
