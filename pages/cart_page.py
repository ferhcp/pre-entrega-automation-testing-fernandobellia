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
        
        return self.get_text(*self.PAGE_TITLE)

    def get_cart_items(self):
        
        return self.driver.find_elements(*self.CART_ITEMS)

    def get_item_count(self):
  
        return len(self.get_cart_items())

    def get_item_names(self):
        
        return [el.text for el in self.driver.find_elements(*self.ITEM_NAMES)]

    def click_checkout(self):
        
        self.click(*self.CHECKOUT_BUTTON)

    def click_continue_shopping(self):
       
        self.click(*self.CONTINUE_SHOPPING)



    def get_first_item_name(self):
     
        items = self.driver.find_elements(*self.ITEM_NAMES)
        if not items:
            return ""
        return items[0].text

    def product_is_in_cart(self, product_name):
 
        return product_name in self.get_item_names()
