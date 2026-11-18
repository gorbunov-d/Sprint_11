from api.base_api import BaseApi


class UserApi(BaseApi):
    def register(self, credentials):
        return self.request("POST", "/signup", json=credentials)

    def login(self, credentials):
        return self.request(
            "POST",
            "/signin",
            json={
                "email": credentials["email"],
                "password": credentials["password"],
            },
        )
