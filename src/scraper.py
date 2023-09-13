import requests
from bs4 import BeautifulSoup

def fetch_content(search_term, page=1):
    """
    Fetch the content of the bidfta.com search URL for a given search term and page number.

    Args:
    - search_term (str): The term to search for on bidfta.com.
    - page (int): The page number to fetch.

    Returns:
    - str: The HTML content of the search results page.
    """
    base_url = "https://www.bidfta.com/items?pageId={}&itemSearchKeywords={}&locations=345"
    url = base_url.format(page, search_term)
    response = requests.get(url)
    return response.content

def extract_data(html_content):
    """
    Extract item details from the HTML content of the bidfta.com search results page.

    Args:
    - html_content (str): The HTML content of the search results page.

    Returns:
    - list: List of tuples containing item details (description, location, current bid).
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    items = soup.find_all('div', class_='item-description')  # Adjust the class based on actual website structure

    results = []
    for i in items:
        description = i.text.strip()
        location = i.find_next('div', class_='item-location').text.strip()  # Adjust the class
        current_bid = i.find_next('div', class_='current-bid').text.strip()  # Adjust the class
        results.append((description, location, current_bid))

    return results

def scrape_all_results(search_term):
    """
    Scrape all results for a given search term, handling pagination.

    Args:
    - search_term (str): The term to search for on bidfta.com.

    Returns:
    - list: List of tuples containing item details from all pages.
    """
    page = 1
    all_results = []

    while True:
        content = fetch_content(search_term, page)
        page_results = extract_data(content)
        if not page_results:
            break
        all_results.extend(page_results)
        page += 1

    return all_results
