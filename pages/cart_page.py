

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CartPage(BasePage):
    
    # --- Localizadores ---
    PAGE_TITLE        = (By.CLASS_NAME, "title")
    CART_ITEMS        = (By.CLASS_NAME, "cart_item")
    ITEM_NAMES        = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON   = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def get_page_title(self):
        "Retorna el título de la página del carrito."
        return self.get_text(*self.PAGE_TITLE)

    def get_cart_items(self):
        "Retorna la lista de elementos del carrito."
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_item_count(self):
        "Retorna la cantidad de ítems en el carrito."
        return len(self.get_cart_items())

    def get_item_names(self):
        "Retorna una lista con los nombres de los productos en el carrito."
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def click_checkout(self):
        "Hace click en el botón de Checkout."
        self.click(*self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
        "Hace click en 'Continue Shopping' para volver al inventario."""
        self.click(*self.CONTINUE_SHOPPING)
