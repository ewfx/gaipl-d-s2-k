from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

# Load CSV file
df = pd.read_csv("playbooksv3.csv", delimiter=",")

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings for job_template_name
df["embedding"] = df["job_template_name"].apply(lambda x: model.encode(x, convert_to_numpy=True))

# Convert embeddings to a NumPy array for efficient search
embeddings_matrix = np.vstack(df["embedding"].values)

# Check the shape of the embeddings matrix
print("Embeddings matrix shape:", embeddings_matrix.shape)


def find_similar_templates(keyword, top_n=5):
    """Finds the top N most similar job template names based on cosine similarity."""
    # Convert the keyword to an embedding
    keyword_embedding = model.encode(keyword, convert_to_numpy=True).reshape(1, -1)

    # Compute cosine similarity with all job template embeddings
    similarities = cosine_similarity(keyword_embedding, embeddings_matrix).flatten()

    # Get top N matches
    top_indices = similarities.argsort()[-top_n:][::-1]

    # Return matched job template names with similarity scores
    return df.iloc[top_indices][["job_template_id", "job_template_name", "embedding"]].assign(similarity=similarities[top_indices])


def refine_results(initial_results, new_keyword, top_n=3):
    """Filters the initial results further using a new keyword."""
    # Convert the new keyword to an embedding
    new_keyword_embedding = model.encode(new_keyword, convert_to_numpy=True).reshape(1, -1)

    # Extract embeddings of initial top results
    initial_embeddings = np.vstack(initial_results["embedding"].values)

    # Compute cosine similarity within the top results
    new_similarities = cosine_similarity(new_keyword_embedding, initial_embeddings).flatten()

    # Get top matches within this refined set
    top_indices = new_similarities.argsort()[-top_n:][::-1]

    # Return refined results
    return initial_results.iloc[top_indices].drop(columns=["embedding"]).assign(similarity=new_similarities[top_indices])


# Example Usage
keyword1 = "kafka"
initial_results = find_similar_templates(keyword1, top_n=5)

keyword2 = "integration"
refined_results = refine_results(initial_results, keyword2, top_n=3)

print(refined_results)
