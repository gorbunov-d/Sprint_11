import pytest
import requests

from api.listing_api import ListingApi
from api.user_api import UserApi
from data import LISTING_DATA
from helpers.user_helpers import generate_registration_data
from models import RegisteredUser


@pytest.fixture
def session():
    with requests.Session() as http_session:
        yield http_session


@pytest.fixture
def registered_user(session):
    credentials = generate_registration_data()
    response = UserApi(session).register(credentials)
    response.raise_for_status()
    body = response.json()
    return RegisteredUser(
        credentials=credentials,
        user_id=body["user"]["id"],
        token=body["access_token"]["access_token"],
    )


@pytest.fixture
def listing_cleanup(session):
    """Удаляет только объявления этого теста, в том числе после падения проверки."""
    listings = []
    yield listings
    listing_api = ListingApi(session)
    errors = []
    for listing_id, token in listings:
        try:
            response = listing_api.delete(token, listing_id)
            response.raise_for_status()
        except requests.RequestException as error:
            errors.append(f"Объявление {listing_id}: {error}")
    if errors:
        raise RuntimeError("\n".join(errors))


@pytest.fixture
def created_listing(session, registered_user, listing_cleanup):
    response = ListingApi(session).create(registered_user.token, LISTING_DATA.copy())
    response.raise_for_status()
    listing = response.json()
    listing_cleanup.append((listing["id"], registered_user.token))
    return listing


@pytest.fixture
def foreign_listing(session, listing_cleanup):
    credentials = generate_registration_data()
    registration_response = UserApi(session).register(credentials)
    registration_response.raise_for_status()
    owner_token = registration_response.json()["access_token"]["access_token"]
    response = ListingApi(session).create(owner_token, LISTING_DATA.copy())
    response.raise_for_status()
    listing = response.json()
    listing_cleanup.append((listing["id"], owner_token))
    return listing
