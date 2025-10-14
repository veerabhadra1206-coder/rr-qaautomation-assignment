from selenium.webdriver.support.ui import WebDriverWait
from utils.config import EXPLICIT_WAIT
from utils.logger import get_logger

logger = get_logger(__name__)


class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = get_logger(self.__class__.__name__)
