"""
Text Processing and Word Frequency Analysis

This program fetches a text excerpt from Jane Austen's *Pride and Prejudice* and
performs word frequency analysis using two approaches:
1. Basic string-based processing
2. Advanced NLP preprocessing using spaCy

The goal is to compare how preprocessing affects word frequency results.
"""

import operator
import spacy

# Function to fetch data
def fetch_text(raw_url):
    """
    Fetch text data from a URL and cache it locally.

    This function downloads text from the provided URL and saves it to a local
    cache directory to avoid repeated network requests. If the text has already
    been cached, it will be read directly from the cache.

    Parameters:
    raw_url (str): The URL pointing to a raw text file.

    Returns:
    str: The fetched text content as a string. Returns an empty string if the
    request fails.
    """
    import requests
    from pathlib import Path
    import hashlib

    CACHE_DIR = Path("cs_110_content/text_cache")
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    def _url_to_filename(url):
        url_hash = hashlib.sha1(url.encode("utf-8")).hexdigest()[:12]
        return CACHE_DIR / f"{url_hash}.txt"

    cache_path = _url_to_filename(raw_url)

    SUCCESS_MSG = "✅ Text fetched."
    FAILURE_MSG = "❌ Failed to fetch text."
    try:
        if not cache_path.exists():
            response = requests.get(raw_url, timeout=10)
            response.raise_for_status()
            text_data = response.text
            cache_path.write_text(text_data, encoding="utf-8")
        print(SUCCESS_MSG)
        return cache_path.read_text(encoding="utf-8")

    except Exception as e:
        print(FAILURE_MSG)
        print(f"Error: {e}")
        return ""

# Save the URL in a variable
PRIDE_PREJUDICE_URL = "https://gist.githubusercontent.com/goodbadwolf/8514e63776c1e9717d844ea4ee407739/raw/fdc87a64fd18e6ddb01ce8d758f8f2de8d03e163/pride_prejudice_excerpt.txt"

# Fetch the text
pride_prejudice_text = fetch_text(PRIDE_PREJUDICE_URL)

# Statistics about the data
def print_text_stats(text):
    """
    Print basic statistics about a text string.

    This function calculates and prints the total number of characters,
    lines, and words in the provided text.

    Parameters:
    text (str): The text to analyze.

    Returns:
    None
    """
    num_chars = len(text)

    lines = text.splitlines()
    num_lines = len(lines)

    num_words = 0
    for line in lines:
        words_in_line = line.split()
        num_words += len(words_in_line)

    print(f"Number of characters: {num_chars}")
    print(f"Number of lines: {num_lines}")
    print(f"Number of words: {num_words}")

# Function to get word counts
def get_word_counts(text):
    """
    Count word frequencies using basic string processing.

    This function splits the text into words using whitespace, converts
    all words to lowercase, and counts how often each word appears.

    Parameters:
    text (str): The text to analyze.

    Returns:
    dict: A dictionary mapping words (str) to their frequency counts (int).
    """
    word_counts = {}
    lines = text.splitlines()
    for line in lines:
        words = line.split()
        for word in words:
            word = word.lower()
            if word in word_counts:
                word_counts[word] += 1
            else:
                word_counts[word] = 1
    return word_counts

# the print_top_10_frequent_words will call the above get_word_counts() and print only the top 10 frequent words.
def print_top_10_frequent_words(text):
    """
    Print the top 10 most frequent words in a text.

    This function uses get_word_counts() to calculate word frequencies,
    sorts the results in descending order, and prints the 10 most common words.

    Parameters:
    text (str): The text to analyze.

    Returns:
    None
    """
    word_counts = get_word_counts(text)
    sorted_word_counts = dict(
        sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
    )
    top_10_words = list(sorted_word_counts.items())[:10]
    for word, count in top_10_words:
        print(f"{word}: {count}")

# this is a test print
print_text_stats(pride_prejudice_text)

# get the word counts
word_counts = get_word_counts(pride_prejudice_text)
print(word_counts)

# print the top 10 frequent words
print_top_10_frequent_words(pride_prejudice_text)

"""
Using spaCy for advanced text processing
"""

nlp = spacy.load('en_core_web_sm')

def word_tokenization_normalization(text):
    """
    Tokenize and normalize text using spaCy.

    This function processes text with spaCy to remove stop words,
    punctuation, numbers, and short tokens. Remaining words are
    lemmatized and returned as a list.

    Parameters:
    text (str): The raw text to process.

    Returns:
    list: A list of cleaned and lemmatized word strings.
    """
    text = text.lower()
    doc = nlp(text)

    words_normalized = []
    for word in doc:
        if (
            word.text != '\n'
            and not word.is_stop
            and not word.is_punct
            and not word.like_num
            and len(word.text.strip()) > 2
        ):
            words_normalized.append(str(word.lemma_))

    return words_normalized

def word_count(word_list):
    """
    Count word frequencies from a list of words.

    This function iterates over a list of words and counts how often
    each word appears.

    Parameters:
    word_list (list): A list of word strings.

    Returns:
    dict: A dictionary mapping words (str) to their frequency counts (int).
    """
    word_counts = {}
    for word in word_list:
        word = word.lower()
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
    return word_counts

def print_top_15_frequent_words(word_counts):
    """
    Print the top 15 most frequent words from a word-count dictionary.

    This function sorts the dictionary by frequency in descending order
    and prints the 15 most common words.

    Parameters:
    word_counts (dict): A dictionary mapping words to frequency counts.

    Returns:
    None
    """
    sorted_word_counts = dict(
        sorted(word_counts.items(), key=operator.itemgetter(1), reverse=True)
    )
    top_15_words = list(sorted_word_counts.items())[:15]
    for word, count in top_15_words:
        print(f"{word}: {count}")

doc_tokenized = word_tokenization_normalization(pride_prejudice_text)
print(doc_tokenized)

new_counts = word_count(doc_tokenized)
print(new_counts)

print_top_15_frequent_words(new_counts)

"""
COMPARATIVE ANALYSIS

The top 10 most frequent words produced by the basic get_word_counts() function
are dominated by common function words such as “the,” “to,” “and,” “of,” and “a.”
These words appear frequently in English but provide little insight into the
actual meaning or themes of the text. Because this approach relies only on basic
string splitting and lowercasing, punctuation and grammatical variations are
counted as separate words, which adds noise to the results.

In contrast, the top 15 most frequent words generated after spaCy’s
word_tokenization_normalization() preprocessing are more content-focused.
spaCy removes stop words, punctuation, numbers, and very short tokens, and it
also lemmatizes words so that different grammatical forms are grouped together.
As a result, the list contains words related to characters, social relationships,
and judgment, which are central themes in Pride and Prejudice.

The results differ because spaCy’s preprocessing filters out high-frequency but
low-meaning words and normalizes word forms. This makes the cleaned results far
more meaningful for understanding the text’s content. Removing common words
helps reveal underlying topics such as marriage, family, reputation, and social
status. Overall, the spaCy-based approach provides clearer insight into the themes
and narrative focus of the excerpt.
"""