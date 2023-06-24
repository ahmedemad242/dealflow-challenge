"""
Welcome to the documentation for the dealflow API!

## Introduction

dealflow is an easy to use web API for retrieving freelancers information.

## Pagination

API endpoints that return collections of resources, such as tfreelancers,
implement pagination, and the client must use query string arguments to specify
the range of items to return.

The number of items to return is specified by the `limit` argument, which is
optional. If not specified, the server sets the limit to a reasonable value for
the endpoint. If the limit is too large, the server may decide to use a lower
value instead. The following example shows how to request the first 10 freelancers:

    http://localhost:5000/api/freelancers?limit=10

The `offset` argument is used to specify the zero-based index of the first item
to return. If not given, the server sets the offset to 0. The following example
shows how to request the second page of users with a page size of 10:

    http://localhost:5000/api/freelancers?limit=10&offset=10

The response body in a paginated request contains a `data` attribute that is
set to the list of entities that are in the requested page. A `pagination`
attribute is also included with `offset`, `limit`, `count` and `total`
sub-attributes, which should enable the client to present pagination controls
to the freelancers.
"""

from flask import Flask, redirect, url_for, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from apifairy import APIFairy

from dealflow.config import get_config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
ma = Marshmallow()
apifairy = APIFairy()


def create_app(config_name):
    app = Flask("dealflow")
    app.config.from_object(get_config(config_name))

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    apifairy.init_app(app)

    from dealflow.api.freelancers import freelancers_bp
    from dealflow.fake import fake_bp

    app.register_blueprint(freelancers_bp, url_prefix="/api")
    app.register_blueprint(fake_bp)

    @app.route("/")
    def index():
        return redirect(url_for("apifairy.docs"))

    @app.after_request
    def after_request(response):
        request.get_data()
        return response

    return app
