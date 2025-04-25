import pytest
from config.config import BASE_URL
from utils.api_helper import APIHelper
from playwright.async_api import TimeoutError

test_results = []

async def run_test_case(portal_page, test_name, add_method, product_options=None, cart_actions=None, expected_outcome="success"):
    home = portal_page["home"]
    page = home.page

    print(f"\nRunning test case: {test_name}")

    result = {
        "test_name": test_name,
        "passed": True,
        "details": [],
        "expected_outcome": expected_outcome
    }

    try:
        await home.navigate()
        await home.close_newsletter_popup()
        await home.scroll_down()
        await home.scroll_down()

        if add_method == "quick_view":
            try:
                await home.quick_view_product()
                if product_options:
                    await home.view_select_product_options_and_click_find_your_size(product_options)
            except Exception as e:
                result["passed"] = False
                result["details"].append(f"Error al usar 'Quick View': {str(e)}")
                if expected_outcome != "failure":
                    pytest.fail(f"Fallo inesperado en 'Quick View': {str(e)}")
                else:
                    result["passed"] = True

        elif add_method == "quick_add":
            try:
                await home.quick_add_product()
                if product_options:
                    await home.add_select_product_options_and_quick_add_to_cart(product_options)
            except Exception as e:
                result["passed"] = False
                result["details"].append(f"Error al usar 'Quick Add': {str(e)}")
                if expected_outcome != "failure":
                    pytest.fail(f"Fallo inesperado en 'Quick Add': {str(e)}")
                else:
                    result["passed"] = True
        else:
            raise ValueError(f"Método de adición inválido: {add_method}")

        if cart_actions:
            try:
                await home.interact_with_cart(cart_actions)
            except Exception as e:
                result["passed"] = False
                result["details"].append(f"Error al interactuar con el carrito: {str(e)}")
                if expected_outcome != "failure":
                    pytest.fail(f"Fallo inesperado en interacciones con el carrito: {str(e)}")

        cart_items = page.locator("#shoppingCart .tf-mini-cart-item")
        item_count = await cart_items.count()

        if expected_outcome == "success":
            if item_count <= 0:
                result["passed"] = False
                result["details"].append("El carrito está vacío cuando se esperaba al menos un elemento.")
                pytest.fail(f"Fallo en '{test_name}': El carrito está vacío.")
        else:
            if item_count > 0:
                result["passed"] = False
                result["details"].append("El carrito tiene elementos cuando se esperaba que fallara.")
                pytest.fail(f"Fallo en '{test_name}': El carrito tiene elementos inesperadamente.")

        if result["passed"]:
            print(f"Test {test_name}: Ejecución exitosa")

    except TimeoutError:
        result["passed"] = False
        result["details"].append("Timeout alcanzado durante la ejecución.")
        pytest.fail(f"Fallo en '{test_name}': Timeout alcanzado")

    except Exception as e:
        result["passed"] = False
        result["details"].append(f"Error inesperado: {str(e)}")
        pytest.fail(f"Error en '{test_name}': {str(e)}")

    test_results.append(result)

@pytest.mark.parametrize("test_data", [
    pytest.param(("Quick View - Full Options", "quick_view", {"color": "Blue", "size": "L", "quantity": 2}, ["adjust_quantity", "add_note"], "success")),
    pytest.param(("Quick Add - No Options", "quick_add", None, ["adjust_quantity"], "failure")),
    pytest.param(("Quick View - Partial Options", "quick_view", {"color": "White"}, ["estimate_shipping"], "success")),
    pytest.param(("Quick Add - Full Options", "quick_add", {"color": "White", "size": "M", "quantity": 3}, ["add_note"], "success")),
    pytest.param(("Quick View - No Options", "quick_view", None, None, "failure")),
    pytest.param(("Quick Add - Invalid Quantity -20", "quick_add", {"color": "Blue", "size": "S", "quantity": -20}, None, "failure")),
    pytest.param(("Quick View - Extreme Quantity 1000", "quick_view", {"color": "Blue", "size": "L", "quantity": 1000}, ["adjust_quantity"], "success")),
    pytest.param(("Quick Add - All Cart Actions", "quick_add", {"color": "White", "size": "M", "quantity": 1}, ["adjust_quantity", "add_note", "estimate_shipping"], "success")),
    pytest.param(("Quick View - Invalid Quantity -1", "quick_view", {"color": "Blue", "size": "L", "quantity": -1}, None, "failure")),
])

@pytest.mark.asyncio
async def test_home_cases(portal_page, test_data):
    test_name, add_method, product_options, cart_actions, expected_outcome = test_data
    await run_test_case(portal_page, test_name, add_method, product_options, cart_actions, expected_outcome)
