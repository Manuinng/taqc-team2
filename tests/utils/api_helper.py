import requests
from typing import Dict, Any
from config.config import BASE_URL

class APIHelper:
    TOKEN = "mi-token-super-secreto"

    @staticmethod
    def get_user_id(email):
        """Retrieve user ID by email."""
        headers = {"Authorization": f"Bearer {APIHelper.TOKEN}"}
        response = requests.get(f"{BASE_URL}/api/user?email={email}", headers=headers)
        if response.status_code == 200:
            return response.json().get("id")
        return None

    @staticmethod
    def delete_user(user_id):
        """Delete user by ID."""
        headers = {"Authorization": f"Bearer {APIHelper.TOKEN}"}
        response = requests.delete(f"{BASE_URL}/api/user/{user_id}", headers=headers)
        return response.status_code == 200

    @staticmethod
    def get_csrf_token(session: requests.Session) -> str:
        response = session.get(f"{BASE_URL}/api/auth/csrf")
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Failed to retrieve CSRF token: {response.status_code}")
        return response.json().get('csrfToken')

    @staticmethod
    def login(session: requests.Session, email: str, password: str, csrf_token: str) -> requests.Response:
        data = {
            "email": email,
            "password": password,
            "redirect": "false",
            "csrfToken": csrf_token,
            "callbackUrl": f"{BASE_URL}/login",
            "json": "true"
        }
        response = session.post(f"{BASE_URL}/api/auth/callback/credentials", data=data)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Login failed: {response.status_code}")
        return response

    @staticmethod
    def get_auth_session(session: requests.Session) -> requests.Response:
        response = session.get(f"{BASE_URL}/api/auth/session")
        if response.status_code != 200:
            raise requests.exceptions.HTTPError(f"Failed to retrieve session cookie: {response.status_code}")
        return response

    @staticmethod
    def get_order(order_id: str) -> Dict[Any, Any]:
        response = requests.get(f"{BASE_URL}/api/orders/{order_id}")
        if not response.ok:
            raise requests.exceptions.HTTPError(f"Failed to retrieve order {order_id} from API - {response.status_code}")
        return response.json()
