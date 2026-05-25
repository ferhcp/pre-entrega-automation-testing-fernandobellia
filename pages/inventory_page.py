

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Representa la página de productos: /inventory.html"""

    # --- Localizadores ---
    PAGE_TITLE           = (By.CLASS_NAME, "title")
    PRODUCT_ITEMS        = (By.CLASS_NAME, "inventory_item")
    CART_BADGE           = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK            = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN        = (By.CLASS_NAME, "product_sort_container")
    BURGER_MENU          = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK          = (By.ID, "logout_sidebar_link")

    # Segundo commit — localizadores para el primer producto de la lista
    FIRST_PRODUCT_NAME   = (By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_name")
    FIRST_PRODUCT_PRICE  = (By.CSS_SELECTOR, ".inventory_item:first-child .inventory_item_price")

    def get_page_title(self):
     
        return self.get_text(*self.PAGE_TITLE)

    def add_product_to_cart(self, product_name):
 
        # Convierte el nombre a formato de ID: "Sauce Labs Backpack" → "sauce-labs-backpack"
        product_id = product_name.lower().replace(" ", "-")
        add_button_locator = (By.CSS_SELECTOR, f"[data-test='add-to-cart-{product_id}']")
        self.click(*add_button_locator)
        return self

    def remove_product_from_cart(self, product_name):
  
        product_id = product_name.lower().replace(" ", "-")
        remove_button_locator = (By.CSS_SELECTOR, f"[data-test='remove-{product_id}']")
        self.click(*remove_button_locator)
        return self

    def get_cart_count(self):

        if self.is_element_visible(*self.CART_BADGE):
            return int(self.get_text(*self.CART_BADGE))
        return 0

    def go_to_cart(self):
  
        self.click(*self.CART_LINK)

    def get_product_count(self):
  
        return len(self.driver.find_elements(*self.PRODUCT_ITEMS))

    def logout(self):
   
        self.click(*self.BURGER_MENU)
        self.click(*self.LOGOUT_LINK)

    # ── Segundo commit — métodos para Navegación y Verificación del Catálogo ──

    def get_first_product_name(self):

        return self.get_text(*self.FIRST_PRODUCT_NAME)

    def get_first_product_price(self):

        return self.get_text(*self.FIRST_PRODUCT_PRICE)

    def is_sort_dropdown_visible(self):
    
        return self.is_element_visible(*self.SORT_DROPDOWN)

    def is_burger_menu_visible(self):
   
        return self.is_element_visible(*self.BURGER_MENU)

    def is_cart_icon_visible(self):

        return self.is_element_visible(*self.CART_LINK)
