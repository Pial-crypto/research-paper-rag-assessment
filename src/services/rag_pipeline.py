import requests
from openai import OpenAI
from src.services.embedding_service import get_embeddings
from src.services.qdrant_client import search_vector
from src.config import LLM_MODE, OPENAI_API_KEY, DEEPSEEK_API_KEY


def answer_query(question, top_k=5, paper_ids=None):
    """
    Answer a query by:
    1. Embedding the question
    2. Searching Qdrant for relevant contexts
    3. Generating an answer via Ollama / DeepSeek / OpenAI
    Returns:
    {
        "answer": "...",
        "citations": [...],
        "sources_used": [...],
        "confidence": 0.85
    }
    """
    # 🧠 Step 1: Embed the question
    q_vec = get_embeddings([question])[0]

    # 🧩 Step 2: Retrieve relevant context from Qdrant
    results = search_vector(q_vec, top_k=top_k)
    context, citations, sources_used = "", [], set()

    for r in results:
        payload = r.payload
        if paper_ids and payload.get("paper_id") not in paper_ids:
            continue
        context += payload.get("text", "") + "\n"
        citations.append({
            "paper_title": payload.get("title", "Unknown"),
            "section": payload.get("section", "Other"),
            "page": payload.get("page", -1),
            "relevance_score": r.score
        })
        sources_used.add(payload.get("title", "Unknown"))

    # 🧠 Step 3: Choose LLM model
    prompt = f"""You are a helpful research assistant.
Answer the question using only the given context.
If context is insufficient, say 'Not enough information.'

Context:
{context}

Question: {question}
Answer:"""

    answer = None

    # --- LLM OPTION 1: Ollama (Local) ---
    if LLM_MODE.lower() == "ollama":
        try:
            resp = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "deepseek-r1", "prompt": prompt},
                timeout=60
            )
            answer = resp.json().get("response", "").strip()
        except Exception as e:
            answer = f"Ollama LLM not available ({e})"

    # --- LLM OPTION 2: DeepSeek API ---
    elif LLM_MODE.lower() == "deepseek":
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.4,
                },
                timeout=60,
            )
            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
        except Exception as e:
            answer = f"DeepSeek API error: {e}"

    # --- LLM OPTION 3: OpenAI ---
    elif LLM_MODE.lower() == "openai":
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            answer = response.choices[0].message.content.strip()
        except Exception as e:
            answer = f"OpenAI API error: {e}"

    else:
        answer = "LLM not configured properly."

    # 🧾 Step 4: Return full response
    return {
        "answer": answer,
        "citations": citations,
        "sources_used": list(sources_used),
        "confidence": 0.85
    }
