import pandas as pd
import requests
from bs4 import BeautifulSoup
import os

df = pd.read_csv(r'C:\Users\jatin\coding_stuff\Black_Cuffer_assignment\Input.csv')


output_dir = 'article_texts'
os.makedirs(output_dir, exist_ok=True)

for _, row in df.iterrows():
    url_id = row['URL_ID']
    url = row['URL']

    # Fetch the webpage content
    try:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'html.parser')
        content_div = soup.find('div', class_="td-post-content tagdiv-type")
        if content_div is not None:
            extracted_text = content_div.get_text(separator='\n', strip=True)
        else:
            extracted_text = "";
    except requests.RequestException as e:
        print(f"Error fetching content for URL {url}: {e}")
        continue
    filename = os.path.join(output_dir, f"{url_id}.txt")
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(extracted_text)

    print(f"Saved content for URL ID {url_id} to {filename}")

print("All articles extracted and saved to text files.")

