"""
Test cases for freelancer model.
"""

from datetime import datetime
import pytest
from dealflow.models.freelancer import Freelancer
from tests.base_test_case import BaseTestCase


class FreelancerModelTests(BaseTestCase):
    """
    Test cases for freelancer model.
    """

    def test_password_hashing(self):
        """
        Test password hashing.
        """
        freelancer = Freelancer(
            username="ahmed",
            password="cat",
            firstname="ahmed",
            lastname="ahmed",
            email="ahmed@gmail.com",
            date_of_birth=datetime(1990, 1, 1),
        )
        assert not freelancer.checkPassword("dog")
        assert freelancer.checkPassword("cat")
        with pytest.raises(AttributeError):
            freelancer.password
