import os
import nltk
import string
import re
import pyphen
nltk.download('punkt')
from nltk.corpus import stopwords
nltk.download('stopwords')

stopword_folder_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/20211030 Test Assignment/StopWords"

def read_and_combine_files(stopword_folder_path):
    combined_text = ""
    for filename in os.listdir(stopword_folder_path):
        if filename.endswith(".txt"):
            filepath = os.path.join(stopword_folder_path, filename)
            with open(filepath, 'r') as f:
                file_text = f.read()
                combined_text += file_text + ", "

    return combined_text[:-2]

given_stop_word = read_and_combine_files(stopword_folder_path)
positive_dict_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/MasterDictionary/positive-words.txt"
negative_dict_path = "C:/Users/jatin/coding_stuff/Black_Cuffer_assignment/MasterDictionary/negative-words.txt"

with open(positive_dict_path, "r") as f:
    positive_words = f.read().splitlines()

with open(negative_dict_path, "r") as f:
    negative_words = f.read().splitlines()

positive_dict = {word: 'positive' for word in positive_words}
negative_dict = {word: 'negative' for word in negative_words}

def calculate_sentiment_scores(text, positive_dict, negative_dict, given_stop_word):
    tokens = nltk.word_tokenize(text)  # Tokenize the input text
    filtered_words = [word for word in tokens if word.lower() not in given_stop_word]

    positive_score = sum(1 for word in filtered_words if word in positive_dict)
    negative_score = sum(-1 for word in filtered_words if word in negative_dict)
    negative_score = negative_score * -1

    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    total_words = len(filtered_words)
    subjectivity_score = (positive_score + negative_score) / (total_words + 0.000001)

    return positive_score, negative_score, polarity_score, subjectivity_score


def calculate_readability(text):
    try:
        sentence_tokens = nltk.sent_tokenize(text)
        tokens = nltk.word_tokenize(text)
        avg_sentence_length = len(tokens) / len(sentence_tokens)
        syllable_counter = pyphen.Pyphen(lang='en_US')
        complex_words = sum(1 for word in tokens if syllable_counter.inserted(word).count("-") >= 2)
        percentage_of_complex_words = complex_words / len(tokens)
        fog_index = 0.4 * (avg_sentence_length + float(percentage_of_complex_words))

        return avg_sentence_length, percentage_of_complex_words, fog_index, complex_words
    except ZeroDivisionError:
        print("Error: Cannot calculate readability for empty text.")
        return None

def word_count_without_stop_words(text):
    stop_words = set(stopwords.words('english'))
    translator = str.maketrans('', '', string.punctuation)
    tokens = nltk.word_tokenize(text)
    cleaned_words = [word.translate(translator).lower() for word in tokens if
                     word.translate(translator).lower() not in stop_words]
    return len(cleaned_words)


def syllabel_count_per_word(text):
    tokens = nltk.word_tokenize(text)
    vowels = "aeiouy"
    for word in tokens:
        count = 0
        if word.endswith("es") or word.endswith("ed"):
            if not any(vowel in word[:-2] for vowel in vowels):
                return count
        if word[-1] == "e":
            word = word[:-1]
        for index, char in enumerate(word):
            if char in vowels and (index == 0 or word[index - 1] not in vowels):
                count += 1
        return count


def personal_pronouns(text):
    pronoun_pattern = r"\b(i|we|my|ours|us)\b(?!\s*US)"
    matches = re.findall(pronoun_pattern, text, flags=re.IGNORECASE)
    return len(matches)


def average_word_length(text):
    try:
        words = text.split()
        total_characters = sum(len(word) for word in words)
        total_words = len(words)
        awl = total_characters / total_words
        return awl
    except ZeroDivisionError:
        print("Error: Cannot calculate readability for empty text.")
        return None

