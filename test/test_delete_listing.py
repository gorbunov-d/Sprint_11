from api.listing_api import ListingApi
from data import DELETE_SUCCESS


class TestDeleteListing:
    def test_owner_deletes_listing_successfully(
        self, session, registered_user, created_listing, listing_cleanup
    ):
        listing_id = created_listing["id"]

        response = ListingApi(session).delete(registered_user.token, listing_id)

        assert response.status_code == 200, response.text
        listing_cleanup.remove((listing_id, registered_user.token))
        assert response.json() == DELETE_SUCCESS
