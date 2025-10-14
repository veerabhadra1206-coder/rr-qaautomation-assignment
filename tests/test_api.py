import requests
import pytest
from utils.logger import get_logger


logger = get_logger()
# API Details
BASE_URL = "https://api.themoviedb.org/3/movie"
API_KEY = "add494e96808c55b3ee7f940c9d5e5b6"
CATEGORIES = ["popular", "top_rated", "now_playing"]
START_YEAR = 1900
END_YEAR = 2025
PAGE_NUMBER = 2
params = {
    "sort_by": "popularity.desc",
    "release_date.gte": f"{START_YEAR}-01-01",
    "release_date.lte": f"{END_YEAR}-12-31",
    "vote_average.gte": 5,
    "vote_average.lte": 5,
    "page": f"{PAGE_NUMBER}",
    "api_key": API_KEY
}

# API Test: Category
@pytest.mark.parametrize("category", CATEGORIES)
def test_api_category(category):
    url = f"{BASE_URL}/{category}?page=1&api_key={API_KEY}"

    try:
        logger.info(f"==== Starting API Test for Category: {category} ====")
        logger.info(f"Step 1: Sending GET request to {url}")
        response = requests.get(url)
        logger.info(f"Response Code: {response.status_code}")

        assert response.status_code == 200, f"Failed API call for {category}"

        logger.info("Step 2: Parsing JSON response")
        data = response.json()

        logger.info("Step 3: Validating presence of 'results' key")
        assert "results" in data, "'results' key missing in response"

        movies = data["results"]
        logger.info(f"Step 4: Number of movies returned: {len(movies)}")
        assert len(movies) > 0, "No movies found in response"

        logger.info("Step 5: Validating fields for first 5 movies")
        for i, movie in enumerate(movies[:5]):
            title = movie.get("title")
            logger.info(f"Validating Movie {i+1}: {title}")
            assert "title" in movie, "'title' missing"
            assert "release_date" in movie, "'release_date' missing"
            assert "vote_average" in movie, "'vote_average' missing"
            assert "id" in movie, "'id' missing"

        logger.info(f"==== API Test Passed for '{category}' ====")

    except AssertionError as e:
        logger.error(f"Assertion failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


#  API Test: Rating Filter
def test_api_rating():
    params = {
        "sort_by": "popularity.desc",
        "release_date.gte": "1900-01-01",
        "release_date.lte": "2025-12-31",
        "vote_average.gte": 5,
        "vote_average.lte": 5,
        "page": 1,
        "api_key": API_KEY
    }

    try:
        logger.info("==== Starting API Test for Rating Filter ====")
        response = requests.get("https://api.themoviedb.org/3/discover/movie", params=params)
        logger.info(f"Request URL: {response.url}")
        logger.info(f"Response Status: {response.status_code}")

        assert response.status_code == 200, "API did not return 200 OK"

        data = response.json()
        expected_keys = ["page", "results", "total_pages", "total_results"]

        for key in expected_keys:
            assert key in data, f"'{key}' not found in response"

        results = data.get("results", [])
        logger.info(f"Total Movies Returned: {len(results)}")

        for movie in results:
            title = movie.get("title", "N/A")
            vote = movie.get("vote_average", 0)
            logger.info(f"Movie: {title} | Vote: {vote}")
            assert vote <= 5, f"{title} has vote_average > 5"

        logger.info("==== API Test Passed for Rating Filter ====\n")

    except AssertionError as e:
        logger.error(f"Assertion failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


# API Test: Year filter
@pytest.mark.parametrize("start_year,end_year", [(2000, 2010), (2015, 2025)])
def test_api_year_range(start_year, end_year):
    yearparams = {
        "sort_by": "popularity.desc",
        "release_date.gte": f"{start_year}-01-01",
        "release_date.lte": f"{end_year}-12-31",
        "vote_average.gte": 0,
        "vote_average.lte": 5,
        "page": 1,
        "api_key": API_KEY
    }

    try:
        logger.info(f"==== Starting Year Range Test: {start_year}-{end_year} ====")
        response = requests.get("https://api.themoviedb.org/3/discover/movie", params=yearparams)
        logger.info(f"Request URL: {response.url}")
        logger.info(f"Response Status: {response.status_code}")
        assert response.status_code == 200, "did not return 200 OK"

        data = response.json()
        results = data.get("results", [])
        logger.info(f"Movies Found: {len(results)}")

        for movie in results:
            release_date = movie.get("release_date", "0000-00-00")
            release_year = int(release_date.split("-")[0])
            assert start_year <= release_year <= end_year, f"({release_year}) is not in range"

        logger.info(f"==== API Year Range Test Passed for {start_year}-{end_year} ====\n")

    except AssertionError as e:
        logger.error(f"Assertion failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

# API Test: Pagination
@pytest.mark.parametrize("page_number", [1, 2, 3, 4])
def test_api_pagination(page_number):
    url = f"{BASE_URL}/popular?page={page_number}&api_key={API_KEY}"

    try:
        logger.info(f"==== Starting Pagination Test for Page {page_number} ====")
        logger.info(f"Step 1: Sending GET request → {url}")

        response = requests.get(url)
        logger.info(f"Step 2: Response Status Code → {response.status_code}")
        assert response.status_code == 200, f"did not return 200 OK {page_number}"

        data = response.json()
        logger.info("Step 3: Validating 'results' in response JSON")
        assert "results" in data, "'results' key missing in response"

        logger.info(f"==== Pagination Test Passed for Page {page_number} ====\n")

    except AssertionError as e:
        logger.error(f"Assertion failed: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise