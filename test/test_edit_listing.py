import pytest

from data import FOREIGN_LISTING_ERROR, LISTING_CHANGES
from helpers.assertions import assert_listing_matches


class TestEditListing:
    @pytest.mark.parametrize("field,value", LISTING_CHANGES, ids=["name", "description", "price"])
    def test_owner_edits_listing_successfully(
        self, listing_api, registered_user, created_listing, listing_data, field, value
    ):
        updated_data = {**listing_data, field: value}
        listing_id = created_listing["id"]

        response = listing_api.update(registered_user.token, listing_id, updated_data)

        assert response.status_code == 200, response.text
        assert_listing_matches(
            response.json(), updated_data, listing_id, registered_user.user_id
        )
        saved_response = listing_api.get_own_listings(registered_user.token)
        assert saved_response.status_code == 200, saved_response.text
        offers = saved_response.json()["offers"]
        assert len(offers) == 1
        assert_listing_matches(
            offers[0], updated_data, listing_id, registered_user.user_id
        )

    def test_other_user_cannot_edit_listing(
        self, listing_api, registered_user, other_user, created_listing, listing_data
    ):
        listing_id = created_listing["id"]
        field, value = LISTING_CHANGES[0]
        updated_data = {**listing_data, field: value}
        assert other_user.user_id != registered_user.user_id

        response = listing_api.update(other_user.token, listing_id, updated_data)

        assert response.status_code == 401, response.text
        assert response.json() == FOREIGN_LISTING_ERROR
        saved_response = listing_api.get_own_listings(registered_user.token)
        assert saved_response.status_code == 200, saved_response.text
        offers = saved_response.json()["offers"]
        assert len(offers) == 1
        assert_listing_matches(
            offers[0], listing_data, listing_id, registered_user.user_id
        )
