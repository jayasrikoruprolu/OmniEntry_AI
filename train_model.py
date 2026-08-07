import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer

# ===========================
# Load Dataset
# ===========================

data = pd.read_csv("dataset/services.csv")
print(data.columns)
print(data.head())
# Remove missing values
data = data.fillna("")

# Combine important columns for better AI search
data["combined"] = (
    data["service_name"] + " " +
    data["category_name"] + " " +
    data["keywords"]
)

# ===========================
# Train TF-IDF Model
# ===========================

vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True
)

vectors = vectorizer.fit_transform(data["combined"])

# ===========================
# Create model folder
# ===========================

os.makedirs("model", exist_ok=True)

# Save vectorizer
joblib.dump(vectorizer, "model/vectorizer.pkl")

# Save services + vectors together
model = {
    "services": data,
    "vectors": vectors
}

joblib.dump(model, "model/services.pkl")

print("=" * 50)
print("✅ AI Model Trained Successfully")
print(f"Total Services : {len(data)}")
print(f"Vocabulary Size : {len(vectorizer.vocabulary_)}")
print("=" * 50)