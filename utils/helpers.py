import os
import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Espera y sincronización

def esperar_url_contiene(driver, texto_url, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(EC.url_contains(texto_url))
        return True
    except TimeoutException:
        url_actual = driver.current_url
        raise TimeoutException(
            f"Timeout: La URL '{url_actual}' no contiene '{texto_url}' "
            f"después de {timeout} segundos."
        )


def esperar_elemento_desaparece(driver, by, locator, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located((by, locator))
        )
        return True
    except TimeoutException:
        return False


# Captura de pantalla

def tomar_captura(driver, nombre_test, directorio="reports/screenshots"):
    try:
        # Crear directorio si no existe
        os.makedirs(directorio, exist_ok=True)

        # Generar nombre de archivo con timestamp para evitar colisiones
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"{nombre_test}_{timestamp}.png"
        ruta_completa = os.path.join(directorio, nombre_archivo)

        driver.save_screenshot(ruta_completa)
        print(f"\n📸 Captura guardada: {ruta_completa}")
        return ruta_completa

    except Exception as e:
        print(f"\n⚠️  No se pudo guardar la captura: {e}")
        return None


def tomar_captura_en_falla(driver, nombre_test):
    return tomar_captura(driver, f"FALLA_{nombre_test}")



# validaciónes 

def verificar_titulo_pagina(driver, titulo_esperado):
    titulo_actual = driver.title
    return titulo_actual == titulo_esperado


def elemento_existe_en_pagina(driver, by, locator):
    try:
        driver.find_element(by, locator)
        return True
    except NoSuchElementException:
        return False


def contar_elementos(driver, by, locator):
    elementos = driver.find_elements(by, locator)
    return len(elementos)

def extraer_precio(texto_precio):
    import re
    # Busca uno o más dígitos, punto opcional y más dígitos
    match = re.search(r'\d+\.\d+', texto_precio)
    if not match:
        raise ValueError(
            f"No se encontró un precio válido en el string: '{texto_precio}'"
        )
    return float(match.group())


def formatear_nombre_producto_a_id(nombre_producto):
    return nombre_producto.lower().replace(" ", "-")


def obtener_timestamp_legible():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def generar_datos_usuario_invalido(caso):
    catalogo = {
        "sin_usuario": {
            "username": "",
            "password": "",
            "error_esperado": "Username is required"
        },
        "sin_password": {
            "username": "standard_user",
            "password": "",
            "error_esperado": "Password is required"
        },
        "credenciales_invalidas": {
            "username": "standard_user",
            "password": "wrong_password",
            "error_esperado": "Username and password do not match"
        },
        "usuario_bloqueado": {
            "username": "locked_out_user",
            "password": "secret_sauce",
            "error_esperado": "Sorry, this user has been locked out"
        },
    }

    if caso not in catalogo:
        claves_validas = list(catalogo.keys())
        raise KeyError(
            f"Caso '{caso}' no existe. Opciones válidas: {claves_validas}"
        )

    return catalogo[caso]


def hacer_scroll_al_fondo(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)  # Pausa breve para que el scroll se complete


def hacer_scroll_al_inicio(driver):
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(0.3)


def obtener_texto_todos_elementos(driver, by, locator):
    elementos = driver.find_elements(by, locator)
    return [el.text for el in elementos if el.text.strip()]
