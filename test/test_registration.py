from data import DUPLICATE_EMAIL_ERROR


class TestRegistration:
    def test_register_new_user_successfully(self, user_api, registration_data):
        response = user_api.register(registration_data)

        assert response.status_code == 201, response.text
        body = response.json()
        assert body["user"]["email"] == registration_data["email"]
        assert isinstance(body["user"]["id"], int)
        assert body["user"]["id"] > 0
        token = body["access_token"]["access_token"]
        assert isinstance(token, str)
        assert token

    def test_register_existing_email_is_rejected(self, user_api, registered_user):
        response = user_api.register(registered_user.credentials)

        assert response.status_code == 400, response.text
        assert response.json() == DUPLICATE_EMAIL_ERROR
