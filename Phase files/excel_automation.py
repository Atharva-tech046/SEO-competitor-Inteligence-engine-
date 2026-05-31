import csv
import re
from collections import Counter
import pandas as pd

print("Reading scraped data...")
# 1. Fetch the data exactly like before
with open('seo_data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    row = next(reader)
    corpus = row['Full Content']

# 2. Run our NLP pipeline
clean_text = re.sub(r'[^a-zA-Z\s]', '', corpus).lower()
tokens = clean_text.split()
stop_words = {"the", "and", "of", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with", "it", "not", "or", "be", "are", "from", "at", "as", "an", "was", "can", "which", "how", "such", "their", "they", "have", "has"}
filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]

# Get the top 20 keywords this time for a better spreadsheet report
word_counts = Counter(filtered_tokens).most_common(20)

# 3. Convert data to a Pandas DataFrame (Structured Table)
# This formats our raw Python dictionary into clean rows and columns
df = pd.DataFrame(word_counts, columns=['Keyword', 'Frequency (Occurrences)'])

# Capitalize keywords for clean presentation
df['Keyword'] = df['Keyword'].str.capitalize()

# 4. Export directly to Excel with automatic formatting
excel_filename = 'SEO_Keyword_Report.xlsx'
df.to_excel(excel_filename, index=False, sheet_name='Keywords Analysis')

print(f"Success! Final automated spreadsheet saved as: '{excel_filename}'")