from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils.config import EXPLICIT_WAIT
from selenium.webdriver.support import expected_conditions as EC
from utils.logger import get_logger

logger = get_logger(__name__)
class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)
        self.logger = get_logger(self.__class__.__name__)
    # Locators
    CATEGORY_FILTER = (By.XPATH, "//nav//ul/li/a")
    MOVIE_TITLES = (By.XPATH, "//div[contains(@class,'flex flex-col items-center')]/p[1]")
    MOVIE_META = (By.XPATH, "//div[contains(@class,'flex flex-col items-center')]/p[2]")
    TYPE_DROPDOWN = (By.XPATH, "(//p[text()='Type']/following::div[contains(@class,'css-yk16xz-control')])[1]")
    SELECTED_TYPE = (By.XPATH, "//div[contains(@class,'css-1uccc91-singleValue')]")
    GENRE_DROPDOWN = (By.XPATH, "(//p[text()='Genre']/following::div[contains(@class,'css-yk16xz-control')])[1]")
    SELECTED_GENRE = (By.XPATH, "//div[contains(@class,'css-12jo7m5')]")
    YEAR_START_DROPDOWN = (By.XPATH, "(//div[contains(@class,'css-1hwfws3')])[3]")
    YEAR_END_DROPDOWN = (By.XPATH, "(//div[contains(@class,'css-1hwfws3')])[4]")
    RATING_STARS = (By.XPATH, "(//ul[contains(@class,'rc-rate')]//div[@role='radio' and @aria-posinset='4'])")
    PAGINATION = (By.ID, "react-paginate")
    NEXT_BUTTON = (By.XPATH, "//li[contains(@class,'next')]/a")
    SELECTED_PAGE = (By.XPATH, "//li[@class='selected']/a")

    # Actions
    def select_category(self, category_name):
        try:
            self.logger.info(f"Selecting category: {category_name}")
            self.wait.until(EC.presence_of_all_elements_located(self.CATEGORY_FILTER))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//nav//ul/li/a[text()='{category_name}']"))).click()
            self.logger.info(f"Clicked on category: {category_name}")
        except Exception as e:
            self.logger.error(f"Error selecting category '{category_name}': {e}")
            raise

    # Return all visible movie titles
    def get_all_titles(self):

        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(self.MOVIE_TITLES))
            titles = [el.text.strip() for el in elements if el.text.strip()]
            self.logger.info(f"Found {len(titles)} movie titles: {titles[:5]} ...")
            return titles
        except Exception as e:
            self.logger.error(f"Error getting titles: {e}")
            return []

    # Select from Type dropdown (Movie/TV Shows)
    def select_type(self, type_name):
        try:
            self.wait.until(EC.element_to_be_clickable(self.TYPE_DROPDOWN)).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{type_name}']"))).click()
            self.logger.info(f"Selected type: {type_name}")
        except Exception as e:
            self.logger.error(f"Error selecting type '{type_name}': {e}")
            raise

    # Get currently selected type value
    def get_selected_type(self):
        try:
            selected = self.wait.until(EC.visibility_of_element_located(self.SELECTED_TYPE)).text
            self.logger.info(f"Currently selected type: {selected}")
            return selected
        except Exception as e:
            self.logger.error(f"Error getting selected type: {e}")
            return None
    # Select start and end year
    def select_year_range(self, start_year, end_year):
        try:
            self.wait.until(EC.element_to_be_clickable(self.YEAR_START_DROPDOWN)).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{start_year}']"))).click()
            self.wait.until(EC.element_to_be_clickable(self.YEAR_END_DROPDOWN)).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, f"//div[text()='{end_year}']"))).click()
            self.logger.info(f"Year range selected: {start_year}-{end_year}")
        except Exception as e:
            self.logger.error(f"Error selecting year range: {e}")
            raise

    def get_selected_start_year(self):
        try:
            year_text = self.wait.until(EC.visibility_of_element_located(self.YEAR_START_DROPDOWN)).text
            year = int(year_text)
            self.logger.info(f"Selected start year: {year}")
            return year
        except Exception as e:
            self.logger.error(f"Error getting selected start year: {e}")
            return None

    def get_selected_end_year(self):
        try:
            year_text = self.wait.until(EC.visibility_of_element_located(self.YEAR_END_DROPDOWN)).text
            year = int(year_text)
            self.logger.info(f"Selected end year: {year}")
            return year
        except Exception as e:
            self.logger.error(f"Error getting selected end year: {e}")
            return None

    # Extract years from movie info
    def get_displayed_years(self):
        try:
            items = self.driver.find_elements(*self.MOVIE_META)
            years = [i.text.split(",")[-1].strip() for i in items if "," in i.text]
            self.logger.info(f"Extracted years: {years[:5]} ...")
            return years
        except Exception as e:
            self.logger.error(f"Error extracting years: {e}")
            return []

    # Selecting genre from dropdown
    def select_genre(self, genre_name):
        try:
            # Open dropdown
            self.wait.until(EC.element_to_be_clickable(self.GENRE_DROPDOWN)).click()

            # Click the desired genre
            option = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//div[text()='{genre_name}']"))
            )
            option.click()
            self.logger.info(f"Selected genre: {genre_name}")

        except Exception as e:
            self.logger.error(f"Error selecting genre '{genre_name}': {e}")
            raise

    # getting genres of each movie displayed on the page
    def get_displayed_genres(self):
        try:
            elements = self.driver.find_elements(*self.MOVIE_META)
            genres = [el.text.split(",")[0].strip() for el in elements if el.text.strip()]
            self.logger.info(f"Extracted genres: {genres[:5]} ...")
            return genres
        except Exception as e:
            self.logger.error(f"Error extracting genres: {e}")
            return []
    # Click a specific star rating
    def select_rating(self, stars):
        try:
            star = self.wait.until(EC.presence_of_element_located((
                By.XPATH,
                f"(//ul[contains(@class,'rc-rate')]//div[@role='radio' and @aria-posinset='{stars}'])"
            )))
            star.click()
            self.logger.info(f"Selected rating: {stars} stars")
            return star
        except Exception as e:
            self.logger.error(f"Error selecting rating '{stars}': {e}")
            raise

    # Wait until pagination component is visible
    def wait_for_pagination(self):
        try:
            self.wait.until(EC.presence_of_element_located(self.PAGINATION))
            self.logger.info("Pagination is visible.")
        except Exception as e:
            self.logger.error(f"Error waiting for pagination: {e}")
            raise

    # Click on the next page button
    def click_next_page(self):
        try:
            next_button = self.wait.until(EC.element_to_be_clickable(self.NEXT_BUTTON))
            next_button.click()
            self.logger.info("Clicked next page button.")
        except Exception as e:
            self.logger.error(f"Error clicking next page button: {e}")
            raise

    # Return the number of the currently selected page
    def get_selected_page_number(self):
        try:
            selected = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(self.SELECTED_PAGE)
            )
            page_number = selected.text.strip()
            self.logger.info(f"Currently selected page: {page_number}")
            return page_number
        except Exception as e:
            self.logger.error(f"Error getting selected page number: {e}")
            return None
    def select_page(self, page_number):
        try:
            page_link = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//li/a[text()='{page_number}']")))
            page_link.click()
            self.logger.info(f"Selected page: {page_number}")
        except Exception as e:
            self.logger.error(f"Error selecting page: {e}")


