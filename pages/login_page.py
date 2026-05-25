

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.constants import BASE_URL


class LoginPage(BasePage):


    # --- Localizadores ---
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON   = (By.ID, "login-button")
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
       
        self.driver.get(BASE_URL)
        return self

    def enter_username(self, username):
        """Escribe el nombre de usuario en el campo correspondiente."""
        self.send_keys(*self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        """Escribe la contraseña en el campo correspondiente."""
        self.send_keys(*self.PASSWORD_INPUT, password)
        return self

    def click_login(self):
        """Hace click en el botón de login."""
        self.click(*self.LOGIN_BUTTON)
        return self

    def login(self, username, password):
        """Realiza el flujo completo de login."""
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()

    def get_error_message(self):
        """Retorna el texto del mensaje de error si está visible."""
        return self.get_text(*self.ERROR_MESSAGE)

    def is_error_displayed(self):
        """Verifica si el mensaje de error está visible."""
        return self.is_element_visible(*self.ERROR_MESSAGE)
