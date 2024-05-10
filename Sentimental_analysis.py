import os
import nltk
import string
import re
import pandas as pd
import pyphen

nltk.download('punkt')
from nltk.corpus import stopwords

nltk.download('stopwords')

text_file_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/article_texts/blackassign0001.txt"
with open(text_file_path, 'r') as f:
    text = f.read()

stopword_folder_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/20211030 Test Assignment/StopWords"


# print(text)
def read_and_combine_files(stopword_folder_path):
    combined_text = ""
    for filename in os.listdir(stopword_folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(stopword_folder_path, filename)
            with open(filepath, 'r') as f:
                file_text = f.read()
                combined_text += file_text + ", "  # Add comma as a separator

    return combined_text[:-2]  # Remove the last comma and space


stop_word = read_and_combine_files(stopword_folder_path)

# print(a1)


# Analysis_1 = remove_stopwords(text, stop_word)
#
#
#
positive_dict_path = "20211030 Test Assignment/MasterDictionary/positive-words.txt"
negative_dict_path = "20211030 Test Assignment/MasterDictionary/negative-words.txt"
with open(positive_dict_path, "r") as f:
    positive_words = f.read().splitlines()

with open(negative_dict_path, "r") as f:
    negative_words = f.read().splitlines()

positive_dict = {word: 'positive' for word in positive_words}
negative_dict = {word: 'negative' for word in negative_words}


def calculate_sentiment_scores(text, positive_dict, negative_dict, stop_words):
    tokens = nltk.word_tokenize(text)  # Tokenize the input text
    filtered_words = [word for word in tokens if word.lower() not in stop_words]

    positive_score = sum(1 for word in filtered_words if word in positive_dict)
    negative_score = sum(-1 for word in filtered_words if word in negative_dict)
    negative_score = negative_score * -1

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    total_words = len(filtered_words)
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score



# a2 = calculate_sentiment_scores(text, positive_dict, negative_dict, stop_word)
# print(a2)


def calculate_readability(text):
    sentence_tokens = nltk.sent_tokenize(text)
    tokens = nltk.word_tokenize(text)
    avg_sentence_length = len(tokens) / len(sentence_tokens)
    syllable_counter = pyphen.Pyphen(lang='en_US')
    complex_words = sum(1 for word in tokens if syllable_counter.inserted(word).count("-") >= 2)
    percentage_of_complex_words = complex_words / len(tokens)
    fog_index = 0.4 * (avg_sentence_length + float(percentage_of_complex_words))

    return avg_sentence_length, percentage_of_complex_words, fog_index, complex_words
# a3 = calculate_readability(text)
# print(a3)

def word_count_without_stop_words(text):
    stop_words = set(stopwords.words('english'))
    translator = str.maketrans('', '', string.punctuation)  # Remove punctuation
    tokens = nltk.word_tokenize(text)
    cleaned_words = [word.translate(translator).lower() for word in tokens if word.translate(translator).lower() not in stop_words]
    return len(cleaned_words)
# a4 = word_count_without_stop_words(text)
# print(a4)

def syllabel_count_per_word(text):
    tokens = nltk.word_tokenize(text)
    vowels = "aeiouy"

    for word in tokens:  # Iterate over each word
        count = 0  # Initialize the count for each word

        if word.endswith("es") or word.endswith("ed"):
        # Check for "es" and "ed", but don't count if preceding part has no vowel
            if not any(vowel in word[:-2] for vowel in vowels):
                return count

        if word[-1] == "e":
            word = word[:-1]

        for index, char in enumerate(word):
            if char in vowels and (index == 0 or word[index - 1] not in vowels):
                count += 1

        return count
# a5 = syllabel_count_per_word(text)
# print(a5)

def personal_pronouns(text):
    pronoun_pattern = r"\b(i|we|my|ours|us)\b(?!\s*US)"
    matches = re.findall(pronoun_pattern, text, flags=re.IGNORECASE)

    return len(matches)
    # Process texts
# a6= personal_pronouns(text)
# print(a6)

def average_word_length(text):
    words = text.split()  # Split the text into a list of words
    total_characters = sum(len(word) for word in words)  # Count the total characters
    total_words = len(words)  # Count the number of words

    awl = total_characters / total_words
    return awl


# text_folder = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/article_texts"
# results = process_multiple_texts(text_folder, positive_dict, negative_dict)

# df = pd.DataFrame(results, columns=["Filename", "Positive Score", "Negative Score", "Polarity Score"])
# df.to_excel("test123.xlsx", index=False)


# analysis_2 = calculate_sentiment_scores(text, positive_dict, negative_dict,stop_word)
# analysis_3 = calculate_readability(text)
# analysis_4 = word_count_without_stop_words(text)
# analysis_5 = syllabel_count_per_word(text)
# analysis_6 = personal_pronouns(text)
# analysis_7 = average_word_length(text)

