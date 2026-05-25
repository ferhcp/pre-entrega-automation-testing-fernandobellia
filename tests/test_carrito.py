from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.constants import (
    PRODUCT_NAME,       
    CART_TITLE,         
    BADGE_INICIAL,      
    BADGE_UN_PRODUCTO,  
)

TIMEOUT = 10


class TestCarritoProductos:
    """
    Tercer commit — Suite de tests para Interacción con Productos y Carrito.

    Flujo base que cubre cada test:
      1. Partir de sesión iniciada en /inventory.html (fixture driver_sesion)
      2. Interactuar con el botón "Add to cart" del producto
      3. Verificar el badge del carrito
      4. Navegar al carrito
      5. Verificar el contenido del carrito
    """

   

    def test_badge_carrito_es_cero_antes_de_agregar(self, driver_sesion):
        
        # verificar estado inicial limpio
        inventario = InventoryPage(driver_sesion)
        badge_inicial = inventario.get_cart_count()

        assert badge_inicial == BADGE_INICIAL, (
            f"[TC-026 | Tercer commit] El badge debería ser 0 al inicio,\n"
            f"  pero muestra: {badge_inicial}"
        )

    def test_agregar_primer_producto_incrementa_badge_a_uno(self, driver_sesion):
         # agregar  producto al carrito
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)

        # espera visible tras agregar
        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "shopping_cart_badge")
            ),
            message=(
                f"[TC-027 | Tercer commit] El badge del carrito no apareció "
                f"después de agregar '{PRODUCT_NAME}'."
            )
        )

        badge_actual = inventario.get_cart_count()

        assert badge_actual == BADGE_UN_PRODUCTO, (
            f"[TC-027 | Tercer commit] Badge incorrecto tras agregar 1 producto.\n"
            f"  Esperado: {BADGE_UN_PRODUCTO}\n"
            f"  Obtenido: {badge_actual}"
        )

    def test_navegar_al_carrito_muestra_url_correcta(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)
        inventario.go_to_cart()

        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.url_contains("cart.html"),
            message=(
                "[TC-028 | Tercer commit] La URL no cambió a /cart.html "
                f"después de navegar al carrito. URL actual: {driver_sesion.current_url}"
            )
        )

        # verificar URL
        url_actual = driver_sesion.current_url
        assert "cart.html" in url_actual, (
            f"[TC-028 | Tercer commit] URL incorrecta al navegar al carrito.\n"
            f"  Esperada: contiene 'cart.html'\n"
            f"  Obtenida: '{url_actual}'"
        )

    def test_carrito_muestra_titulo_your_cart(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)
        inventario.go_to_cart()

        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.url_contains("cart.html"),
            message="[TC-029 | Tercer commit] No se llegó a /cart.html"
        )

        carrito = CartPage(driver_sesion)
        titulo = carrito.get_page_title()

        assert titulo == CART_TITLE, (
            f"[TC-029 | Tercer commit] Título del carrito incorrecto.\n"
            f"  Esperado: '{CART_TITLE}'\n"
            f"  Obtenido: '{titulo}'"
        )

    def test_producto_agregado_aparece_en_el_carrito(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)
        inventario.go_to_cart()

        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "cart_item")
            ),
            message=(
                "[TC-030 | Tercer commit] Ningún ítem es visible en el carrito "
                f"después de agregar '{PRODUCT_NAME}'."
            )
        )

        carrito = CartPage(driver_sesion)

        # verificar que el producto correcto está en el carrito
        assert carrito.product_is_in_cart(PRODUCT_NAME), (
            f"[TC-030 | Tercer commit] '{PRODUCT_NAME}' no aparece en el carrito.\n"
            f"  Ítems actuales: {carrito.get_item_names()}"
        )

        # verificar que hay exactamente 1 ítem
        cantidad = carrito.get_item_count()
        assert cantidad == 1, (
            f"[TC-030 | Tercer commit] Se esperaba 1 ítem en el carrito,\n"
            f"  pero se encontraron: {cantidad}"
        )

    def test_nombre_del_primer_item_en_carrito_es_correcto(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)
        inventario.go_to_cart()

        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")),
            message="[TC-031 | Tercer commit] El ítem no fue visible en el carrito."
        )

        carrito = CartPage(driver_sesion)
        nombre_en_carrito = carrito.get_first_item_name()

        assert nombre_en_carrito == PRODUCT_NAME, (
            f"[TC-031 | Tercer commit] Nombre del ítem incorrecto.\n"
            f"  Esperado: '{PRODUCT_NAME}'\n"
            f"  Obtenido: '{nombre_en_carrito}'"
        )

    def test_flujo_completo_agregar_y_verificar_en_carrito(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)

        assert inventario.get_cart_count() == BADGE_INICIAL, \
            "[TC-032 | Tercer commit | Paso 1] Badge inicial debe ser 0."

        # agregar producto y verificar
        inventario.add_product_to_cart(PRODUCT_NAME)

        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")),
            message="[TC-032 | Tercer commit | Paso 3] Badge no apareció."
        )
        assert inventario.get_cart_count() == BADGE_UN_PRODUCTO, \
            "[TC-032 | Tercer commit | Paso 3] Badge debe ser 1 tras agregar."

        # avegar al carrito y verificar URL
        inventario.go_to_cart()

        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.url_contains("cart.html"),
            message="[TC-032 | Tercer commit | Paso 5] URL no cambió a /cart.html."
        )
        assert "cart.html" in driver_sesion.current_url, \
            "[TC-032 | Tercer commit | Paso 5] URL incorrecta."

        carrito = CartPage(driver_sesion)

        # verificar título del carrito
        assert carrito.get_page_title() == CART_TITLE, \
            "[TC-032 | Tercer commit | Paso 6] Título del carrito incorrecto."

        # esperar ítem y verificar contenido
        WebDriverWait(driver_sesion, TIMEOUT).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cart_item")),
            message="[TC-032 | Tercer commit | Paso 7] Ítem no visible en carrito."
        )

        assert carrito.product_is_in_cart(PRODUCT_NAME), (
            f"[TC-032 | Tercer commit | Paso 7] '{PRODUCT_NAME}' no está en el carrito.\n"
            f"  Ítems: {carrito.get_item_names()}"
        )
        assert carrito.get_item_count() == 1, \
            "[TC-032 | Tercer commit | Paso 8] Debe haber exactamente 1 ítem."

        print(
            f"\n✅ [TC-032 | Tercer commit] Flujo completo OK — "
            f"'{PRODUCT_NAME}' agregado y verificado en /cart.html"
        )
