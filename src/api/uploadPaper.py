from fastapi import APIRouter, UploadFile, File, HTTPException
from src.services.pdf_processor import extract_text_with_sections
from src.services.embedding_service import get_embeddings
from src.services.qdrant_client import upsert_vectors
import uuid, time, os
from src.services.connectMongoDB import papers_collection


router = APIRouter()
@router.post("/papers/upload")
async def upload_paper(file: UploadFile = File(...)):
    temp_file = f"temp_{uuid.uuid4()}.pdf"
    result = None
    points = []

    try:
        with open(temp_file, "wb") as f:
            f.write(await file.read())

        sections,paper_title = extract_text_with_sections(temp_file)
        if not sections:
            raise ValueError("No sections found in the PDF.")

        text_chunks = [s["text"] for s in sections]
        metadata_list = [{"section": s["section"], "page": s["page"]} for s in sections]

        embeddings = get_embeddings(text_chunks)
        if not embeddings:
            raise ValueError("No embeddings generated.")

        expected_dim = len(embeddings[0])
        if any(len(e) != expected_dim for e in embeddings):
            raise ValueError("Inconsistent embedding dimensions.")

        paper_doc = {
            "filename": file.filename,
            "sections": metadata_list,
            "embedding_dim": expected_dim,
            "createdAt": time.time(),
            "title": paper_title
        }
        result = await papers_collection.insert_one(paper_doc)
        paper_id = str(result.inserted_id)

        points = [
            {
                "id": str(uuid.uuid4()),
                "vector": emb,
                "payload": {
                    "paper_id": paper_id,
                    "title": file.filename,
                    "text": text_chunks[i],
                    "title": paper_title,
                    "section": meta["section"],
                    "page": meta["page"],
                },
            }
            for i, (emb, meta) in enumerate(zip(embeddings, metadata_list))
        ]

        upsert_vectors(points)
        print(f"Uploaded {len(points)} vectors to Qdrant for paper_id={paper_id}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    return {
        "status": "success",
        "paper_id": str(result.inserted_id),
        "uploaded_points": len(points),
    }
