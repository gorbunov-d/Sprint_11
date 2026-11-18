from api.base_api import BaseApi


class ListingApi(BaseApi):
    @staticmethod
    def multipart_fields(data):
        """None вместо имени файла создаёт обычные multipart-поля формы."""
        return {field: (None, str(value)) for field, value in data.items()}

    def create(self, token, data):
        return self.request(
            "POST",
            "/create-listing",
            headers=self.auth_headers(token),
            files=self.multipart_fields(data),
        )

    def update(self, token, listing_id, data):
        form_data = {**data, "img1": "null", "img2": "null", "img3": "null"}
        return self.request(
            "PATCH",
            f"/update-offer/{listing_id}",
            headers=self.auth_headers(token),
            files=self.multipart_fields(form_data),
        )

    def delete(self, token, listing_id):
        return self.request(
            "DELETE",
            f"/listings/{listing_id}",
            headers=self.auth_headers(token),
        )

    def get_own_listings(self, token, page=1):
        return self.request(
            "GET",
            f"/profile/listings/{page}",
            headers=self.auth_headers(token),
        )
