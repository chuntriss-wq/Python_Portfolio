import requests
import json
import random

# --- OOP CLASS: API Fetcher ---
class APIFetcher:
    """
    A class to encapsulate the logic for making HTTP requests and handling 
    common network errors and JSON parsing for various public APIs.
    """
    
    def __init__(self, name="Generic Fetcher"):
        # Instance attribute for identification
        self.name = name
        # Class attributes (shared) could be used here for API keys/rate limits

    def _make_request(self, url: str) -> dict or None:
        """
        Internal, protected method to handle the core network request and error handling.
        Returns the parsed JSON dictionary on success, or None on failure.
        """
        print(f"\n[{self.name}] Attempting to fetch data from: {url}")
        
        try:
            # Step 1: Make the HTTP GET request with a timeout
            response = requests.get(url, timeout=10) 
            
            # Step 2: Check for a successful response (raises HTTPError for 4xx/5xx codes)
            response.raise_for_status() 
            
            # Step 3: Parse the JSON data
            return response.json()
            
        except requests.exceptions.HTTPError as err_h:
            print(f"[{self.name}] HTTP Error ({response.status_code}): {err_h}")
        except requests.exceptions.ConnectionError as err_c:
            print(f"[{self.name}] Connection Error: {err_c}")
        except requests.exceptions.Timeout as err_t:
            print(f"[{self.name}] Timeout Error: {err_t}")
        except requests.exceptions.RequestException as err:
            print(f"[{self.name}] Unknown Request Error: {err}")
        except json.JSONDecodeError:
            print(f"[{self.name}] Error: Failed to decode JSON response.")
            
        return None # Return None if any error occurred

    def fetch_chuck_norris_joke(self) -> str:
        """Fetches a random joke using the internal request method."""
        api_url = "https://api.chucknorris.io/jokes/random"
        data = self._make_request(api_url)
        
        if data:
            # The joke text is typically under the 'value' key
            return data.get('value', 'Joke content not found.')
        return "Failed to retrieve joke."

    def fetch_inspirational_quote(self) -> str:
        """
        Fetches a random inspirational quote from a reliable public API.
        The API returns a single dictionary object.
        """
        api_url = "https://api.quotable.io/random" # Updated API endpoint
        data_dict = self._make_request(api_url) # Renamed variable for clarity of new API structure
        
        if data_dict and isinstance(data_dict, dict):
            # The quotable.io API uses 'content' for the text and 'author'
            text = data_dict.get('content', 'Quote content missing') 
            author = data_dict.get('author', 'Unknown')
            
            return f"\"{text}\" - {author}"
        return "Failed to retrieve quote."


# --- Execution and Demonstration ---

def run_api_demo():
    """Demonstrates usage and error handling for the APIFetcher class."""
    
    # Instantiate the class (Encapsulation)
    my_fetcher = APIFetcher(name="Quote & Joke Bot")
    
    # 1. Fetch a Joke
    joke_result = my_fetcher.fetch_chuck_norris_joke()
    print("\n--- Chuck Norris Joke ---")
    print(joke_result)
    
    # 2. Fetch an Inspirational Quote
    quote_result = my_fetcher.fetch_inspirational_quote()
    print("\n--- Inspirational Quote ---")
    print(quote_result)

    # 3. Demonstration of simple testing using assert (Post-OOP best practice)
    # Since we can't control the live API content, we test for successful retrieval structure.
    print("\n--- API Test Assertions ---")
    assert joke_result != "Failed to retrieve joke.", "TEST FAILED: Joke retrieval was unsuccessful."
    assert quote_result != "Failed to retrieve quote.", "TEST FAILED: Quote retrieval was unsuccessful."
    print("✅ Assertions passed: Data was successfully retrieved from both APIs.")


if __name__ == "__main__":
    run_api_demo()
