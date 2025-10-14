import pytest
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from pages.home_page import HomePage
from utils.config import BASE_URL
from utils.test_data import CATEGORY_DATA, TYPE_DATA, YEAR_RANGE_DATA, GENRE_NAME
import time

logger = logging.getLogger(__name__)

# Verify filtering by categories and correct URL redirection
@pytest.mark.parametrize("category,slug", CATEGORY_DATA.items())
def test_category_filter(driver, category, slug):
    home = HomePage(driver)
    logger.info("  Starting Category Filter Test  ")
    try:
        logger.info(f"Step 1: Selecting category → {category}")
        home.select_category(category)

        logger.info("Step 2: Waiting for page elements to load")
        WebDriverWait(driver, 10).until(EC.visibility_of_any_elements_located(home.MOVIE_TITLES))
        logger.info(f"Elements loaded successfully for '{category}'")

        logger.info("Step 3: Validating URL update")
        current_url = driver.current_url
        expected_url = f"/{slug}"
        logger.info(f"Current URL: {current_url}")
        assert expected_url in current_url, f"Expected '{expected_url}' in URL"

        logger.info("Step 4: Verifying movie titles are displayed")
        titles = home.get_all_titles()
        logger.info(f"Titles displayed for '{category}': {titles}")
        assert titles, f"No titles found for '{category}'"

        logger.info(f"  Category Filter Test Passed for '{category}'  ")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Category Filter Test Failed for '{category}': {e}")
        raise


@pytest.mark.parametrize("type_name", TYPE_DATA)
def test_type_filter(driver, type_name):
    home = HomePage(driver)
    logger.info("  Starting Type Dropdown Filter Test  ")
    try:
        logger.info(f"Step 1: Selecting type: {type_name}")
        home.select_type(type_name)

        logger.info("Step 2: Waiting for dropdown value to update")
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, "//div[contains(@class,'css-1uccc91-singleValue')]"),
                type_name
            )
        )

        logger.info("Step 3: Validating selected type from UI")
        selected_type = home.get_selected_type()
        logger.info(f"Selected type: {selected_type}")
        assert selected_type.lower() == type_name.lower(), f"Expected '{type_name}', got '{selected_type}'"

        logger.info(f"  Type Dropdown Filter Test Passed for '{type_name}'  ")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Type Dropdown Filter Test Failed for '{type_name}': {e}")
        raise


@pytest.mark.parametrize("start_year,end_year", YEAR_RANGE_DATA)
def test_year_range_filter(driver, start_year, end_year):
    home = HomePage(driver)
    logger.info("  Starting Year Range Filter Test  ")
    try:
        logger.info(f"Step 1: Selecting year range: start_year: {end_year}")
        home.select_year_range(start_year, end_year)

        logger.info("Step 2: Verifying selected years in UI")
        selected_start = home.get_selected_start_year()
        selected_end = home.get_selected_end_year()
        logger.info(f"UI shows: {selected_start} - {selected_end}")

        assert selected_start == start_year
        assert selected_end == end_year

        # logger.info("Step 3: Verifying all displayed movies fall in range")
        # years = home.get_displayed_years()
        # for year in years:
        #     assert start_year <= int(year) <= end_year, f"Movie year {year} not in range"
        # logger.info(f"Displayed years: {years}")

        logger.info(f"  Year Range Filter Test Passed ({start_year}-{end_year})  ")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Year Range Filter Test Failed ({start_year}-{end_year}): {e}")
        raise


@pytest.mark.parametrize("star_count", [1, 2])
def test_star_rating(driver, star_count):
    home = HomePage(driver)
    logger.info("  Starting Star Rating Filter Test  ")
    try:
        logger.info(f"Step 1: Selecting {star_count}-star rating")
        home.select_rating(star_count)

        logger.info("Step 2: Waiting for selected star to be active")
        selected_star_locator = (By.XPATH, f"(//ul[contains(@class,'rc-rate')]//div[@role='radio' and @aria-posinset='{star_count}'])")
        WebDriverWait(driver, 10).until(
            EC.element_attribute_to_include(selected_star_locator, "aria-checked")
        )

        logger.info("Step 3: Verifying star rating is selected")
        selected_star = driver.find_element(*selected_star_locator)
        is_checked = selected_star.get_attribute("aria-checked") == "true"
        assert is_checked, f"{star_count}-star rating not selected"

        logger.info(f"  {star_count}-Star Rating Filter Test Passed  ")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Star Rating Filter Test Failed ({star_count} stars): {e}")
        raise


def test_genre_filter(driver):
    home = HomePage(driver)
    logger.info("  Starting Genre Filter Test  ")
    try:
        logger.info(f"Step 1: Selecting genre: {GENRE_NAME}")
        home.select_genre(GENRE_NAME)

        logger.info("Step 2: Verify the selected genre appears in the filter dropdown")
        selected_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(home.SELECTED_GENRE)
        )
        selected = selected_element.text
        assert GENRE_NAME.lower() == selected.lower(), f"Dropdown shows '{selected}' but expected '{GENRE_NAME}'"
        logger.info(f"Genre '{GENRE_NAME}' correctly displayed in dropdown.")

        logger.info(f"Genre Filter Test Passed for '{GENRE_NAME}'")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Genre Filter Test Failed for '{GENRE_NAME}': {e}")
        raise



@pytest.mark.pagination
def test_pagination(driver):
    logger.info("  Starting Pagination Test  ")
    home = HomePage(driver)
    try:
        logger.info("Step 2: Waiting for pagination to be visible")
        home.wait_for_pagination()

        logger.info("Step 3: Clicking on next page button")
        home.click_next_page()

        logger.info("Step 4: Verifying that Page 2 is selected")
        selected_page = home.get_selected_page_number()
        logger.info(f"Selected page displayed: {selected_page}")
        assert selected_page == "2", f"Expected page '2' but found '{selected_page}'"

        logger.info("  Pagination Test Passed Successfully  ")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Pagination Test Failed: {e}")
        raise


# Category Page Refresh
@pytest.mark.parametrize("slug_name, slug_url", CATEGORY_DATA.items())
def test_refresh_category(driver, slug_name, slug_url):
    home = HomePage(driver)
    url = f"{BASE_URL}/{slug_url}"
    logger.info("  Starting Category Page Refresh Test  ")
    try:
        logger.info(f"Step 1: Opening category page → {slug_name} : {url}")
        driver.get(url)

        logger.info("Step 2: Waiting for movies to load")
        titles = (WebDriverWait(driver, 10).until
                  (EC.presence_of_all_elements_located( (By.XPATH,
                "//div[contains(@class,'flex flex-col items-center')]//p"))
            ))
        assert titles, f"No movie titles found before refreshing category page '{slug_name}'"
        logger.info(f"Category page {slug_name} loaded successfully.")

        logger.info("Step 3: Refreshing the page and verifying movie load again")

        # refreshing page and checking
        driver.refresh()
        # waiting for elements to be located
        time.sleep(5)
        # Getting movie titles after refresh
        titles_after_refresh = home.get_all_titles()
        assert titles_after_refresh, f"No movie titles found after refreshing category page '{slug_name}'"

        logger.info(f"  Category Refresh Test Passed for '{slug_name}'  ")

    except TimeoutException as e:
        logger.error(f"Category Refresh Test Failed for '{slug_name}': {e}")
        raise

# Checking know broken pages
def test_broken_pages(driver):
    logger.info("  Starting Dynamic Broken Page Check  ")
    home = HomePage(driver)
    try:
        logger.info("Step 1: Waiting for pagination to be visible")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "react-paginate"))
        )

        logger.info("Step 2: Fetching last 3 page numbers")
        last_three_elems = driver.find_elements(
            By.XPATH,
            "(//ul/li[not(contains(@class,'next')) and not(contains(@class,'previous')) and not(contains(@class,'break'))]/a)[position() > last()-3]"
        )

        last_three_pages = [int(elem.text) for elem in last_three_elems]
        logger.info(f"Last 3 pages detected: {last_three_pages}")

        for page_num in last_three_pages:
            logger.info(f"Step 3: Clicking on page: {page_num}")
            home.select_page(page_num)

            logger.info("Step 4: Verifying movie titles are present")
            titles = home.get_all_titles()
            assert titles, f"No movie titles found on page {page_num}"
            logger.info(f"Page {page_num} Loaded Successfully ({len(titles)} movies)")

        logger.info("  Broken Page Check Passed  ")

    except (TimeoutException, NoSuchElementException, AssertionError) as e:
        logger.error(f"Broken Page Check Failed: {e}")
        raise