from helpers.assertions import assert_listing_matches


class TestCreateListing:
    def test_create_listing_successfully(
        self, listing_api, registered_user, listing_data, listing_cleanup
    ):
        response = listing_api.create(registered_user.token, listing_data)

        assert response.status_code == 201, response.text
        body = response.json()
        listing_id = body["id"]
        listing_cleanup.append((listing_id, registered_user.token))
        assert isinstance(listing_id, int)
        assert listing_id > 0
        assert_listing_matches(body, listing_data, listing_id, registered_user.user_id)

        saved_response = listing_api.get_own_listings(registered_user.token)
        assert saved_response.status_code == 200, saved_response.text
        offers = saved_response.json()["offers"]
        assert len(offers) == 1
        assert_listing_matches(
            offers[0], listing_data, listing_id, registered_user.user_id
        )
