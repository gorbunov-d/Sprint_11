from api.listing_api import ListingApi
from data import LISTING_DATA
from helpers.assertions import assert_listing_matches


class TestCreateListing:
    def test_create_listing_successfully(
        self, session, registered_user, listing_cleanup
    ):
        listing_data = LISTING_DATA.copy()

        response = ListingApi(session).create(registered_user.token, listing_data)

        assert response.status_code == 201, response.text
        body = response.json()
        listing_id = body["id"]
        listing_cleanup.append((listing_id, registered_user.token))
        assert isinstance(listing_id, int)
        assert_listing_matches(body, listing_data, registered_user.user_id)
