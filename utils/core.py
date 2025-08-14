import re
from collections import Counter
from pyvi import ViTokenizer
from utils.llm import call_llm_keyword_filter

# ===== Load stopwords =====
def load_stopwords(path='stopword/vietnamese-stopwords.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        return set([line.strip().lower() for line in f if line.strip()])

stopwords = load_stopwords("stopword/vietnamese-stopwords.txt")
stopwords_dash = load_stopwords()

# ===== Remove emojis =====
def remove_emoji(text):
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"  # Emoticons
        u"\U0001F300-\U0001F5FF"  # Symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # Transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # Flags
        u"\U00002500-\U00002BEF"  # Misc symbols
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U00002700-\U000027BF"  # More dingbats
        u"\U0001F900-\U0001F9FF"  # Supplemental symbols
        u"\U0001FA70-\U0001FAFF"  # Extended symbols
        u"\U00002600-\U000026FF"  # Misc symbols
        u"\U00002300-\U000023FF"  # Misc technical
        u"\U0001F018-\U0001F270"  # Misc icons
        u"\U0001F650-\U0001F67F"  # Ornamental symbols
        "]+",
        flags=re.UNICODE
    )
    return emoji_pattern.sub(" ", text)

# ===== Clean text =====
def clean_text(text):
    if not isinstance(text, str):
        return ""

    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)  # Remove links
    text = re.sub(r"#\S+", " ", text)                     # Remove hashtags
    text = remove_emoji(text)                             # Remove emojis
    text = re.sub(r"\d+", " ", text)                      # Remove numbers
    text = re.sub(r"[^\wÀ-ỹ\s_]", " ", text)               # Remove special chars
    text = re.sub(r"\s+", " ", text).strip()               # Normalize spaces

    return text

# ===== Extract keywords =====
def extract_keywords_from_titles(titles, min_freq=10):
    counter = Counter()

    for text in titles:
        text = clean_text(text)
        if not text:
            continue

        tokens = ViTokenizer.tokenize(text).split()

        for token in tokens:
            token_clean = token.lower().strip()

            if not token_clean or len(token_clean) == 1:
                continue
            if token_clean in stopwords_dash or token_clean in stopwords:
                continue

            counter[token_clean] += 1

    # Filter keywords by frequency threshold
    keywords = [kw for kw, freq in counter.items() if freq >= min_freq]
    return keywords

def extract_keywords(titles, category, min_freq=10):
    """
    Extract keywords from a list of titles based on the specified category.
    """
    if not titles or not isinstance(titles, list):
        return []

    keywords = extract_keywords_from_titles(titles, min_freq)
    filtered_keywords = call_llm_keyword_filter(category, keywords)
    return filtered_keywords