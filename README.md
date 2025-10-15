# RR – QA Automation Assignment
--veerabhadra--

## **Description**
This project is a hybrid test automation framework for a movie and TV show listing platform, covering both UI and API testing. It uses keyword-driven, data-driven, and Page Object Model (POM) strategies, with integrated logging and screenshots, to deliver scalable, maintainable, and reusable tests suitable for CI/CD pipelines.
This assignment showcases my skills in UI and API test automation using Python, Selenium, and Pytest.  
The target demo website is: https://tmdb-discover.surge.sh/

---

## **Assignment Scope**

1. **Filtering Options**
   - **Categories:** Popular, Trending, Newest, Top Rated  
   - **Titles**  
   - **Type:** Movies or TV Shows  
   - **Year of Release:** Using start and end year  
   - **Rating:** Star rating filter  
   - **Genre:** E.g., Action  

2. **Pagination**
   - Navigate through pages  
   - Validate movie titles load correctly  

3. **Negative / Known Issues**
   - Refreshing/accessing pages with specific slugs may fail  
   - Last few pagination pages may not function  

---


## **🔹 UI Test Cases**

| Test Case | Test Function | Steps | Expected Result |
|----------------|------------------|------------|---------------------|
| Category Filter | `test_category_filter` | 1. Open Home Page.<br>2. Click on a category.<br>3. Wait for movie titles to load.<br>4. Check URL and UI updates. | URL updates with category slug.<br>Movie titles are displayed correctly. |
| Type Filter | `test_type_filter` | 1. Open “Type” dropdown.<br>2. Select Movie/TV Show.<br>3. Wait for UI update.<br>4. Verify selection. | Dropdown shows the selected type. |
| Year Range Filter | `test_year_range_filter` | 1. Select start and end year.<br>2. Validate selected range on screen. | Displayed movies fall within selected year range. |
| Star Rating Filter | `test_star_rating` | 1. Select a star rating (1–5).<br>2. Wait for star to activate.<br>3. Validate selected rating. | Selected star is active.<br>Movies are filtered by rating. |
| Genre Filter | `test_genre_filter` | 1. Open Genre dropdown.<br>2. Select a genre - Action.<br>3. Verify dropdown value. | Selected genre appears correctly in dropdown. |
| Pagination | `test_pagination` | 1. Wait for pagination to appear.<br>2. Click “Next Page”.<br>3. Verify active page number. | Next page loads and displays movie titles. |
| Category Page Refresh | `test_refresh_category` | 1. Open category page.<br>2. Refresh the page.<br>3. Verify movie titles reload. | Movies reload successfully after refresh. |
| Broken Pages Check | `test_broken_pages` | 1. Fetch last 3 pagination pages.<br>2. Open each page.<br>3. Verify movie titles. | No missing or empty movie titles on last pages. |

---

## ** API Test Cases**

| **Test Case** | **Test Function name** | **Steps** | **Expected Result** |
|----------------|------------------|------------|---------------------|
| Category API | `test_api_category` | 1. Send GET request to `/movie/{category}`.<br>2. Parse JSON response.<br>3. Validate fields. | Status 200 OK.<br>Response contains `results`.<br>Each movie has `title`, `release_date`, `vote_average`, and `id`. |
| Rating Filter API | `test_api_rating` | 1. Send GET request with `vote_average.gte` and `.lte` filters.<br>2. Parse response.<br>3. Validate votes. | Status 200 OK.<br>All returned movies have `vote_average ≤ 5`. |
| Year Range API | `test_api_year_range` | 1. Send GET request with `release_date.gte` and `.lte` params.<br>2. Parse response.<br>3. Validate release years. | Status 200 OK.<br>Movies fall within the selected year range. |
| Pagination API | `test_api_pagination` | 1. Send GET request with `page` parameter.<br>2. Parse response. | Status 200 OK.<br>Data corresponds to the requested page number. |

---

### Features Implemented
- All tests are written using **Pytest**.  
- UI tests use **Selenium WebDriver** for browser automation.  
- API tests use **Requests** for API validation.  
- Fully automated tests for **UI filters** and **pagination**  
- **API tests** for categories, rating, year range, and pagination
- Configurable test data stored in `utils/test_data.py`  
- Config file (`utils/config.py`) for base URL, waits, browser, and paths   
- **Logging** implemented with `logging` module in `utils/logger.py` (info, step, error logs)
- Each test includes detailed logging for every step and validation. 
- Screenshots captured **on failures** and attached to HTML report  
 

**Test Execution Command Example:**
```bash
pytest --html=reports/report.html --self-contained-html
```

### **3. Logging**

- Logs stored in **console** and file (/logs/automation)  
- Logs include:
  - Test start/end  
  - Step execution   
  - API responses  
  - Errors / assertion failures  


### **6. Defects Found**
- Refreshing category URLs fails  
- Pagination works for first few pages; last few pages (broken) are not showing any movie titles  

---

### **7. CI/CD Integration Approach**

1. **GitHub Actions** pipeline  
2. Steps:
   - Install Python dependencies (`requirements.txt`)  
   - Run Pytest tests  
   - Generate HTML report and save artifacts       

**GitHub Actions YAML snippet:**
```yaml
name: Run UI + API Tests for rr

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  test:
    runs-on: windows-latest

    steps:
      # Checkout repo
      - name: Checkout Repository
        uses: actions/checkout@v4

      # Setup Python
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      # Installing dependencies
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest-html

      - name: Run Tests and Generate HTML Report
        run: |
          mkdir -p reports
          pytest --html=reports/report.html --self-contained-html 
        continue-on-error: true
  
      - name: Upload HTML Report
        uses: actions/upload-artifact@v4
        with:
          name: pytest-html-report
          path: reports/

```





