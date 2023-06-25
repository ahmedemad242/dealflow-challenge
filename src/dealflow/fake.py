import click
from flask import Blueprint
from faker import Faker
from dealflow import db
from dealflow.models.freelancer import Freelancer
from datetime import datetime

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
            date_of_birth=faker.date_between_dates(
                date_start=datetime(1990, 1, 1), date_end=datetime(2005, 12, 31)
            ),
        )
        db.session.add(freelancer)

    db.session.commit()
    print(num, "freelancers added.")
