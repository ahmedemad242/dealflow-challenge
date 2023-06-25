from marshmallow import validate, fields, pre_dump, post_dump
from dealflow import ma
from dealflow.models.freelancer import Freelancer
from datetime import date


class FreelancerFilterSchema(ma.Schema):
    firstname = ma.String()
    lastname = ma.String()
    email = ma.String()


class FreelancerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Freelancer
        ordered = True

    firstname = ma.auto_field(required=True, validate=validate.Length(max=120))
    lastname = ma.auto_field(required=True, validate=validate.Length(max=120))
    email = ma.auto_field(
        required=True, validate=[validate.Length(max=120), validate.Email()]
    )

    age = fields.Method("calculate_age", dump_only=True)
    public_id = ma.auto_field(dump_only=True)
    created_at = ma.auto_field(dump_only=True)

    date_of_birth = ma.auto_field(required=True, load_only=True, format="%Y-%m-%d")
    username = ma.auto_field(
        required=True, load_only=True, validate=validate.Length(min=3, max=64)
    )
    password = ma.String(required=True, load_only=True, validate=validate.Length(min=3))

    def calculate_age(self, obj):
        date = obj.date_of_birth
        print(date)
        if date:
            today = date.today()
            age = today.year - date.year
            if today.month < date.month or (
                today.month == date.month and today.day < date.day
            ):
                age -= 1
            return age
        return None
