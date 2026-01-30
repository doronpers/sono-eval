import uuid

from locust import HttpUser, between, task


class AssessmentUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """Setup user."""
        self.candidate_id = f"test_user_{uuid.uuid4().hex[:8]}"
        # If authentication was enabled in load tests, we would login here

    @task(3)
    def submit_assessment(self):
        """Submit a standard assessment."""
        payload = {
            "candidate_id": self.candidate_id,
            "submission_type": "code",
            "content": {"file": "solution.py", "code": "def hello(): return 'world'"},
            "paths_to_evaluate": ["technical", "problem_solving"],
        }

        with self.client.post(
            "/api/v1/assessments", json=payload, catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Assessment submission failed: {response.status_code}"
                )

    @task(1)
    def check_health(self):
        """Check API health."""
        self.client.get("/health")

    @task(1)
    def check_system_status(self):
        """Check system status."""
        self.client.get("/api/v1/status/system")
