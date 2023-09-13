import argparse
import pandas as pd
import logging
from src.utils import load_search_terms, save_search_terms
from src.scraper import scrape_all_results
from src.emailer import send_email

# Set up logging configuration
logging.basicConfig(filename='../logs/scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description="Search for items on bidfta.com")
    parser.add_argument('--add', type=str, help="Add an item to the search list")
    parser.add_argument('--remove', type=str, help="Remove an item from the search list")
    parser.add_argument('--email', type=str, help="Email address to send notifications")

    args = parser.parse_args()

    items_to_search = load_search_terms()

    if args.add and args.add not in items_to_search:
        items_to_search.append(args.add)
        save_search_terms(items_to_search)
        logging.info(f"Added search term: {args.add}")

    if args.remove and args.remove in items_to_search:
        items_to_search.remove(args.remove)
        save_search_terms(items_to_search)
        logging.info(f"Removed search term: {args.remove}")

    logging.info("Starting scraping process...")
    all_results = []
    for item in items_to_search:
        results = scrape_all_results(item)
        for r in results:
            all_results.append((item, *r))
    logging.info("Scraping process completed.")

    # Save results to CSV
    df = pd.DataFrame(all_results, columns=["Search Term", "Description", "Location", "Current Bid"])
    df.to_csv("../data/results.csv", index=False)
    logging.info("Results saved to results.csv")

    # Send email notification
    if args.email:
        try:
            send_email("Bidfta Search Results", "Please find attached the search results from Bidfta.", args.email, "../data/results.csv")
            logging.info(f"Email sent to {args.email}")
        except Exception as e:
            logging.error(f"Error sending email: {e}")

if __name__ == "__main__":
    main()