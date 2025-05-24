from sentence_transformers import SentenceTransformer
from faqs import FAQData
import numpy as np
import faiss

# Step 1: Load pretrained model and prepare FAQ data
model = SentenceTransformer('all-MiniLM-L6-v2')

faq_data = FAQData()
faqs = faq_data.faqs
questions = faq_data.get_questions()

# Convert FAQs to embeddings (vectors)
# 3 questions converted to 384 numbers
faq_embeddings = model.encode(questions, convert_to_numpy=True)

# Step 2: Build a FAISS Index (IVF for ANN)
# No of columns = 384
dimension = faq_embeddings.shape[1]  

# small number for demo
# dividing the vector spave into 3 buckets(cluster)
n_clusters = 3  

# base index for clustering
quantizer = faiss.IndexFlatL2(dimension)

# grouping similar vectors together in a cluster of 3
# distance will be measured by L2 
index = faiss.IndexIVFFlat(quantizer, dimension, n_clusters, faiss.METRIC_L2)

# Train the index with the FAQs
# learns data structure using k-means first
# needed for IVF indices
index.train(faq_embeddings)  
index.add(faq_embeddings)

# Step 3: Encode a new query
query = "I'm unable to store multiple keys at once, What to do?"
query_embedding = model.encode([query], convert_to_numpy=True)

# Step 4: Perform approximate nearest neighbor search
k = 4  # number of nearest neighbors to return
distances, indices = index.search(query_embedding, k)

# Step 5: Apply threshold logic
L2_THRESHOLD = 0.75 
matched_index = indices[0][0]
matched_distance = distances[0][0]

if matched_distance <= L2_THRESHOLD:
    print(f"Match found: \n\"{faqs[matched_index]['question']}\"\n Answer: {faqs[matched_index]['answer']}\n(Distance: {matched_distance:.4f})")
else:
    print(f"No close match. Closest was: \"{questions[matched_index]}\" (Distance: {matched_distance:.4f})")
