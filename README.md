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

## **Test Strategy**

### **1. UI test cases**

| Test Case | Steps | Expected Result |
|-----------|-------|----------------|
| Category Filter | 1. Open Home Page <br> 2. Click on a category <br> 3. Wait for titles to load | URL contains category slug, movie titles displayed |
| Type Filter | 1. Open Type dropdown <br> 2. Select Movie/TV Show <br> 3. Validate selection | Dropdown shows selected type |
| Year Range Filter | 1. Select start and end year <br> 2. Validate UI shows selected range | Displayed movies are within the year range |
| Star Rating Filter | 1. Select a star rating <br> 2. Validate selected star | Movies are filtered based on rating |
| Genre Filter | 1. Open Genre dropdown <br> 2. Select Action <br> 3. Validate UI | Dropdown shows selected genre |
| Pagination | 1. Wait for pagination <br> 2. Click next page <br> 3. Verify page number | Movies titles for next page are displayed |
| Category Page Refresh | 1. Open category URL <br> 2. Refresh page <br> 3. Validate movie titles | Titles reload successfully |
| Broken Pages Check | 1. Navigate last 3 pages <br> 2. Verify movie titles | No missing movie titles |

## **1. UI test cases**

| Test Case | Steps | Expected Result |
|-----------|-------|----------------|
| Category API  | 1. Send GET request to /movie/{category}<br>2. Parse response<br>3. Validate fields  | Status code is 200.<br>Response JSON contains 'results'.<br>Each result has title, id. |
| Rating Filter API  | 1. Send GET request with vote_average.gte parameter<br>2. Parse response  | Status code is 200.<br>All returned items have vote_average at/above the parameter value.|
| Year Range API  | 1. Send GET with release_date.gte and .lte params<br>2. Parse response  | Status code is 200.<br>All listed movies are within the specified year range.|
| Pagination API | 1. Send GET request with page parameter<br>2. Parse response  | Status code is 200.<br>Returned data corresponds to the requested page.|


### **2. Test Suite Implementation**

**Technologies / Libraries Used:**
- **Python** – Test scripts  
- **Selenium** – Web UI automation  
- **Pytest** – Test runner  
- **pytest-html** – HTML report generation with screenshots  
- **Requests** – API testing  

**Features Implemented:**
- Fully automated tests for **UI filters** and **pagination**  
- **API tests** for categories, rating, year range, and pagination  
- **Logging** implemented with `logging` module (info, step, error logs)  
- Screenshots captured **on failures** and attached to HTML report  
- Configurable test data stored in `utils/test_data.py`  
- Config file (`utils/config.py`) for base URL, waits, browser, and paths  

**Test Execution Command Example:**
```bash
pytest --html=reports/report.html --self-contained-html
```

---

### **3. Logging**

- Logs stored in **console** and file (/logs/automation)  
- Logs include:
  - Test start/end  
  - Step execution  
  - Selected filters  
  - API responses  
  - Errors / assertion failures  


### **6. Defects Found**
- Refreshing category URLs sometimes fails  
- Pagination works for first few pages; last few pages may not display movies  

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





