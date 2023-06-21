import random
import click
from flask import Blueprint
from faker import Faker
from dealflow import db
from dealflow.models.freelancer import Freelancer

fake_bp = Blueprint("fake", __name__)
faker = Faker()


@fake_bp.cli.command()
@click.argument("num", type=int)
def freelancers(num):
    """Create the given number of fake users."""
    for i in range(num):
        freelancer = Freelancer(
            email=faker.email(),
            password=faker.password(),
            username=faker.user_name(),
            firstname=faker.first_name(),
            lastname=faker.last_name(),
            date_of_birth=faker.date_time_this_year(),
        )
        db.session.add(freelancer)

    db.session.commit()
    print(num, "freelancers added.")
