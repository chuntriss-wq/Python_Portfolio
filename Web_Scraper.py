import requests
from bs4 import BeautifulSoup
import time # Used to simulate a delay, which is good practice for web scraping
import csv # New module imported for CSV file handling

# The base URL of the target website. This is a public, open source site designed for scraping demos.
SCRAPE_URL = "http://quotes.toscrape.com/"
CSV_FILENAME = "quotes.csv" # Define a constant for the output file name

def scrape_all_quotes():
    """
    Fetches the HTML from the target URL, extracts all quotes and authors, 
    and handles pagination to scrape all pages.
    """
    all_quotes = []
    current_url = SCRAPE_URL
    page_count = 0
    
    # Loop continues as long as a 'next' link is found
    while current_url:
        page_count += 1
        print(f"\n--- Scraping Page {page_count} at: {current_url} ---")
        
        # 1. Network Request and Error Handling
        try:
            # Make the HTTP GET request
            response = requests.get(current_url, timeout=10)
            
            # Raise an exception for bad status codes (4xx or 5xx)
            response.raise_for_status() 
            
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Failed to fetch the page {current_url}. Details: {e}")
            break # Stop scraping if a page fails
            
        # Introduce a slight delay to be polite to the server
        time.sleep(1) 
        
        # 2. Parsing and Extraction
        try:
            # Initialize BeautifulSoup with the downloaded HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find all <div> elements with the class 'quote'
            quote_elements = soup.find_all('div', class_='quote')
            
            # Extract data from the current page
            for quote_element in quote_elements:
                text = quote_element.find('span', class_='text').get_text(strip=True)
                author = quote_element.find('small', class_='author').get_text(strip=True)
                all_quotes.append({'quote': text, 'author': author})
                
            # 3. Find the Next Page Link for Pagination
            next_link_container = soup.find('li', class_='next')
            
            if next_link_container:
                # If a 'next' link is found, get the relative URL
                next_page_relative = next_link_container.find('a')['href']
                # Construct the full absolute URL for the next page
                current_url = SCRAPE_URL.rstrip('/') + next_page_relative
            else:
                # If no 'next' link is found, set current_url to None to break the loop
                current_url = None
                
        except Exception as e:
            print(f"ERROR during parsing of page {page_count}: {e}")
            break # Stop scraping on parsing error

    print("\n--- Scraping Complete ---")
    return all_quotes

# --- NEW FUNCTION FOR DATA PERSISTENCE ---

def save_to_csv(data: list[dict], filename: str, fieldnames: list):
    """
    Writes a list of dictionaries to a CSV file.
    
    Uses the 'with open' statement (Python best practice for file handling)
    and the DictWriter object to manage dictionary-to-CSV mapping.
    """
    try:
        # 'w' mode means write (overwrites file if it exists)
        # newline='' prevents blank rows from being inserted in Windows
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            
            # Create a DictWriter object to map dictionary keys to CSV columns
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            # Write the header row using the fieldnames
            writer.writeheader()
            
            # Write the data rows
            writer.writerows(data)
            
        print(f"\nSUCCESS: Data saved to {filename}")
        
    except Exception as e:
        print(f"ERROR: Could not write data to CSV file: {e}")


# --- Execution ---

if __name__ == "__main__":
    
    # We now call the function that handles all pagination
    extracted_data = scrape_all_quotes() 
    
    if extracted_data:
        print("\n--- Extracted Quotes Summary ---")
        print(f"Total Quotes Found: {len(extracted_data)}\n")
        
        # Save the data to a CSV file
        field_headers = ['quote', 'author']
        save_to_csv(extracted_data, CSV_FILENAME, field_headers)

        # Print a few examples for confirmation
        for i, data in enumerate(extracted_data[:3]):
            print(f"{i+1}. {data['quote']} (by {data['author']})")
        
        if len(extracted_data) > 3:
             print("...")
             
    else:
        print("\nNo quotes were extracted. Please check the error messages above.")
