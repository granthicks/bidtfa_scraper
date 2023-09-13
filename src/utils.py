def load_search_terms(file_path="../data/search_terms.txt"):
    """
    Load search terms from a file.

    Args:
    - file_path (str): Path to file containing search terms.

    Returns:
    - list: List of search terms.
    """

    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []

def save_search_terms(terms, file_path="../data/search_terms.txt"):
    """
    Save search terms to a file.

    Args:
    - terms (list): List of search terms to save.
    - file_path (str): Path to the file to save the search terms.
    """

    with open(file_path, 'w') as f:
        for term in terms:
            f.write(f"{term}\n")
