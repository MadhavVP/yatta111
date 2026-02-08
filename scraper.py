# MOCK SCRAPER MODULE
# Restored because file was missing

def fetch_new_bills():
    """
    Mock function to return a list of 'new' bills.
    """
    print("[MOCK] Scraper: Fetching new bills...")
    return [
        {
            "id": "BILL-124",
            "title": "The Equal Tacos Act",
            "text": "This bill mandates taco equality for all citizens.",
            "source": "federal",
            "url": "http://congress.gov/bill/123"
        },
        {
            "id": "BILL-456",
            "title": "Maternal Health Improvement Act",
            "text": "Provides funding for improved maternal healthcare facilities.",
            "source": "state",
            "url": "http://state.gov/bill/456"
        }
    ]
