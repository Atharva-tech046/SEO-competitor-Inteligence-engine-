import requests
from bs4 import BeautifulSoup
import csv
import re
from collections import Counter
import pandas as pd

# ==========================================
# PHASE 1: EXTRACTION (Scraping)
# ==========================================
def extract_data(url):
    print(f"[1/3] Extracting data from: {url}")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Grab main text
        page_title = soup.find('h1').get_text() if soup.find('h1') else "No H1 Found"
        paragraphs = [p.get_text().strip() for p in soup.find_all('p')]
        full_text = " ".join([p for p in paragraphs if p])
        
        # Save raw data backup
        with open('seo_raw_data.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['URL', 'Title', 'Raw Content'])
            writer.writerow([url, page_title, full_text])
            
        return full_text
    else:
        print(f"Error: Failed to fetch page. Status code {response.status_code}")
        return None

# ==========================================
# PHASE 2: TRANSFORMATION (NLP Analysis)
# ==========================================
def analyze_text(text):
    print("[2/3] Running NLP text normalization and tokenization...")
    
    clean_text = re.sub(r'[^a-zA-Z\s]', '', text).lower()
    tokens = clean_text.split()
    
    stop_words = {"the", "and", "of", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with", "it", "not", "or", "be", "are", "from", "at", "as", "an", "was", "can", "which", "how", "such", "their", "they", "have", "has"}
    filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]
    
    # Return top 20 keywords
    return Counter(filtered_tokens).most_common(20)

# ==========================================
# PHASE 3: LOADING (Excel Automation)
# ==========================================
def generate_report(keyword_data, output_filename="Automated_SEO_Report.xlsx"):
    print("[3/3] Generating enterprise Excel report...")
    
    df = pd.DataFrame(keyword_data, columns=['Keyword', 'Frequency (Occurrences)'])
    df['Keyword'] = df['Keyword'].str.capitalize()
    
    df.to_excel(output_filename, index=False, sheet_name='Keyword Analysis')
    print(f"✅ Success! Pipeline complete. Report saved as: {output_filename}")

# ==========================================
# MASTER SWITCH (Execution Block)
# ==========================================
if __name__ == "__main__":
    print("=== STARTING SEO INTELLIGENCE PIPELINE ===")
    
    
    target_url = "https://en.wikipedia.org/wiki/Apple_Inc." 
    
    
    scraped_text = extract_data(target_url)
    
    if scraped_text:
       
        top_keywords = analyze_text(scraped_text)
        
     
        generate_report(top_keywords)