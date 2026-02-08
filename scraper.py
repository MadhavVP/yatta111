"""
Scraper module - fetches bills from Indiana General Assembly website
Nathan's code - refactored to not run on import
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def fetch_new_bills():
    """
    Fetch bills from Indiana General Assembly website
    Returns a list of bill dictionaries
    """
    print("[Scraper] Starting bill fetch...")
    
    # Set up headless Firefox
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(options=options)
    
    try:
        # Search for bills related to "woman"
        driver.get("https://iga.in.gov/search?q=woman")
        driver.implicitly_wait(2)
        
        # Change pagination to show 100 results
        driver.find_element(By.CLASS_NAME, 'PaginationSelect_select__4bc2b')
        select_element = driver.find_element(By.CLASS_NAME, 'PaginationSelect_select__4bc2b')
        select = Select(select_element)
        select.select_by_visible_text('100')
        
        driver.implicitly_wait(2)
        try:
            driver.find_element(By.CLASS_NAME, 'BaseResult_resultContainer__pgT+s')
        except:
            pass
        
        # Parse the search results
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', class_='BaseResult_resultContainer__pgT+s')
        
        bills = []
        
        for r in results:
            # Extract basic bill info
            title_elem = r.find_all('h6')
            desc_elem = r.find_all('p')
            
            if not title_elem or not desc_elem:
                continue
                
            bill_id = title_elem[0].text.strip()
            description = desc_elem[0].text.strip()
            bill_page_link = f"https://iga.in.gov{r.find_all('a')[0]['href']}"
            
            print(f"[Scraper] Found: {bill_id}")
            print(f"[Scraper]   {description}")
            
            # Get PDF link from bill page
            pdf_url = get_bill_pdf_url(bill_page_link, options)
            
            if pdf_url:
                print(f"[Scraper]   PDF: {pdf_url}")
            
            # Create bill object
            bill = {
                'id': bill_id,
                'title': description,
                'source': 'indiana_legislature',
                'state': 'IN',
                'status': 'introduced',  # Could parse this from page
                'url': pdf_url or bill_page_link,
                'text': ''  # Will be filled by get_bill_text() if needed
            }
            
            bills.append(bill)
        
        print(f"[Scraper] Fetched {len(bills)} bills")
        return bills
        
    except Exception as e:
        print(f"[Scraper] Error fetching bills: {e}")
        import traceback
        traceback.print_exc()
        return []
        
    finally:
        driver.quit()


def get_bill_pdf_url(bill_page_url, options=None):
    """
    Navigate to a bill page and extract the PDF link
    """
    if options is None:
        options = Options()
        options.add_argument("--headless")
    
    driver = webdriver.Firefox(options=options)
    
    try:
        driver.get(bill_page_url)
        driver.implicitly_wait(2)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        pdf_link_elem = soup.find('a', class_='Menu_menuItem__Y4JS+ Menu_primary__Dj7Gh')
        
        if pdf_link_elem and 'href' in pdf_link_elem.attrs:
            return pdf_link_elem['href']
        
        return None
        
    except Exception as e:
        print(f"[Scraper] Error getting PDF URL: {e}")
        return None
        
    finally:
        driver.quit()


def get_bill_text(bill_id):
    """
    Fetch the full text of a bill given its ID
    For now, returns empty string - could implement PDF parsing
    """
    # TODO: Implement PDF text extraction if needed
    # Could use PyPDF2 or similar to extract text from PDF
    return ""
