from api.user_api import UserApi


class TestLogin:
    def test_registered_user_logs_in_successfully(self, session, registered_user):
        response = UserApi(session).login(registered_user.credentials)

        assert response.status_code == 201, response.text
        body = response.json()
        assert body["user"]["id"] == registered_user.user_id
        assert body["user"]["email"] == registered_user.credentials["email"]
        assert isinstance(body["token"]["access_token"], str)
