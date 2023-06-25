from datetime import datetime
from dealflow import db
from dealflow.models.freelancer import Freelancer
from tests.base_test_case import BaseTestCase


class PaginationTests(BaseTestCase):
    """
    Tests for the pagination
    """

    def setUp(self):
        """
        Create 26 freelancers in the database
        """
        super().setUp()
        for i in range(26):
            freelancer = Freelancer(
                username=chr(ord("a") + i),
                email=f'{chr(ord("a") + i)}@example.com',
                password="test",
                firstname=f'firstname{chr(ord("a") + i)}',
                lastname=f'lastname{chr(ord("a") + i)}',
                date_of_birth=datetime(1990, 1, 1),
            )
            db.session.add(freelancer)
        db.session.commit()

    def test_pagination_default(self):
        """
        Test the default pagination
        """
        rv = self.client.get("/api/freelancers")
        assert rv.status_code == 200
        assert rv.json["pagination"]["total"] == 27
        assert rv.json["pagination"]["offset"] == 0
        assert rv.json["pagination"]["count"] == 25
        assert rv.json["pagination"]["limit"] == 25
        assert len(rv.json["data"]) == 25

    def test_pagination_page(self):
        """
        Test the pagination with parameter
        """
        rv = self.client.get("/api/freelancers?offset=10&limit=10")
        assert rv.status_code == 200
        assert rv.json["pagination"]["total"] == 27
        assert rv.json["pagination"]["offset"] == 10
        assert rv.json["pagination"]["count"] == 10
        assert rv.json["pagination"]["limit"] == 10
        assert len(rv.json["data"]) == 10

    def test_pagination_last(self):
        """
        Test the pagination of last page
        """
        rv = self.client.get("/api/freelancers?offset=20")
        assert rv.status_code == 200
        assert rv.json["pagination"]["total"] == 27
        assert rv.json["pagination"]["offset"] == 20
        assert rv.json["pagination"]["count"] == 7
        assert rv.json["pagination"]["limit"] == 25
        assert len(rv.json["data"]) == 7

    def test_pagination_invalid(self):
        """
        Test the pagination with invalid parameters
        """
        rv = self.client.get("/api/freelancers?offset=-2")
        assert rv.status_code == 400
        rv = self.client.get("/api/freelancers?limit=-10")
        assert rv.status_code == 400

    def test_pagination_custom_limit(self):
        rv = self.client.get("/api/freelancers?offset=16&limit=5")
        assert rv.status_code == 200
        assert rv.json["pagination"]["total"] == 27
        assert rv.json["pagination"]["offset"] == 16
        assert rv.json["pagination"]["count"] == 5
        assert rv.json["pagination"]["limit"] == 5
        assert len(rv.json["data"]) == 5

    def test_pagination_large_per_page(self):
        rv = self.client.get("/api/freelancers?offset=26&limit=50")
        assert rv.status_code == 200
        assert rv.json["pagination"]["total"] == 27
        assert rv.json["pagination"]["offset"] == 26
        assert rv.json["pagination"]["count"] == 1
        assert rv.json["pagination"]["limit"] == 25
        assert len(rv.json["data"]) == 1
