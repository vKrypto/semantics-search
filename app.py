from sentence_transformers import SentenceTransformer
from faqs import FAQData
import faiss
import numpy as np


# Step 1: Sample FAQs
faq_data = FAQData()
faqs = faq_data.faqs
questions = faq_data.get_questions()

# Step 2: Generate Embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Converting questions to vectors
embeddings = model.encode(questions, convert_to_numpy=True)

# Step 3: Create FAISS index and store embeddings
# By default the dimension is 384
# Shape: (3, 384) 3 questions 384 dimensions
dimension = embeddings.shape[1] #384

# Creating index
# Using L2 (Euclidean) distance, ANN can also be used for large db
# l2 is a measure of dissimalrity - so distance <= threshold = good match
# IndexIVF will be used for that
index = faiss.IndexFlatL2(dimension)

# Adding vectors in db.
index.add(embeddings)

# Save index and questions for reuse
# Storing in disk so no need to create everytime
faiss.write_index(index, "faq_index.faiss")
np.save("faq_questions.npy", questions, allow_pickle=True)

# Step 4: Perform Semantic Search on a new query
def search_faq(query, k=2, threshold=0.65):
    '''
        k: Number of top matching vectors to be returned
        threshold: max distance allowed
        smaller distance = better match
        query_vec: 384 dimension user query vector
        D: distance b/w user vector and matched faq vector
        A 2D numpy array (i,j) i = number of queries 
        I: indices of matched questions from original dict.
        FAISS returns 2-D array even for one query
        zip - pairs up the element of two list
    '''
    # Encoding user query - multiple queries can be sent as it takes list as input
    query_vec = model.encode([query])

    # Distance and index of the matching vectors 
    D, I = index.search(query_vec, k)
    # for idx in I[0]:
    #     print(f"Q: {faqs[idx]['question']}")
    #     print(f"A: {faqs[idx]['answer']}")
    #     print("---")
    any_match = False

    for distance, idx in zip(D[0], I[0]):
        if distance <= threshold:
            print(f"Q: {faqs[idx]['question']}")
            print(f"A: {faqs[idx]['answer']}")
            print(f"(Distance: {distance:.4f})")
            print("---")
            any_match = True
    
    if not any_match:
        print('Please connect to support team')

# Test query
# search_faq("How to upload multiple API keys?")
search_faq("I'm unable to store multiple keys at once, What to do?")

