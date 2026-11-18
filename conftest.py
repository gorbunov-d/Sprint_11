from dataclasses import dataclass

import pytest
import requests

from api.listing_api import ListingApi
from api.user_api import UserApi
from data import DELETE_SUCCESS, LISTING_DATA, USER_PASSWORD
from helpers.email_generator import generate_email


@dataclass(frozen=True)
class RegisteredUser:
    credentials: dict
    user_id: int
    token: str


@pytest.fixture
def session():
    with requests.Session() as http_session:
        yield http_session


@pytest.fixture
def user_api(session):
    return UserApi(session)


@pytest.fixture
def listing_api(session):
    return ListingApi(session)


@pytest.fixture
def registration_data():
    return {
        "email": generate_email(),
        "password": USER_PASSWORD,
        "submitPassword": USER_PASSWORD,
    }


@pytest.fixture
def user_factory(user_api):
    def create_user():
        credentials = {
            "email": generate_email(),
            "password": USER_PASSWORD,
            "submitPassword": USER_PASSWORD,
        }
        response = user_api.register(credentials)
        assert response.status_code == 201, response.text
        body = response.json()
        return RegisteredUser(
            credentials=credentials,
            user_id=body["user"]["id"],
            token=body["access_token"]["access_token"],
        )

    return create_user


@pytest.fixture
def registered_user(user_factory):
    return user_factory()


@pytest.fixture
def other_user(user_factory):
    return user_factory()


@pytest.fixture
def listing_data():
    return LISTING_DATA.copy()


@pytest.fixture
def listing_cleanup(listing_api):
    """Удаляет только объявления этого теста, в том числе после падения проверки."""
    listings = []
    yield listings
    errors = []
    for listing_id, token in listings:
        try:
            response = listing_api.delete(token, listing_id)
            assert response.status_code == 200, response.text
            assert response.json() == DELETE_SUCCESS
        except (requests.RequestException, AssertionError, ValueError) as error:
            errors.append(f"Объявление {listing_id}: {error}")
    assert not errors, "\n".join(errors)


@pytest.fixture
def created_listing(listing_api, registered_user, listing_data, listing_cleanup):
    response = listing_api.create(registered_user.token, listing_data)
    assert response.status_code == 201, response.text
    listing = response.json()
    listing_cleanup.append((listing["id"], registered_user.token))
    return listing
