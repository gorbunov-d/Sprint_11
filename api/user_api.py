from api.base_api import BaseApi
from urls import SIGNIN, SIGNUP


class UserApi(BaseApi):
    def register(self, credentials):
        return self.request("POST", SIGNUP, json=credentials)

    def login(self, credentials):
        return self.request(
            "POST",
            SIGNIN,
            json={
                "email": credentials["email"],
                "password": credentials["password"],
            },
        )
