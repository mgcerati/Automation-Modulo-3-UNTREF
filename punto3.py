import logging
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"

logger = logging.getLogger(__name__)


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    options.add_argument("--disable-save-password-bubble")
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


def login(driver):
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys(USERNAME)
    driver.find_element(By.ID, "password").send_keys(PASSWORD)
    driver.find_element(By.ID, "login-button").click()
    logger.info("Login realizado como '%s'", USERNAME)


# ─── Caso 1 ───────────────────────────────────────────────────────────────────
class TestCaso1:
    def test_ordenar_precio_low_to_high(self, driver):
        login(driver)

        select = Select(driver.find_element(By.CLASS_NAME, "product_sort_container"))
        select.select_by_value("lohi")
        logger.info("Ordenamiento seleccionado: 'Price (low to high)'")

        precios = driver.find_elements(By.CLASS_NAME, "inventory_item_price")
        valores = [float(p.text.replace("$", "")) for p in precios]
        logger.info("Precios obtenidos: %s", valores)

        logger.info("Verificando que los precios estén ordenados de menor a mayor")
        assert valores == sorted(valores), (
            f"Los precios no estan ordenados de menor a mayor: {valores}"
        )
        logger.info("OK: precios ordenados correctamente")


# ─── Caso 2 ───────────────────────────────────────────────────────────────────
class TestCaso2:
    def test_checkout_validaciones(self, driver):
        login(driver)

        total_productos = len(driver.find_elements(By.CSS_SELECTOR, "button.btn_primary.btn_inventory"))
        logger.info("Total de productos disponibles: %d", total_productos)
        for _ in range(total_productos):
            driver.find_elements(By.CSS_SELECTOR, "button.btn_primary.btn_inventory")[0].click()
        logger.info("Todos los productos agregados al carrito")

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        logger.info("Verificando cantidad de items en carrito: esperado=%d, actual=%d", total_productos, len(items))
        assert len(items) == total_productos, (
            f"Se esperaban {total_productos} productos en el carrito, "
            f"pero hay {len(items)}."
        )
        logger.info("OK: todos los productos están en el carrito")

        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("Martin")
        driver.find_element(By.ID, "continue").click()
        logger.info("Checkout iniciado solo con nombre, sin apellido")

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        logger.info("Verificando error de apellido: '%s'", error)
        assert "Last Name is required" in error, (
            f"Error esperado 'Last Name is required', pero se obtuvo: '{error}'"
        )
        logger.info("OK: error 'Last Name is required' presente")

        driver.find_element(By.ID, "last-name").send_keys("Perez")
        driver.find_element(By.ID, "continue").click()
        logger.info("Apellido ingresado, continuando sin código postal")

        error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']").text
        logger.info("Verificando error de código postal: '%s'", error)
        assert "Postal Code is required" in error, (
            f"Error esperado 'Postal Code is required', pero se obtuvo: '{error}'"
        )
        logger.info("OK: error 'Postal Code is required' presente")


# ─── Caso 3 ───────────────────────────────────────────────────────────────────
class TestCaso3:
    def test_flujo_compra_completo(self, driver):
        login(driver)

        driver.find_elements(By.CSS_SELECTOR, "button.btn_inventory")[0].click()
        logger.info("Un producto agregado al carrito")

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
        driver.find_element(By.CSS_SELECTOR, "button.cart_button").click()
        logger.info("Producto removido del carrito")

        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        logger.info("Verificando que el carrito está vacío: items=%d", len(items))
        assert len(items) == 0, "El carrito debería estar vacío tras remover el artículo."

        badge = driver.find_elements(By.CLASS_NAME, "shopping_cart_badge")
        logger.info("Verificando que el badge del carrito desapareció")
        assert len(badge) == 0, "El badge del carrito debería desaparecer."
        logger.info("OK: carrito vacío y badge eliminado")

        driver.find_element(By.ID, "continue-shopping").click()
        logger.info("Regresando a la tienda")

        driver.find_elements(By.CSS_SELECTOR, "button.btn_primary.btn_inventory")[0].click()
        driver.find_elements(By.CSS_SELECTOR, "button.btn_primary.btn_inventory")[0].click()
        logger.info("2 productos agregados al carrito")

        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        items = driver.find_elements(By.CLASS_NAME, "cart_item")
        logger.info("Verificando que hay 2 items en el carrito: actual=%d", len(items))
        assert len(items) == 2, (
            f"Se esperaban 2 productos en el carrito, pero hay {len(items)}."
        )
        logger.info("OK: 2 productos en el carrito")

        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("Martin")
        driver.find_element(By.ID, "last-name").send_keys("Perez")
        driver.find_element(By.ID, "postal-code").send_keys("1234")
        driver.find_element(By.ID, "continue").click()
        logger.info("Datos de checkout ingresados, continuando")

        driver.find_element(By.ID, "finish").click()
        logger.info("Compra finalizada, verificando mensaje de confirmación")

        wait = WebDriverWait(driver, 10)
        confirmacion = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
        )
        logger.info("Mensaje de confirmación obtenido: '%s'", confirmacion.text)
        assert "Thank you for your order" in confirmacion.text, (
            f"No se encontró el mensaje de confirmación. Texto: '{confirmacion.text}'"
        )
        logger.info("OK: compra realizada exitosamente")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--html=reporte_punto3.html", "--self-contained-html", "--log-cli-level=INFO"])