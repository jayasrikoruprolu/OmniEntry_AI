import joblib

# Load model
vectorizer = joblib.load("model/vectorizer.pkl")
model = joblib.load("model/services.pkl")

services = model["services"]
vectors = model["vectors"]

def recommend(query):

    query = query.lower().strip()

    query_vector = vectorizer.transform([query])

    similarity = (query_vector * vectors.T).toarray()[0]

    best_index = similarity.argmax()

    return services.iloc[best_index]