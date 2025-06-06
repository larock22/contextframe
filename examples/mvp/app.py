from fastapi import FastAPI
from pydantic import BaseModel
from contextframe import FrameDataset
from sentence_transformers import SentenceTransformer
import numpy as np
import uvicorn

app = FastAPI()
DS = FrameDataset.open("./kb.lance")
ENC = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class Query(BaseModel):
    q: str
    k: int = 4

@app.post("/query")
def query(body: Query):
    vec = ENC.encode([body.q])[0].astype(np.float32)
    hits = DS.knn_search(vec, k=body.k)
    return [
        {
            "title": getattr(r, "title", r.metadata.get('title', '')),  # fallback for title
            "snippet": getattr(r, "content", getattr(r, "text_content", ""))[:200] + "…",
            "score": r.metadata.get("score", None),
        }
        for r in hits
    ]

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
