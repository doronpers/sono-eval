import json
import random
import string

from locust import HttpUser, between, task


class SonoEvalUser(HttpUser):
    wait_time = between(1, 4)
    token = None
    candidate_id = None

    def on_start(self):
        """Login and setup user session."""
        self.login()
        self.candidate_id = f"load_test_user_{''.join(random.choices(string.ascii_lowercase, k=5))}"

    def login(self):
        """Authenticate with the API."""
        response = self.client.post(
            "/api/v1/auth/token", data={"username": "admin", "password": "secret"}
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    @task(3)
    def view_health(self):
        """View health checkpoint (frequent action)."""
        self.client.get("/health")

    @task(1)
    def generate_tags(self):
        """Generate tags for random text."""
        text = "This is a sample python function def hello(): print('world')"
        self.client.post("/api/v1/tags/generate", json={"text": text, "max_tags": 5})

    @task(1)
    def create_assessment(self):
        """Create a full assessment."""
        payload = {
            "candidate_id": self.candidate_id,
            "submission_type": "code",
            "content": {"code": "def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)"},
            "paths_to_evaluate": ["technical", "problem_solving"],
        }
        self.client.post("/api/v1/assessments", json=payload)
