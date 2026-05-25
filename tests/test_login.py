import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from utils.constants import (
    BASE_URL,
    VALID_USER,
    VALID_PASSWORD,
    LOCKED_USER,
    INVALID_PASSWORD,
    ERROR_EMPTY_FIELDS,
    ERROR_EMPTY_PASSWORD,
    ERROR_INVALID_CREDENTIALS,
    ERROR_LOCKED_USER,
    INVENTORY_TITLE,
)
from utils.helpers import generar_datos_usuario_invalido



URL_INVENTARIO   = f"{BASE_URL}/inventory.html"  # URL exacta post-login
TITULO_PESTAÑA   = "Swag Labs"                   # <title> del documento HTML
TITULO_CONTENIDO = "Products"                    # H1 visible en la página
TIMEOUT_ESPERA   = 10                            # segundos para WebDriverWait


# ─────────────────────────────────────────────────────────────────────────────
class TestLoginExitoso:


    def test_login_exitoso_valida_url_inventario(self, driver):
   
        login_page = LoginPage(driver)
        login_page.open()

        # Ingresar credenciales válidas y hacer login 
        login_page.login(VALID_USER, VALID_PASSWORD)

        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.url_contains("inventory.html"),
            message=(
                "Timeout: La URL no cambió a /inventory.html en "
                f"{TIMEOUT_ESPERA} segundos. URL actual: {driver.current_url}"
            )
        )

        # ── PASO 6: Verificar URL exacta ──────────────────────────────────
        url_actual = driver.current_url
        assert "inventory.html" in url_actual, (
            f"[TC-001] URL incorrecta tras el login.\n"
            f"  Esperada: contiene '/inventory.html'\n"
            f"  Obtenida: '{url_actual}'"
        )

    def test_login_exitoso_valida_titulo_contenido_products(self, driver):
        
        # Login 
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)

       
        elemento_titulo = WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title")),
            message=(
                f"Timeout: El título de la página de inventario no fue "
                f"visible en {TIMEOUT_ESPERA} segundos."
            )
        )

        # Verificar texto 
        titulo_obtenido = elemento_titulo.text
        assert titulo_obtenido == TITULO_CONTENIDO, (
            f"[TC-002] Título del contenido incorrecto.\n"
            f"  Esperado: '{TITULO_CONTENIDO}'\n"
            f"  Obtenido: '{titulo_obtenido}'"
        )

    def test_login_exitoso_valida_titulo_pestaña_swag_labs(self, driver):
       
        # Login 
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, VALID_PASSWORD)

        
        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.title_is(TITULO_PESTAÑA),
            message=(
                f"Timeout: El título de la pestaña no cambió a "
                f"'{TITULO_PESTAÑA}' en {TIMEOUT_ESPERA} segundos. "
                f"Título actual: '{driver.title}'"
            )
        )

        # Verificar título
        titulo_pestaña_actual = driver.title
        assert titulo_pestaña_actual == TITULO_PESTAÑA, (
            f"[TC-003] Título de pestaña incorrecto.\n"
            f"  Esperado: '{TITULO_PESTAÑA}'\n"
            f"  Obtenido: '{titulo_pestaña_actual}'"
        )

    def test_login_exitoso_triple_validacion_completa(self, driver):
        
        
        login_page = LoginPage(driver)
        login_page.open()

        # Verificar URL 
        assert BASE_URL in driver.current_url, (
            f"[TC-004] No se navegó a la página de login. "
            f"URL actual: '{driver.current_url}'"
        )

        # Ingresar credenciales 
        login_page.enter_username(VALID_USER)    
        login_page.enter_password(VALID_PASSWORD)  
        login_page.click_login()                   

        
        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.url_contains("inventory.html"),
            message="[TC-004] La URL no redirigió a /inventory.html"
        )

       
        elemento_titulo = WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title")),
            message="[TC-004] El título 'Products' no fue visible en el DOM"
        )

        
        
        url_actual = driver.current_url
        assert "inventory.html" in url_actual, (
            f"[TC-004 | URL] Redirección incorrecta.\n"
            f"  Esperada: contiene 'inventory.html'\n"
            f"  Obtenida: '{url_actual}'"
        )

        
        titulo_contenido = elemento_titulo.text
        assert titulo_contenido == TITULO_CONTENIDO, (
            f"[TC-004 | TÍTULO H1] Texto incorrecto en la página.\n"
            f"  Esperado: '{TITULO_CONTENIDO}'\n"
            f"  Obtenido: '{titulo_contenido}'"
        )

        
        titulo_pestaña = driver.title
        assert titulo_pestaña == TITULO_PESTAÑA, (
            f"[TC-004 | TITLE] Título de pestaña incorrecto.\n"
            f"  Esperado: '{TITULO_PESTAÑA}'\n"
            f"  Obtenido: '{titulo_pestaña}'"
        )


# ─────────────────────────────────────────────────────────────────────────────
class TestLoginFallido:
   

    def test_login_sin_credenciales_muestra_error_username(self, driver):
    
        login_page = LoginPage(driver)
        login_page.open()
        login_page.click_login()

        # ESPERA EXPLÍCITA — aguardar que el mensaje de error aparezca
        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            ),
            message="[TC-005] El mensaje de error no apareció en la página."
        )

        error_texto = login_page.get_error_message()
        assert ERROR_EMPTY_FIELDS in error_texto, (
            f"[TC-005] Error inesperado.\n"
            f"  Esperado: '{ERROR_EMPTY_FIELDS}'\n"
            f"  Obtenido: '{error_texto}'"
        )

    def test_login_sin_password_muestra_error_password(self, driver):
      
        login_page = LoginPage(driver)
        login_page.open()
        login_page.enter_username(VALID_USER)
        login_page.click_login()

        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            ),
            message="[TC-006] El mensaje de error no apareció."
        )

        error_texto = login_page.get_error_message()
        assert ERROR_EMPTY_PASSWORD in error_texto, (
            f"[TC-006] Error inesperado. Obtenido: '{error_texto}'"
        )

    def test_login_credenciales_invalidas_muestra_error_credenciales(self, driver):
        
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, INVALID_PASSWORD)

        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            ),
            message="[TC-007] El mensaje de error no apareció."
        )

        error_texto = login_page.get_error_message()
        assert ERROR_INVALID_CREDENTIALS in error_texto, (
            f"[TC-007] Error inesperado. Obtenido: '{error_texto}'"
        )

    def test_login_usuario_bloqueado_muestra_error_locked(self, driver):
       
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(LOCKED_USER, VALID_PASSWORD)

        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            ),
            message="[TC-008] El mensaje de error no apareció."
        )

        error_texto = login_page.get_error_message()
        assert ERROR_LOCKED_USER in error_texto, (
            f"[TC-008] Error inesperado. Obtenido: '{error_texto}'"
        )

    def test_login_fallido_no_redirige_al_inventario(self, driver):
      
        login_page = LoginPage(driver)
        login_page.open()
        login_page.login(VALID_USER, INVALID_PASSWORD)

        url_actual = driver.current_url
        assert "inventory" not in url_actual, (
            f"[TC-009] El login fallido NO debería redirigir al inventario.\n"
            f"  URL actual: '{url_actual}'"
        )

    # ── Test parametrizado ────────────────────────────────────────────────────

    @pytest.mark.parametrize("caso", [
        "sin_usuario",
        "sin_password",
        "credenciales_invalidas",
        "usuario_bloqueado",
    ])
    def test_login_negativo_parametrizado(self, driver, caso):
       
        datos = generar_datos_usuario_invalido(caso)

        login_page = LoginPage(driver)
        login_page.open()

        if datos["username"]:
            login_page.enter_username(datos["username"])
        if datos["password"]:
            login_page.enter_password(datos["password"])

        login_page.click_login()

        # Espera explícita antes de leer el error
        WebDriverWait(driver, TIMEOUT_ESPERA).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "[data-test='error']")
            ),
            message=f"[TC-010 | {caso}] El mensaje de error no apareció."
        )

        error_texto = login_page.get_error_message()
        assert datos["error_esperado"] in error_texto, (
            f"[TC-010 | {caso}] Error inesperado.\n"
            f"  Esperado contiene: '{datos['error_esperado']}'\n"
            f"  Obtenido: '{error_texto}'"
        )
