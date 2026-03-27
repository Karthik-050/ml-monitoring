from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(code1, code2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([code1, code2])
    similarity = cosine_similarity(vectors)[0][1]
    return similarity

def clean_code(code):
    return "".join(code.split()).lower()