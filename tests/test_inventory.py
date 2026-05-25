import pytest
from selenium.webdriver.common.by import By

from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.constants import (
    INVENTORY_TITLE,
    CART_TITLE,
    PRODUCT_NAME,
    BASE_URL,
)
from utils.helpers import (
    contar_elementos,
    extraer_precio,
    obtener_texto_todos_elementos,
    esperar_url_contiene,
)


class TestInventory:
    def test_pagina_inventario_muestra_titulo_correcto(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        titulo_obtenido = inventario.get_page_title()

        assert titulo_obtenido == INVENTORY_TITLE, (
            f"[TC-010] Título incorrecto. "
            f"Esperado: '{INVENTORY_TITLE}' | Obtenido: '{titulo_obtenido}'"
        )

    def test_inventario_muestra_exactamente_seis_productos(self, driver_sesion):
        cantidad = contar_elementos(
            driver_sesion, By.CLASS_NAME, "inventory_item"
        )

        assert cantidad == 6, (
            f"[TC-011] Se esperaban 6 productos, "
            f"pero se encontraron: {cantidad}"
        )

    def test_todos_los_productos_tienen_nombre_visible(self, driver_sesion):
        nombres = obtener_texto_todos_elementos(
            driver_sesion, By.CLASS_NAME, "inventory_item_name"
        )

        assert len(nombres) == 6, (
            f"[TC-012] Se esperaban 6 nombres de productos, "
            f"pero se encontraron: {len(nombres)}"
        )
        for nombre in nombres:
            assert nombre.strip() != "", (
                f"[TC-012] Un producto tiene el nombre vacío: '{nombre}'"
            )

    def test_todos_los_productos_tienen_precio_valido(self, driver_sesion):
        precios_texto = obtener_texto_todos_elementos(
            driver_sesion, By.CLASS_NAME, "inventory_item_price"
        )

        assert len(precios_texto) == 6, (
            f"[TC-013] Se esperaban 6 precios, se encontraron: {len(precios_texto)}"
        )

        for texto in precios_texto:
            precio = extraer_precio(texto)  # Usando helper de utils/helpers.py
            assert precio > 0, (
                f"[TC-013] Precio inválido encontrado: '{texto}' → {precio}"
            )

    def test_agregar_producto_actualiza_badge_carrito(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)

        badge_count = inventario.get_cart_count()

        assert badge_count == 1, (
            f"[TC-014] El badge del carrito debería ser 1, "
            f"pero muestra: {badge_count}"
        )

    def test_agregar_multiples_productos_actualiza_badge(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart("Sauce Labs Backpack")
        inventario.add_product_to_cart("Sauce Labs Bike Light")

        badge_count = inventario.get_cart_count()

        assert badge_count == 2, (
            f"[TC-015] El badge debería mostrar 2, "
            f"pero muestra: {badge_count}"
        )

    def test_quitar_producto_elimina_badge_carrito(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(PRODUCT_NAME)

        assert inventario.get_cart_count() == 1, (
            "[TC-016] El producto no se agregó correctamente al carrito."
        )

        inventario.remove_product_from_cart(PRODUCT_NAME)

        assert inventario.get_cart_count() == 0, (
            "[TC-016] El badge debería desaparecer al remover el producto, "
            f"pero muestra: {inventario.get_cart_count()}"
        )

    def test_click_en_icono_carrito_navega_a_cart(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.go_to_cart()

        esperar_url_contiene(driver_sesion, "cart")

        carrito = CartPage(driver_sesion)
        titulo = carrito.get_page_title()

        assert titulo == CART_TITLE, (
            f"[TC-017] Título incorrecto en carrito. "
            f"Esperado: '{CART_TITLE}' | Obtenido: '{titulo}'"
        )

    def test_logout_desde_menu_redirige_a_login(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        inventario.logout()

        url_actual = driver_sesion.current_url
        url_esperada = f"{BASE_URL}/"

        assert url_actual == url_esperada or url_actual == BASE_URL, (
            f"[TC-018] URL incorrecta tras logout. "
            f"Esperada: '{url_esperada}' | Actual: '{url_actual}'"
        )

    @pytest.mark.parametrize("nombre_producto", [
        "Sauce Labs Backpack",
        "Sauce Labs Bike Light",
        "Sauce Labs Bolt T-Shirt",
    ])
    def test_agregar_cada_producto_al_carrito(self, driver_sesion, nombre_producto):
        inventario = InventoryPage(driver_sesion)
        inventario.add_product_to_cart(nombre_producto)

        badge_count = inventario.get_cart_count()

        assert badge_count == 1, (
            f"[TC-019 | {nombre_producto}] "
            f"El badge debería ser 1, pero es: {badge_count}"
        )


class TestNavegacionCatalogo:
    def test_titulo_pagina_inventario_es_correcto(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)
        titulo = inventario.get_page_title()

        assert titulo == INVENTORY_TITLE, (
            f"[TC-020 | Segundo commit] Título incorrecto.\n"
            f"  Esperado: '{INVENTORY_TITLE}'\n"
            f"  Obtenido: '{titulo}'"
        )

   

    def test_catalogo_tiene_al_menos_un_producto_visible(self, driver_sesion):
        cantidad = contar_elementos(
            driver_sesion, By.CLASS_NAME, "inventory_item"
        )

        assert cantidad >= 1, (
            f"[TC-021 | Segundo commit] No se encontró ningún producto visible.\n"
            f"  Cantidad detectada: {cantidad}"
        )

   

    def test_primer_producto_tiene_nombre_y_precio_visibles(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)

        nombre_primero = inventario.get_first_product_name()
        precio_primero = inventario.get_first_product_price()

        print(f"\n[Segundo commit | TC-022] Primer producto del catálogo:")
        print(f"  Nombre : {nombre_primero}")
        print(f"  Precio : {precio_primero}")

        # Validar nombre 
        assert nombre_primero.strip() != "", (
            "[TC-022 | Segundo commit] El nombre del primer producto está vacío."
        )

        # Validar formato de precio
        assert precio_primero.startswith("$"), (
            f"[TC-022 | Segundo commit] El precio no tiene formato '$XX.XX'.\n"
            f"  Obtenido: '{precio_primero}'"
        )

        # Validar que el precio es numérico y positivo
        valor_numerico = extraer_precio(precio_primero)
        assert valor_numerico > 0, (
            f"[TC-022 | Segundo commit] El precio debe ser > 0.\n"
            f"  Texto: '{precio_primero}' → Valor: {valor_numerico}"
        )

    def test_menu_hamburguesa_esta_presente_en_la_interfaz(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)

        assert inventario.is_burger_menu_visible(), (
            "[TC-023 | Segundo commit] El menú hamburguesa (☰) no está visible "
            "en la página de inventario."
        )

    
    def test_filtro_ordenamiento_esta_presente_en_la_interfaz(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)

        assert inventario.is_sort_dropdown_visible(), (
            "[TC-024 | Segundo commit] El dropdown de filtros/ordenamiento "
            "no está visible en la página de inventario."
        )

    
    def test_icono_carrito_esta_presente_en_la_interfaz(self, driver_sesion):
        inventario = InventoryPage(driver_sesion)

        assert inventario.is_cart_icon_visible(), (
            "[TC-025 | Segundo commit] El ícono del carrito no está visible "
            "en la página de inventario."
        )
