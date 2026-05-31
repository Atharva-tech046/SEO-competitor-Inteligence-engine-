import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/IPhone"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Fetching data from the target URL...")
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the main title
    page_title = soup.find('h1').get_text() if soup.find('h1') else "No H1 Found"
    
    # Extract all H2 subheadings (List comprehension to get the text of each)
    subheadings = [h2.get_text().strip() for h2 in soup.find_all('h2')]
    
    # Extract all paragraph text
    paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
    # Join all paragraph text into one massive block of text, removing empty spaces
    full_text = " ".join([p for p in paragraphs if p])
    
    print("Data extracted successfully! Saving to CSV...")

    # --- NEW: Save the extracted data to a CSV file ---
    # We create a file called 'seo_data.csv' and write our findings into it
    with open('seo_data.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row
        writer.writerow(['Page Title', 'Subheadings (H2)', 'Full Content'])
        # Write our extracted data
        writer.writerow([page_title, " | ".join(subheadings), full_text])
        
    print("Done! Check your folder for 'seo_data.csv'.")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")