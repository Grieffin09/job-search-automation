import logging
from selenium import webdriver
from selenium.common import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_driver():
    """Set up and return a Selenium WebDriver instance."""
    options = Options()
    options.headless = True  # Run in headless mode for better performance
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    return driver

def extract_jobs(driver):
    """Extract job details from the current page."""
    job_listings = driver.find_elements(By.CSS_SELECTOR, "div.srp-jobtuple-wrapper")
    jobs = []
    for job in job_listings:
        job_data = {}

        # Extract job title
        job_title_element = job.find_elements(By.CSS_SELECTOR, "a.title")
        job_data["job_title"] = job_title_element[0].text if job_title_element else "N/A"

        # Extract company name
        company_name_element = job.find_elements(By.CSS_SELECTOR, "a.comp-name")
        job_data["company_name"] = company_name_element[0].text if company_name_element else "N/A"

        # Extract experience
        experience_element = job.find_elements(By.CSS_SELECTOR, "span.expwdth")
        job_data["experience"] = experience_element[0].text if experience_element else "N/A"

        # Extract salary
        salary_element = job.find_elements(By.CSS_SELECTOR, "span.sal")
        job_data["salary"] = salary_element[0].text if salary_element else "N/A"

        # Extract location
        location_element = job.find_elements(By.CSS_SELECTOR, "span.locWdth")
        job_data["location"] = location_element[0].text if location_element else "N/A"

        # Extract job description
        job_description_element = job.find_elements(By.CSS_SELECTOR, "span.job-desc")
        job_data["job_description"] = job_description_element[0].text if job_description_element else "N/A"

        # Extract skills/tags
        skills_elements = job.find_elements(By.CSS_SELECTOR, "li.tag-li")
        job_data["skills"] = [skill.text for skill in skills_elements] if skills_elements else []

        # Extract post date
        post_date_element = job.find_elements(By.CSS_SELECTOR, "span.job-post-day")
        job_data["post_date"] = post_date_element[0].text if post_date_element else "N/A"

        jobs.append(job_data)

    return jobs


def scrape_jobs(base_url):
    """Scrape job listings from multiple pages."""
    driver = setup_driver()
    all_jobs = []
    page_number = 1
    max_pages = 20  # Limit to avoid infinite loops

    while page_number <= max_pages:
        current_url = f"{base_url}-{page_number}?wfhType=2"
        logging.info(f"Loading page {page_number} from URL: {current_url}")

        driver.get(current_url)

        # Wait for the job listings container to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.srp-jobtuple-wrapper"))
        )

        jobs = extract_jobs(driver)
        if not jobs:
            logging.info("No more jobs found. Ending crawl.")
            break

        all_jobs.extend(jobs)
        logging.info(f"Extracted {len(jobs)} jobs from page {page_number}.")

        page_number += 1

    driver.quit()
    return all_jobs

