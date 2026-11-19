from api.user_api import UserApi
from data import DUPLICATE_EMAIL_ERROR
from helpers.user_helpers import generate_registration_data


class TestRegistration:
    def test_register_new_user_successfully(self, session):
        registration_data = generate_registration_data()

        response = UserApi(session).register(registration_data)

        assert response.status_code == 201, response.text
        body = response.json()
        assert body["user"]["email"] == registration_data["email"]
        assert isinstance(body["user"]["id"], int)
        assert isinstance(body["access_token"]["access_token"], str)

    def test_register_existing_email_is_rejected(self, session, registered_user):
        response = UserApi(session).register(registered_user.credentials)

        assert response.status_code == 400, response.text
        assert response.json() == DUPLICATE_EMAIL_ERROR
