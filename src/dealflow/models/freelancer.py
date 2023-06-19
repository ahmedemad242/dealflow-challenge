""" User model """

from datetime import datetime, timedelta
from uuid import uuid4

from dealflow.utils.result import Result
from flask import current_app

from dealflow import db, bcrypt


class Freelancer(db.Model):
    """
    Freelancer model to store freelancer information.

    Fields:
        id              -   INT         -   Primary key for the freelancer.
        username        -   VARCHAR     -   Freelancer username for login.
        password        -   VARCHAR     -   Freelancer password for login.
        email           -   VARCHAR     -   Freelancer email address.
        firstname       -   VARCHAR     -   Freelancer first name.
        lastname        -   VARCHAR     -   Freelancer last name.
        public_id       -   VARCHAR     -   Public id for the freelancer.
        date_of_birth   -   DATE        -   Date of birth of the freelancer.
        created_at      -   TIMESTAMP   -   Timestamp indicating when the freelancer account was created.
        updated_at      -   TIMESTAMP   -   Timestamp indicating when the freelancer account was last updated.
        deleted_at      -   TIMESTAMP   -   Timestamp indicating when the freelancer account was deleted.

    """

    __tablename__ = "freelancer"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    publicId = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.TIMESTAMP,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )
    deleted_at = db.Column(db.TIMESTAMP)

    def __init__(
        self, email, password, username, firstname, lastname, date_of_birth, **kwargs
    ):
        super(Freelancer, self).__init__(**kwargs)

        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.date_of_birth = date_of_birth

    def __repr__(self):
        return f"<Freelancer email={self.email}, username={self.username}>"

    @classmethod
    def insert(cls, email, password, username, firstname, lastname, date_of_birth):
        """
        inserts freelancer to the database and returns the newly created freelancer
        """

        freelancer = Freelancer(
            email, password, username, firstname, lastname, date_of_birth
        )
        db.session.add(freelancer)
        db.session.commit()

        return freelancer

    @classmethod
    def delete(cls, id):
        """
        removes freelancer from the database
        """

        freelancer = cls.query.findByID(id)
        db.session.delete(freelancer)
        db.session.commit()

    @classmethod
    def update(cls, id, email, password, username, firstname, lastname, date_of_birth):
        """
        updates existing freelancer record and returns the updated freelancer
        """

        freelancer = cls.query.get(id)

        freelancer.email = email
        freelancer.password = password
        freelancer.username = username
        freelancer.firstname = firstname
        freelancer.lastname = lastname
        freelancer.date_of_birth = date_of_birth
        db.session.commit()

        return freelancer

    @classmethod
    def findByEmail(cls, email):
        """
        Returns freelancer data given a valid email
        -----
        parameters:
            email - String
        """

        freelancer = cls.query.filter_by(email=email).first()
        return freelancer

    @classmethod
    def findByPublicId(cls, publicId):
        """
        Returns freelancer data given a valid publicId
        -----
        parameters:
            publicId - String
        """

        freelancer = cls.query.filter_by(publicId=publicId).first()
        return freelancer

    @classmethod
    def findById(cls, id):
        """
        Returns freelancer data given a valid id
        -----
        parameters:
            id - int
        """

        freelancer = cls.query.filter_by(id=id).first()
        return freelancer

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        """
        Sets password in database as a hash
        -----
        parameters:
            password - String
        """

        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.passwordHash = hash_bytes.decode("utf-8")

    def checkPassword(self, password):
        """
        Returns true if a given password matches database
        -----
        parameters:
            password - String
        """

        return bcrypt.check_password_hash(self.passwordHash, password)
