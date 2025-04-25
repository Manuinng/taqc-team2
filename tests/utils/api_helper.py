import requests

class APIHelper:
    BASE_URL = "https://automation-portal-bootcamp.vercel.app/api/user"
    TOKEN = "mi-token-super-secreto"

    @staticmethod
    def get_user_id(email):
        """Retrieve user ID by email."""
        headers = {"Authorization": f"Bearer {APIHelper.TOKEN}"}
        response = requests.get(f"{APIHelper.BASE_URL}?email={email}", headers=headers)
        if response.status_code == 200:
            return response.json().get("id")
        return None

    @staticmethod
    def delete_user(user_id):
        """Delete user by ID."""
        headers = {"Authorization": f"Bearer {APIHelper.TOKEN}"}
        response = requests.delete(f"{APIHelper.BASE_URL}/{user_id}", headers=headers)
        return response.status_code == 200