from data import DELETE_SUCCESS


class TestDeleteListing:
    def test_owner_deletes_listing_successfully(
        self, listing_api, registered_user, created_listing, listing_cleanup
    ):
        listing_id = created_listing["id"]

        response = listing_api.delete(registered_user.token, listing_id)

        assert response.status_code == 200, response.text
        listing_cleanup.remove((listing_id, registered_user.token))
        assert response.json() == DELETE_SUCCESS
        saved_response = listing_api.get_own_listings(registered_user.token)
        assert saved_response.status_code == 200, saved_response.text
        assert saved_response.json()["offers"] == []
