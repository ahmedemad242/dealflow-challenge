from locust import HttpUser, task


class WebsiteUser(HttpUser):
    @task
    def getFreelancers(self):
        self.client.get(url="/api/freelancers")
