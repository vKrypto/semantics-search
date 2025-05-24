from sentence_transformers import SentenceTransformer
from faqs import FAQData
import numpy as np
import faiss

# Sample FAQs
faq_data = FAQData()
faqs = faq_data.faqs
questions = faq_data.get_questions()

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate and normalize FAQ embeddings
faq_embeddings = model.encode(questions, convert_to_numpy=True)
normalized_faq_embeddings = faq_embeddings / np.linalg.norm(faq_embeddings, axis=1, keepdims=True)

# Create FAISS index for cosine similarity (via inner product)
dimension = normalized_faq_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)
index.add(normalized_faq_embeddings)

# Search function
def search_faq(query, k=2, threshold=0.7):  # 0.7 is a good starting threshold
    query_vec = model.encode([query], convert_to_numpy=True)
    query_vec = query_vec / np.linalg.norm(query_vec, axis=1, keepdims=True)  # Normalize
    
    scores, indices = index.search(query_vec, k)
    found = False
    
    for score, idx in zip(scores[0], indices[0]):
        if score >= threshold:
            print(f"Q: {faqs[idx]['question']}")
            print(f"A: {faqs[idx]['answer']}")
            print(f"(Cosine similarity: {score:.4f})")
            print("---")
            found = True
    
    if not found:
        print("Sorry, no good match found.")

# Test
search_faq("How to upload many API keys at once?")
