

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
from utils.helpers import (
    extraer_precio,
    esperar_url_contiene,
)


class TestCheckout:


    @pytest.fixture(autouse=True)
    def setup_carrito(self, driver_sesion):
   
        self.driver = driver_sesion

        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)

        inventario.go_to_cart()
        esperar_url_contiene(driver_sesion, "cart")


    def test_carrito_muestra_titulo_correcto(self):
        """
        TC-020 | VALIDACIÓN
        Verificar que la página del carrito tiene el título 'Your Cart'.

        Resultado esperado:
          - El título de la página es 'Your Cart'.
        """
        carrito = CartPage(self.driver)
        titulo = carrito.get_page_title()

        assert titulo == CART_TITLE, (
            f"[TC-020] Título incorrecto. "
            f"Esperado: '{CART_TITLE}' | Obtenido: '{titulo}'"
        )

    def test_carrito_contiene_exactamente_un_item(self):
      
        carrito = CartPage(self.driver)
        cantidad = carrito.get_item_count()

        assert cantidad == 1, (
            f"[TC-021] Se esperaba 1 ítem, "
            f"pero el carrito tiene: {cantidad}"
        )

    def test_carrito_contiene_el_producto_correcto(self):
  
        carrito = CartPage(self.driver)
        nombres_en_carrito = carrito.get_item_names()

        assert PRODUCT_NAME in nombres_en_carrito, (
            f"[TC-022] '{PRODUCT_NAME}' no está en el carrito. "
            f"Items actuales: {nombres_en_carrito}"
        )


    def test_click_checkout_navega_al_formulario(self):
      
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        esperar_url_contiene(self.driver, "checkout-step-one")

        checkout_info = CheckoutInfoPage(self.driver)
        titulo = checkout_info.get_page_title()

        assert titulo == CHECKOUT_INFO_TITLE, (
            f"[TC-023] Título incorrecto. "
            f"Esperado: '{CHECKOUT_INFO_TITLE}' | Obtenido: '{titulo}'"
        )

    def test_formulario_error_sin_first_name(self):
      
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.click_continue()  # Sin llenar ningún campo

        error = checkout_info.get_error_message()

        assert "First Name is required" in error, (
            f"[TC-024] Mensaje de error inesperado: '{error}'"
        )

    def test_formulario_error_sin_last_name(self):
   
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.send_keys(*CheckoutInfoPage.FIRST_NAME, CHECKOUT_FIRST_NAME)
        checkout_info.click_continue()

        error = checkout_info.get_error_message()

        assert "Last Name is required" in error, (
            f"[TC-025] Mensaje de error inesperado: '{error}'"
        )

    def test_formulario_error_sin_postal_code(self):
     
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.send_keys(*CheckoutInfoPage.FIRST_NAME, CHECKOUT_FIRST_NAME)
        checkout_info.send_keys(*CheckoutInfoPage.LAST_NAME, CHECKOUT_LAST_NAME)
        checkout_info.click_continue()

        error = checkout_info.get_error_message()

        assert "Postal Code is required" in error, (
            f"[TC-026] Mensaje de error inesperado: '{error}'"
        )


    def test_resumen_muestra_total_mayor_a_cero(self):
       
        carrito = CartPage(self.driver)
        carrito.click_checkout()

        checkout_info = CheckoutInfoPage(self.driver)
        checkout_info.fill_information(
            CHECKOUT_FIRST_NAME,
            CHECKOUT_LAST_NAME,
            CHECKOUT_POSTAL_CODE
        )
        checkout_info.click_continue()

        resumen = CheckoutOverviewPage(self.driver)
        total_texto = resumen.get_total()

        total_valor = extraer_precio(total_texto)

        assert total_valor > 0, (
            f"[TC-027] El total debería ser > $0, "
            f"pero se obtuvo: '{total_texto}' → {total_valor}"
        )


    def test_flujo_completo_de_compra_end_to_end(self):
       
        carrito = CartPage(self.driver)
        assert carrito.get_page_title() == CART_TITLE, \
            "[TC-028 | Paso 1] No se está en la página del carrito."
        assert carrito.get_item_count() == 1, \
            "[TC-028 | Paso 1] El carrito no tiene exactamente 1 ítem."

        carrito.click_checkout()
        esperar_url_contiene(self.driver, "checkout-step-one")

        checkout_info = CheckoutInfoPage(self.driver)
        assert checkout_info.get_page_title() == CHECKOUT_INFO_TITLE, \
            "[TC-028 | Paso 3] No se está en el formulario de checkout."

        checkout_info.fill_information(
            CHECKOUT_FIRST_NAME,
            CHECKOUT_LAST_NAME,
            CHECKOUT_POSTAL_CODE
        )
        checkout_info.click_continue()
        esperar_url_contiene(self.driver, "checkout-step-two")

        resumen = CheckoutOverviewPage(self.driver)
        assert resumen.get_page_title() == CHECKOUT_OVERVIEW_TITLE, \
            "[TC-028 | Paso 4] No se está en la página de resumen."

        total_texto = resumen.get_total()
        total_valor = extraer_precio(total_texto)
        assert total_valor > 0, \
            f"[TC-028 | Paso 4] Total inválido: '{total_texto}'"

        resumen.click_finish()
        esperar_url_contiene(self.driver, "checkout-complete")

        confirmacion = CheckoutCompletePage(self.driver)

        assert confirmacion.get_page_title() == CHECKOUT_COMPLETE_TITLE, (
            f"[TC-028 | Paso 6] Título incorrecto. "
            f"Esperado: '{CHECKOUT_COMPLETE_TITLE}' | "
            f"Obtenido: '{confirmacion.get_page_title()}'"
        )

        header = confirmacion.get_complete_header()
        assert "Thank you for your order" in header, (
            f"[TC-028 | Paso 6] Mensaje de confirmación inesperado: '{header}'"
        )

        assert confirmacion.is_order_complete(), \
            "[TC-028 | Paso 6] La orden no se marcó como completada."

        print(f"\n✅ [TC-028] Compra completada exitosamente. Header: '{header}'")
