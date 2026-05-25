import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage
from utils.constants import BASE_URL, VALID_USER, VALID_PASSWORD
from utils.helpers import tomar_captura_en_falla, obtener_timestamp_legible

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")             
    chrome_options.add_argument("--disable-dev-shm-usage")  
    chrome_options.add_argument("--disable-gpu")            
    chrome_options.add_argument("--disable-extensions")

    navegador = webdriver.Chrome(options=chrome_options)

    
    navegador.implicitly_wait(5) 

    print(f"\n🚀 Navegador iniciado — {obtener_timestamp_legible()}")

    yield navegador  

    print(f"\n🔒 Cerrando navegador — {obtener_timestamp_legible()}")
    navegador.quit()

@pytest.fixture(scope="function")
def driver_sesion(driver):
    login = LoginPage(driver)
    login.open()
    login.login(VALID_USER, VALID_PASSWORD)

    print(f"✅ Sesión iniciada como '{VALID_USER}'")
    return driver  


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    reporte = outcome.get_result()

    if reporte.when == "call" and reporte.failed:
        
        driver_fixture = None
        if "driver" in item.fixturenames:
            driver_fixture = item.funcargs.get("driver")
        elif "driver_sesion" in item.fixturenames:
            driver_fixture = item.funcargs.get("driver_sesion")

        if driver_fixture:
            nombre_test = item.name.replace(" ", "_")
            ruta = tomar_captura_en_falla(driver_fixture, nombre_test)
            if ruta:
                print(f"\n📸 Captura de falla guardada: {ruta}")