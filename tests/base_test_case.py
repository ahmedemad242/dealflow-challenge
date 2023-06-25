"""
Base test case for all test cases.
"""

import unittest
from datetime import datetime

from dealflow import create_app, db
from dealflow.models.freelancer import Freelancer


class BaseTestCase(unittest.TestCase):
    """
    Contains the base test case for all test cases
    """

    def setUp(self):
        self.app = create_app("testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        freelancer = Freelancer(
            username="userNameTest",
            email="test@example.com",
            password="foo",
            firstname="firstNameTest",
            lastname="lastNameTest",
            date_of_birth=datetime(1990, 1, 1),
        )
        db.session.add(freelancer)
        db.session.commit()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.close()
        db.drop_all()
        self.app_context.pop()
