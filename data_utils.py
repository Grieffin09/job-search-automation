import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_jobs_to_csv(jobs, filename):
    """Save a list of jobs to a CSV file."""
    if not jobs:
        logging.info("No jobs to save.")
        return

    fieldnames = jobs[0].keys()

    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(jobs)
        logging.info(f"Saved {len(jobs)} jobs to '{filename}'.")
    except IOError as e:
        logging.error(f"Error saving jobs to CSV: {e}")
