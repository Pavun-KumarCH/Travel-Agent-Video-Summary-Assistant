# Components/dpr.py

import torch
import numpy as np
import faiss
from transformers import (
    DPRQuestionEncoder,
    DPRContextEncoder,
    DPRQuestionEncoderTokenizer,
    DPRContextEncoderTokenizer
)

# Load DPR Question encoder and tokenizer for the query
query_encoder = DPRQuestionEncoder.from_pretrained("facebook/dpr-question_encoder-single-nq-base")
query_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained("facebook/dpr-question_encoder-single-nq-base")

# Load DPR context encoder and tokenizer for the passages
passage_encoder = DPRContextEncoder.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")
passage_tokenizer = DPRContextEncoderTokenizer.from_pretrained("facebook/dpr-ctx_encoder-single-nq-base")

def encode_passage(video_df):
    """
    Encodes the transcripts using the DPR context encoder.
    """
    passages = video_df['Transcript'].tolist()
    passage_embeddings = []

    for passage in passages:
        # Check if the passage is valid
        if passage.startswith("No transcript") or passage.startswith("Error") or passage.startswith("Invalid"):
            # Assign a zero vector for invalid passages
            embedding = np.zeros(passage_encoder.config.hidden_size)
        else:
            # Tokenize and encode the passage
            inputs = passage_tokenizer(passage, return_tensors='pt', max_length=512, truncation=True, padding=True)
            with torch.no_grad():
                embedding = passage_encoder(**inputs).pooler_output.numpy()
        passage_embeddings.append(embedding)

    # Convert to a Numpy Array
    passage_embeddings = np.vstack(passage_embeddings).astype('float32')

    return passage_embeddings

def faiss_vector_store(passage_embeddings):
    """
    Initializes and populates a FAISS index with passage embeddings.
    """
    dimension = passage_embeddings.shape[1]  # DPR embeddings size is 768
    faiss_index = faiss.IndexFlatIP(dimension)  # Inner Product (dot product) for similarity

    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(passage_embeddings)

    # Add the passage embeddings to the index
    faiss_index.add(passage_embeddings)
    return faiss_index

def search_relevant_passages(video_df, query, faiss_index, top_k=3):
    """
    Searches for the most relevant passages based on the query.
    """
    # Encode the query using the DPR Question encoder
    query_inputs = query_tokenizer(query, return_tensors='pt', max_length=128, truncation=True, padding=True)

    with torch.no_grad():
        query_embedding = query_encoder(**query_inputs).pooler_output.numpy()

    # Normalize the query embedding
    faiss.normalize_L2(query_embedding)

    # Search for the top-k most similar passages
    distances, indices = faiss_index.search(query_embedding.astype('float32'), top_k)

    # Filter the DataFrame based on the retrieved indices
    top_k_indices = indices[0][:top_k]
    top_k_videos = video_df.iloc[top_k_indices].copy()
    top_k_videos['Similarity Score'] = distances[0][:top_k]
    top_k_videos['Query'] = query

    return top_k_videos
