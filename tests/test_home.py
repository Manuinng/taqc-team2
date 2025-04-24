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
                    for option, value in product_options.items():
                        selector = f"select[name='{option}'], input[name='{option}']"
                        is_valid = await page.evaluate(
                            """(field) => field.value === arguments[1]""",
                            await page.query_selector(selector),
                            value
                        )
                        if not is_valid:
                            result["passed"] = False
                            result["details"].append(f"El campo '{option}' no tiene el valor esperado '{value}'.")
                            pytest.fail(f"Fallo en '{test_name}': El campo '{option}' no es válido.")
            except Exception as e:
                result["passed"] = False
                result["details"].append(f"Error al abrir 'Quick View' o seleccionar opciones: {str(e)}")
                if expected_outcome != "failure":
                    pytest.fail(f"Fallo inesperado en 'Quick View': {str(e)}")
        
        elif add_method == "quick_add":
            try:
                await home.quick_add_product()
                if product_options:
                    await home.add_select_product_options_and_quick_add_to_cart(product_options)
                    for option, value in product_options.items():
                        selector = f"select[name='{option}'], input[name='{option}']"
                        is_valid = await page.evaluate(
                            """(field) => field.value === arguments[1]""",
                            await page.query_selector(selector),
                            value
                        )
                        if not is_valid:
                            result["passed"] = False
                            result["details"].append(f"El campo '{option}' no tiene el valor esperado '{value}'.")
                            pytest.fail(f"Fallo en '{test_name}': El campo '{option}' no es válido.")
            except Exception as e:
                result["passed"] = False
                result["details"].append(f"Error al abrir 'Quick Add' o agregar al carrito: {str(e)}")
                if expected_outcome != "failure":
                    pytest.fail(f"Fallo inesperado en 'Quick Add': {str(e)}")
        
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
                result["details"].append("El carrito contiene elementos cuando se esperaba que fallara.")
        
        if result["passed"]:
            print(f"Test {test_name}: Ejecución exitosa")
    
    except TimeoutError:
        result["passed"] = False
        result["details"].append("Timeout alcanzado durante la ejecución.")
        pytest.fail(f"Fallo en '{test_name}': Timeout alcanzado")
    
    except AssertionError as e:
        result["passed"] = False
        result["details"].append(f"Fallo en la verificación: {str(e)}")
        if expected_outcome != "failure":
            pytest.fail(f"Fallo inesperado en '{test_name}': {str(e)}")
    
    except Exception as e:
        result["passed"] = False
        result["details"].append(f"Error inesperado: {str(e)}")
        pytest.fail(f"Error en '{test_name}': {str(e)}")
    
    test_results.append(result)

@pytest.mark.parametrize("test_data", [
    # Escenario 1: Quick View con opciones completas
    pytest.param(("Quick View - Full Options", "quick_view", {"color": "Blue", "size": "L", "quantity": 2}, ["adjust_quantity", "add_note"], "success")),
    
    # Escenario 2: Quick Add sin opciones
    pytest.param(("Quick Add - No Options", "quick_add", None, ["adjust_quantity"], "success")),
    
    # Escenario 3: Quick View con opciones parciales
    pytest.param(("Quick View - Partial Options", "quick_view", {"color": "White"}, ["estimate_shipping"], "success")),
    
    # Escenario 4: Quick Add con opciones completas
    pytest.param(("Quick Add - Full Options", "quick_add", {"color": "White", "size": "M", "quantity": 3}, ["add_note"], "success")),
    
    # Escenario 5: Quick View sin opciones (esperando fallo si las opciones son obligatorias)
    pytest.param(("Quick View - No Options", "quick_view", None, None, "failure")),
    
    # Escenario 6: Quick Add con cantidad inválida
    pytest.param(("Quick Add - Invalid Quantity", "quick_add", {"color": "Blue", "size": "S", "quantity": -1}, None, "failure")),
    
    # Escenario 7: Múltiples acciones en el carrito con Quick View
    pytest.param(("Quick View - Multiple Cart Actions", "quick_view", {"color": "Blue", "size": "L", "quantity": 1}, ["adjust_quantity", "add_note", "estimate_shipping"], "success")),
])
@pytest.mark.asyncio
async def test_home_cases(portal_page, test_data):
    test_name, add_method, product_options, cart_actions, expected_outcome = test_data
    await run_test_case(portal_page, test_name, add_method, product_options, cart_actions, expected_outcome)