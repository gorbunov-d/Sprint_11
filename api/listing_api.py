from api.base_api import BaseApi
from urls import CREATE_LISTING, DELETE_LISTING, OWN_LISTINGS, UPDATE_LISTING


class ListingApi(BaseApi):
    @staticmethod
    def multipart_fields(data):
        """None вместо имени файла создаёт обычные multipart-поля формы."""
        return {field: (None, str(value)) for field, value in data.items()}

    def create(self, token, data):
        return self.request(
            "POST",
            CREATE_LISTING,
            headers=self.auth_headers(token),
            files=self.multipart_fields(data),
        )

    def update(self, token, listing_id, data):
        form_data = {**data, "img1": "null", "img2": "null", "img3": "null"}
        return self.request(
            "PATCH",
            UPDATE_LISTING.format(listing_id=listing_id),
            headers=self.auth_headers(token),
            files=self.multipart_fields(form_data),
        )

    def delete(self, token, listing_id):
        return self.request(
            "DELETE",
            DELETE_LISTING.format(listing_id=listing_id),
            headers=self.auth_headers(token),
        )

    def get_own_listings(self, token, page=1):
        return self.request(
            "GET",
            OWN_LISTINGS.format(page=page),
            headers=self.auth_headers(token),
        )
