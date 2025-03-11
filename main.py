import logging
from scraper import scrape_jobs
from data_utils import save_jobs_to_csv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    base_url = "https://www.naukri.com/data-scientist-jobs"

    all_jobs = scrape_jobs(base_url)

    if all_jobs:
        save_jobs_to_csv(all_jobs, "Todays_Remote_Jobs.csv")
    else:
        logging.info("No jobs were found during the crawl.")

if __name__ == "__main__":
    main()
