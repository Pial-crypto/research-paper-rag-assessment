from sentence_transformers import SentenceTransformer

# Load model once
model = SentenceTransformer("all-mpnet-base-v2")  # 768-dim



def get_embeddings(text_list):
    """
    Input: list of strings
    Output: list of vectors
    """
    return model.encode(text_list, show_progress_bar=False).tolist()
