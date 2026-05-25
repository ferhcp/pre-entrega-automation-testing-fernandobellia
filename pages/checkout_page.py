

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
 

    # ── Localizadores ────────────────────────────────────────────────────────
    PAGE_TITLE      = (By.CLASS_NAME, "title")
    FIRST_NAME      = (By.ID, "first-name")
    LAST_NAME       = (By.ID, "last-name")
    POSTAL_CODE     = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    CANCEL_BUTTON   = (By.ID, "cancel")
    ERROR_MESSAGE   = (By.CSS_SELECTOR, "[data-test='error']")

    def get_page_title(self):
        
        return self.get_text(*self.PAGE_TITLE)

    def fill_information(self, first_name, last_name, postal_code):
  
        self.send_keys(*self.FIRST_NAME, first_name)
        self.send_keys(*self.LAST_NAME, last_name)
        self.send_keys(*self.POSTAL_CODE, postal_code)
        return self

    def click_continue(self):
      
        self.click(*self.CONTINUE_BUTTON)

    def click_cancel(self):
       
        self.click(*self.CANCEL_BUTTON)

    def get_error_message(self):
       
        return self.get_text(*self.ERROR_MESSAGE)

    def is_error_displayed(self):
        
        return self.is_element_visible(*self.ERROR_MESSAGE)


class CheckoutOverviewPage(BasePage):
 

    # ── Localizadores ────────────────────────────────────────────────────────
    PAGE_TITLE      = (By.CLASS_NAME, "title")
    FINISH_BUTTON   = (By.ID, "finish")
    CANCEL_BUTTON   = (By.ID, "cancel")
    ITEM_TOTAL      = (By.CLASS_NAME, "summary_subtotal_label")
    TAX_LABEL       = (By.CLASS_NAME, "summary_tax_label")
    TOTAL           = (By.CLASS_NAME, "summary_total_label")
    CART_ITEMS      = (By.CLASS_NAME, "cart_item")

    def get_page_title(self):
      
        return self.get_text(*self.PAGE_TITLE)

    def get_item_total(self):
      
        return self.get_text(*self.ITEM_TOTAL)

    def get_tax(self):
      
        return self.get_text(*self.TAX_LABEL)

    def get_total(self):
     
        return self.get_text(*self.TOTAL)

    def get_item_count(self):
      
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def click_finish(self):
       
        self.click(*self.FINISH_BUTTON)

    def click_cancel(self):
       
        self.click(*self.CANCEL_BUTTON)


class CheckoutCompletePage(BasePage):


    # Localizadores 
    PAGE_TITLE        = (By.CLASS_NAME, "title")
    COMPLETE_HEADER   = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT     = (By.CLASS_NAME, "complete-text")
    PONY_IMAGE        = (By.CLASS_NAME, "pony_express")
    BACK_HOME_BUTTON  = (By.ID, "back-to-products")

    def get_page_title(self):
      
        return self.get_text(*self.PAGE_TITLE)

    def get_complete_header(self):
        
        
        return self.get_text(*self.COMPLETE_HEADER)

    def get_complete_text(self):
     
        return self.get_text(*self.COMPLETE_TEXT)

    def is_order_complete(self):
       
        return self.is_element_visible(*self.COMPLETE_HEADER)

    def is_pony_image_visible(self):
      
        return self.is_element_visible(*self.PONY_IMAGE)

    def click_back_home(self):
       
        self.click(*self.BACK_HOME_BUTTON)
