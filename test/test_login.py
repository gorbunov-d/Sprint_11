class TestLogin:
    def test_registered_user_logs_in_successfully(
        self, user_api, listing_api, registered_user
    ):
        response = user_api.login(registered_user.credentials)

        assert response.status_code == 201, response.text
        body = response.json()
        assert body["user"]["id"] == registered_user.user_id
        assert body["user"]["email"] == registered_user.credentials["email"]
        token = body["token"]["access_token"]
        assert isinstance(token, str)
        assert token
        profile_response = listing_api.get_own_listings(token)
        assert profile_response.status_code == 200, profile_response.text
        assert profile_response.json()["offers"] == []
