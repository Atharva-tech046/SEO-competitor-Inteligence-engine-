import csv
import re
from collections import Counter

print("Starting NLP Keyword Analysis...")

#1.Load the Corpus Data (reading the data tht just loaded) 
with open('seo_data.csv', mode='r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    row = next(reader)
    corpus = row['Full Content']

#2.Text Normalization (Remove punctuation and make lowercase)
clean_text = re.sub(r'[^a-zA-Z\s]', '', corpus).lower()

#3.Tokenization 
tokens = clean_text.split()

#4.Stop Word Removal (Filter out common grammar words)
stop_words = {"the", "and", "of", "to", "a", "in", "for", "is", "on", "that", "by", "this", "with", "it", "not", "or", "be", "are", "from", "at", "as", "an", "was", "can", "which", "how", "such", "their", "they", "have", "has"}

# Keep the word if it's not a stop word AND it's longer than 2 letters
filtered_tokens = [word for word in tokens if word not in stop_words and len(word) > 2]

#5.Frequency Distribution (Count the occurrences of each keyword)
word_counts = Counter(filtered_tokens)

#6.Output the Results
print("\n--- Top 10 Competitor SEO Keywords ---")
for word, count in word_counts.most_common(10):
    print(f"{word.capitalize()}: {count} occurrences")