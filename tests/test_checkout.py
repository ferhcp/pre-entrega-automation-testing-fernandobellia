import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutInfoPage,
    CheckoutOverviewPage,
    CheckoutCompletePage,
)
from utils.constants import (
    PRODUCT_NAME,
    CART_TITLE,
    CHECKOUT_INFO_TITLE,
    CHECKOUT_OVERVIEW_TITLE,
    CHECKOUT_COMPLETE_TITLE,
    CHECKOUT_FIRST_NAME,
    CHECKOUT_LAST_NAME,
    CHECKOUT_POSTAL_CODE,
)
from utils.helpers import extraer_precio, esperar_url_contiene


class TestCheckout:
    @pytest.fixture(autouse=True)
    def setup_carrito(self, driver_sesion):
        self.driver = driver_sesion

        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)
        inventario.go_to_cart()
        esperar_url_contiene(driver_sesion, "cart")

    # Validación del carrito 

    def test_carrito_muestra_titulo_correcto(self):
        carrito = CartPage(self.driver)
        assert carrito.get_page_title() == CART_TITLE, (
            f"[TC-034] Título incorrecto. Obtenido: '{carrito.get_page_title()}'"
        )

    def test_carrito_contiene_exactamente_un_item(self):
        carrito = CartPage(self.driver)
        assert carrito.get_item_count() == 1, (
            f"[TC-035] Se esperaba 1 ítem, pero hay: {carrito.get_item_count()}"
        )

    def test_carrito_contiene_el_producto_correcto(self):
        carrito = CartPage(self.driver)
        assert PRODUCT_NAME in carrito.get_item_names(), (
            f"[TC-036] '{PRODUCT_NAME}' no está en el carrito. "
            f"Items: {carrito.get_item_names()}"
        )

    # checkout 

    def test_click_checkout_navega_al_formulario(self):
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        esperar_url_contiene(self.driver, "checkout-step-one")

        checkout_info = CheckoutInfoPage(self.driver)
        assert checkout_info.get_page_title() == CHECKOUT_INFO_TITLE, (
            f"[TC-037] Título incorrecto: '{checkout_info.get_page_title()}'"
        )

    def test_formulario_error_sin_first_name(self):
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.click_continue()

        assert "First Name is required" in checkout_info.get_error_message(), (
            f"[TC-038] Error inesperado: '{checkout_info.get_error_message()}'"
        )

    def test_formulario_error_sin_last_name(self):
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        heckout_info.fill_only_first_name(CHECKOUT_FIRST_NAME)
        checkout_info.click_continue()

        assert "Last Name is required" in checkout_info.get_error_message(), (
            f"[TC-039] Error inesperado: '{checkout_info.get_error_message()}'"
        )

    """def test_formulario_error_sin_postal_code(self):
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.fill_first_and_last_name(CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME)
        checkout_info.click_continue()

        assert "Postal Code is required" in checkout_info.get_error_message(), (
            f"[TC-040] Error inesperado: '{checkout_info.get_error_message()}'"
        )"""

    # Validación del resumen

    def test_resumen_muestra_total_mayor_a_cero(self):
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.fill_information(
            CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_POSTAL_CODE
        )
        checkout_info.click_continue()

        resumen = CheckoutOverviewPage(self.driver)
        total_valor = extraer_precio(resumen.get_total())

        assert total_valor > 0, (
            f"[TC-041] Total inválido: '{resumen.get_total()}' → {total_valor}"
        )

    def test_flujo_completo_de_compra_end_to_end(self):
        carrito = CartPage(self.driver)
        assert carrito.get_page_title() == CART_TITLE
        assert carrito.get_item_count() == 1

        carrito.click_checkout()
        esperar_url_contiene(self.driver, "checkout-step-one")

        # Completar formulario
        checkout_info = CheckoutInfoPage(self.driver)
        assert checkout_info.get_page_title() == CHECKOUT_INFO_TITLE
        checkout_info.fill_information(
            CHECKOUT_FIRST_NAME, CHECKOUT_LAST_NAME, CHECKOUT_POSTAL_CODE
        )
        checkout_info.click_continue()
        esperar_url_contiene(self.driver, "checkout-step-two")

        # Verificar resumen
        resumen = CheckoutOverviewPage(self.driver)
        assert resumen.get_page_title() == CHECKOUT_OVERVIEW_TITLE
        assert extraer_precio(resumen.get_total()) > 0

        # Confirmar compra
        resumen.click_finish()
        esperar_url_contiene(self.driver, "checkout-complete")

        # Verificar confirmación
        confirmacion = CheckoutCompletePage(self.driver)
        assert confirmacion.get_page_title() == CHECKOUT_COMPLETE_TITLE
        assert "Thank you for your order" in confirmacion.get_complete_header()
        assert confirmacion.is_order_complete()

        print(f"\n✅ [TC-042] Compra E2E completada: '{confirmacion.get_complete_header()}'")
