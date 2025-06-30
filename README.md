# BizGrabber 1.00
A lightweight Python and executable program for gathering business information (Name, Website, E-Mail). Very easy to use.

## Overview

BizGrabber 1.00 is an automated business information extraction tool designed for efficient web scraping of relevant business data from Google Maps and individual business websites. Built in Python, it leverages web scraping, concurrent HTTP requests, and robust parsing to provide business names, URLs, and email addresses.

BizGrabber is tailored for businesses who want to analyze their competition, and researchers, marketers, investigators, and other professionals who require systematic and precise collection of business-related data within specific industries and geographic regions.

---

## Key Features

### Automated Data Extraction

* Automates retrieval of business URLs directly from Google Maps search results.
* Scrapes individual business websites to obtain pertinent information, such as business names and email contacts.

### Concurrent Processing

* Implements concurrent HTTP requests for efficient and rapid scraping.
* Utilizes multi-threading (`concurrent.futures.ThreadPoolExecutor`) to process multiple URLs simultaneously.

### Intelligent Query Generation

* Dynamically generates targeted search queries to optimize the depth and breadth of data collection.
* Queries include variations with directional terms (e.g., north, south) and proximity indicators (e.g., near, around).

### Data Validation and Cleaning

* Performs URL normalization and filtering to ensure accuracy and consistency.
* Eliminates duplicates and ensures only unique and relevant URLs are processed.

### Comprehensive Logging

* Outputs clear progress updates to the user through terminal logging.
* Generates timestamped CSV reports with structured data, enabling easy analysis and archiving.

---

## Installation

1. Clone or download the repository containing `BizGrabber 1.00.py`.

2. Ensure Python 3.9 or higher is installed.

3. Install required Python packages:

```
pip install requests beautifulsoup4 selenium webdriver-manager
```

---

## Usage
Download BizGrabber, install the dependencies, and open the script.

### Interactive Input

Upon execution, BizGrabber prompts users for:

* **Industry:** Type of businesses targeted (e.g., restaurants, lawyers).
* **City:** Targeted city for the search.
* **Region:** Broader region or state to refine the search.

BizGrabber then constructs search queries automatically and begins data extraction.

---

## Workflow Description

### Step-by-Step Breakdown

1. **Initialization**

   * Display a stylized ASCII banner, version details, and creator information.

2. **Query Generation**

   * Dynamically creates Google Maps search queries combining industry, city, region, directional terms, and proximity indicators.

3. **Google Maps Scraping**

   * Utilizes Selenium WebDriver running headlessly to automate browser-based retrieval of URLs from Google Maps searches.

4. **URL Processing and Validation**

   * Normalizes URLs by removing trailing slashes and converting to lowercase.
   * Filters URLs to exclude non-relevant links (Google Maps internal pages).

5. **Concurrent Website Scraping**

   * Initiates concurrent sessions using `requests` to scrape individual business websites.
   * Parses website content using BeautifulSoup to extract business names (from HTML title tags) and email addresses (via regex matching).

6. **Data Aggregation and CSV Output**

   * Compiles extracted information into structured records.
   * Outputs the final dataset into a timestamped CSV file located in the script's directory.

---

## Technical Specifications

* **Concurrency:** `ThreadPoolExecutor` with configurable maximum workers (`MAX_WORKERS = 20`).
* **HTTP Request Timeout:** 60 seconds (`REQUEST_TIMEOUT`).
* **Data Handling:** CSV file format with columns: `Business Name`, `URL`, and `Email`.

---

## Output

BizGrabber generates a CSV file with the following structure:

```
Business Name,URL,Email
Example Business,http://example.com,contact@example.com
```

The filename includes a precise timestamp to prevent overwrites and facilitate organized data management.

---

## Example Use Case

```
Enter industry: dental
Enter city: Ottawa
Enter region: Ontario

Searching...
Generated 35 record(s) → /path/to/web-extraction-20250630-093200.csv
```

---

## Limitations and Considerations

* Google Maps and websites may implement anti-scraping measures or rate limits, potentially impacting performance.
* Accuracy of email extraction depends on the quality and structure of the websites scraped.
* Headless browser operations (Selenium) may require updates or maintenance based on Google Maps' interface changes.

---

## Future Enhancements

* Integration of proxy rotation and CAPTCHA-solving capabilities to enhance scraping robustness.
* Expansion to include additional business information, such as phone numbers, addresses, and reviews.
* GUI implementation for improved user interaction and real-time progress visualization.

---

## Disclaimer

BizGrabber should be used ethically and in compliance with applicable laws, regulations, and terms of service. The developer, Joshua M Clatney, is not liable for misuse or illegal activities conducted using this tool.

---

### Author Information

**Joshua M Clatney (Clats97)**

Ethical Pentesting Enthusiast

Copyright © 2024-2025 Joshua M Clatney (Clats97) All Rights Reserved

### Disclaimer

**DISCLAIMER: This project comes with no warranty, express or implied. The author is not responsible for abuse, misuse, or vulnerabilities. Please use responsibly and ethically in accordance with relevant laws, regulations, legislation and best practices.**
