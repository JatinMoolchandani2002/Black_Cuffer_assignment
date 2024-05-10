import os
import nltk
import string
import re
import pandas as pd
import pyphen
from nltk.corpus import stopwords

# Download necessary NLTK data
from parametres import calculate_sentiment_scores, calculate_readability, word_count_without_stop_words,syllabel_count_per_word, personal_pronouns, average_word_length, read_and_combine_files

nltk.download('punkt')
nltk.download('stopwords')

# Define the paths
input_csv_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/Input.csv"
output_dir = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/article_texts"
stopword_folder_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/20211030 Test Assignment/StopWords"
positive_dict_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/20211030 Test Assignment/MasterDictionary/positive-words.txt"
negative_dict_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/20211030 Test Assignment/MasterDictionary/negative-words.txt"
output_excel_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/Output Data Structure.xlsx"

# Read the input CSV to get the URL IDs and URLs
df_input = pd.read_csv(input_csv_path)

# Initialize the output dataframe with the required columns
df_output = pd.DataFrame(
    columns=['URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE', 'SUBJECTIVITY SCORE',
             'AVG SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX', 'COMPLEX WORDS',
             'WORD COUNT WITHOUT STOP WORDS', 'SYLLABLE COUNT PER WORD', 'PERSONAL PRONOUNS', 'AVERAGE WORD LENGTH'])

# Read and combine stop words
stop_word = read_and_combine_files(stopword_folder_path)

# Read positive and negative words
with open(positive_dict_path, "r") as f:
    positive_words = f.read().splitlines()

with open(negative_dict_path, "r") as f:
    negative_words = f.read().splitlines()

positive_dict = {word: 'positive' for word in positive_words}
negative_dict = {word: 'negative' for word in negative_words}

# Function definitions (calculate_sentiment_scores, calculate_readability, word_count_without_stop_words, syllabel_count_per_word, personal_pronouns, average_word_length)

# Loop through each file in the article_texts directory
for _, row in df_input.iterrows():
    url_id = row['URL_ID']
    url = row['URL']
    text_file_path = os.path.join(output_dir, f"{url_id}.txt")

    with open(text_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Calculate metrics
    analysis_1 = calculate_sentiment_scores(text, positive_dict, negative_dict, stop_word)
    analysis_2 = calculate_readability(text)
    analysis_3 = word_count_without_stop_words(text)
    analysis_5 = syllabel_count_per_word(text)
    analysis_6 = personal_pronouns(text)
    analysis_7 = average_word_length(text)

    # Create a new row with the calculated metrics
    new_row = {
        "URL_ID": url_id,
        "URL": url,
        "POSITIVE SCORE": analysis_1[0],
        "NEGATIVE SCORE ": analysis_1[1],
        "POLARITY SCORE": analysis_1[2],
        "SUBJECTIVITY SCORE": analysis_1[3],
        "AVG SENTENCE LENGTH": analysis_2[0],
        "PERCENTAGE OF COMPLEX WORDS": analysis_2[1],
        "FOG INDEX": analysis_2[2],
        "COMPLEX WORDS": analysis_2[3],
        "WORD COUNT WITHOUT STOP WORDS": analysis_3,
        "SYLLABLE COUNT PER WORD": analysis_5,
        "PERSONAL PRONOUNS": analysis_6,
        "AVERAGE WORD LENGTH": analysis_7
    }

    # Append the new row to the output dataframe
    df_output = df_output.append(new_row, ignore_index=True)

# Save the output dataframe to an Excel file
df_output.to_excel(output_excel_path, index=False)

print("All articles analyzed and results saved to Excel.")
