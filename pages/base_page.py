from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def find_element(self, by, locator):
        #Espera elemento visible
        return self.wait.until(EC.visibility_of_element_located((by, locator)))

    def click(self, by, locator):
        #Espera elemento clickeable
        element = self.wait.until(EC.element_to_be_clickable((by, locator)))
        element.click()

    def send_keys(self, by, locator, text):
       
        element = self.find_element(by, locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, by, locator):
       
        return self.find_element(by, locator).text

    def is_element_visible(self, by, locator):
        
        try:
            self.wait.until(EC.visibility_of_element_located((by, locator)))
            return True
        except Exception:
            return False

    def get_current_url(self):
       
        return self.driver.current_url
