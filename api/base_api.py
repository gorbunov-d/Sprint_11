from config import BASE_URL, REQUEST_TIMEOUT


class BaseApi:
    def __init__(self, session):
        self.session = session

    def request(self, method, path, **kwargs):
        return self.session.request(
            method,
            f"{BASE_URL}{path}",
            timeout=REQUEST_TIMEOUT,
            **kwargs,
        )

    @staticmethod
    def auth_headers(token):
        return {"Authorization": f"Bearer {token}"}
