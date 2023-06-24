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
        "offset": offset,
        "limit": limit,
        "count": len(freelancers),
        "total": total,
        "data": freelancers,
    }
