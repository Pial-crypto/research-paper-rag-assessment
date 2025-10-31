
## 1. Chunking Strategy

### Why Chunking
Large academic papers often exceed LLM context limits. To ensure relevant retrieval and efficient embedding generation, documents are divided into smaller, semantically meaningful chunks.

### Approach
- Extract section-wise text using **PyMuPDF**.
- Split each section into chunks of ~500 tokens with a 50-token overlap.
- Store section name, page number, and chunk text for each vector.

### Benefits
- Maintains contextual consistency within sections.
- Improves retrieval accuracy during semantic search.
- Prevents exceeding model context window.

---

## 2. Embedding Model Choice

**Model:** `text-embedding-3-large` (OpenAI)

**Reasoning:**
- High performance for academic and research-based language.
- Excellent cosine similarity stability.
- Well-suited for large-scale document databases.

**Alternatives:**
- `text-embedding-3-small` for lower cost.
- `all-MiniLM-L6-v2` (SentenceTransformers) for offline inference.

---

## 3. Prompt Engineering

**Template Used:**
You are a research assistant.
Answer the following question using only the provided context.

Context:
{{context}}

Question:
{{question}}

Answer concisely with supporting details from the text.


**Why This Works:**
- Prevents hallucination by forcing grounded responses.
- Keeps answers concise and focused.
- Encourages citation from retrieved sections.

---

## 4. Database Schema Design

### MongoDB (Metadata)
```json
{
  "_id": "ObjectId",
  "filename": "example.pdf",
  "sections": [
    {"section": "Introduction", "page": 1},
    {"section": "Methodology", "page": 5}
  ],
  "embedding_dim": 768,
  "createdAt": 1730421801.23
}

{
  "id": "uuid",
  "vector": [0.12, 0.44, 0.67, ...],
  "payload": {
    "paper_id": "69027a506731215ddf96f980",
    "title": "AI Research",
    "section": "Abstract",
    "page": 1,
    "text": "This paper introduces a new model for..."
  }
}

5. Trade-offs and Limitations
Component	Trade-off	Description
Chunk Size	Too small = loss of context	Too large = poor retrieval precision
Embedding Source	OpenAI = accurate but paid	SentenceTransformer = free but less accurate
Storage	Mongo + Qdrant	Dual-layer adds complexity but scales better
Retrieval	Based on cosine similarity	May miss long-range dependencies
Latency	Network + embedding call overhead	Can be optimized via caching


6. Future Improvements

Add reranking layer using cosine thresholds.

Implement multi-paper context merging.

Add query caching for frequent questions.

Enable in-text citation references in answers.

Integrate fine-tuned domain prompts.

6. Future Improvements

Add reranking layer using cosine thresholds.

Implement multi-paper context merging.

Add query caching for frequent questions.

Enable in-text citation references in answers.

Integrate fine-tuned domain prompts.

