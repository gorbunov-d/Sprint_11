import pytest

from api.listing_api import ListingApi
from data import FOREIGN_LISTING_ERROR, LISTING_CHANGES, LISTING_DATA
from helpers.assertions import assert_listing_matches


class TestEditListing:
    @pytest.mark.parametrize(
        "field,value", LISTING_CHANGES, ids=["name", "description", "price"]
    )
    def test_owner_edits_listing_successfully(
        self, session, registered_user, created_listing, field, value
    ):
        updated_data = {**LISTING_DATA, field: value}
        listing_id = created_listing["id"]

        response = ListingApi(session).update(
            registered_user.token, listing_id, updated_data
        )

        assert response.status_code == 200, response.text
        body = response.json()
        assert body["id"] == listing_id
        assert_listing_matches(
            body, updated_data, registered_user.user_id
        )

    def test_other_user_cannot_edit_listing(
        self, session, registered_user, foreign_listing
    ):
        field, value = LISTING_CHANGES[0]
        updated_data = {**LISTING_DATA, field: value}

        response = ListingApi(session).update(
            registered_user.token, foreign_listing["id"], updated_data
        )

        assert response.status_code == 401, response.text
        assert response.json() == FOREIGN_LISTING_ERROR
