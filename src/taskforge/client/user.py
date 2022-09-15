from taskforge.client.base import ModelClient


class UserClient(ModelClient):
    plural_name = "users"
    reverse_mapping_key = "email"

    def login(self, email: str, password: str):
        """
        Generates a PAT.
        """
        tokens = self.client.post(
            "/v1/tokens/pat",
            json={
                "email": email,
                "password": password,
            },
        )
        return tokens["pat"]
