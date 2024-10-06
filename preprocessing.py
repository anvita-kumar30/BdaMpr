import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')  # Download WordNet data

def preprocess_email(email_content):
    """
    Preprocesses the email content by removing stopwords and lemmatizing words.
    """
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()

    # Tokenize, lowercase, remove stopwords, and lemmatize
    words = email_content.split()
    processed_words = [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in stop_words]

    return ' '.join(processed_words)
