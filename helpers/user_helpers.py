from data import USER_PASSWORD
from helpers.email_generator import generate_email


def generate_registration_data():
    return {
        "email": generate_email(),
        "password": USER_PASSWORD,
        "submitPassword": USER_PASSWORD,
    }
