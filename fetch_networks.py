import requests
import csv
import time

def fetch_all_networks():
    """
    Fetches all paginated data from the GeckoTerminal API.
    """
    all_networks = []
    # Start with the first page
    next_url = "https://api.geckoterminal.com/api/v2/networks?page=1"
    
    print("Starting data fetch...")

    while next_url:
        try:
            response = requests.get(next_url)
            response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
            data = response.json()

            # Add the networks from the current page
            page_data = data.get("data", [])
            if not page_data:
                print("No more data found.")
                break  # Stop if the 'data' array is empty
            
            for item in page_data:
                all_networks.append({
                    "id": item.get("id"),
                    "name": item.get("attributes", {}).get("name")
                })

            # Find the URL for the next page
            next_url = data.get("links", {}).get("next")
            
            if next_url:
                print(f"Fetching next page: {next_url}")
                time.sleep(1) # Be polite to the API, wait 1 second
            else:
                print("All pages fetched.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            break
            
    return all_networks

def save_to_csv(networks):
    """
    Saves the list of networks to networks.csv.
    """
    if not networks:
        print("No networks to save.")
        return

    # Define the CSV headers
    headers = ["id", "name"]
    
    with open("networks.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(networks)
    
    print(f"Successfully saved {len(networks)} networks to networks.csv")

if __name__ == "__main__":
    networks_list = fetch_all_networks()
    save_to_csv(networks_list)
