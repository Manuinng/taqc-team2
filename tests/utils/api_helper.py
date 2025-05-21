import requests
from typing import Optional, Dict, Any
from uuid import UUID
from config.config import BASE_URL
from tests.utils.common_utils import camel_to_snake

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

    @staticmethod
    def validate_order(order_id: UUID, reference_form_data: Dict[str, str], reference_product: Optional[Dict[str, str]] = None):
        api_order_data = APIHelper.get_order(order_id)
        assert "id" in api_order_data, "API response is missing 'id' field"
        assert "items" in api_order_data, "API response is missing 'items' field"
        api_order_data.pop("createdAt", None)
        api_order_id = api_order_data.pop("id")
        api_cart_data = api_order_data.pop("items", [])

        errors = []

        for key, value in api_order_data.items():
            key = camel_to_snake(key)
            reference = reference_form_data.get(key, None)
            if value != reference:
                errors.append(f"Order {key} mismatch: reference = {reference}, API = {value}")

        if reference_product:
            reference_product_keys = ["title", "price", "quantity"]
            reference_product_data = {
                key: reference_product[key]
                for key in reference_product_keys
                if key in reference_product
            }
            product = api_cart_data[0]
            product.pop("id", None)
            for key, value in product.items():
                if key == "orderId":
                    reference = api_order_id
                else:
                    reference = reference_product_data.get(key, None)
                if value != reference:
                    errors.append(f"Product {key} mismatch: reference = {reference}, API = {value}")

        assert not errors, "API order data mismatch (check complete message for details)\n" + '\n'.join(errors)
