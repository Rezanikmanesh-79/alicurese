from locust import HttpUser, task


class HelloWorldUser(HttpUser):
    def on_start(self):
        response = self.client.post("/accounts/api/v2/jwt/create/", json={
            "email": "admin@admin.com",
            "password": "1234"
        }).json()
        token = response.get("access")
        if token:
            self.client.headers.update({'Authorization': f'Bearer {token}'})

    @task
    def post_list(self):
        self.client.get("/blog/api/v1/post/")

    @task
    def category_list(self):
        self.client.get("/blog/api/v1/catgory/")
