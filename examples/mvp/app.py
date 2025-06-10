from fastapi import FastAPI
from pydantic import BaseModel
from contextframe.frame import FrameDataset
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
    # For MVP with small dataset, let's compute similarity manually
    vec = ENC.encode([body.q])[0].astype(np.float32)
    
    # Get all records as pandas dataframe
    df = DS.to_pandas()
    
    # Compute cosine similarity for each record
    results = []
    for idx in range(len(df)):
        record = df.iloc[idx]
        # Get the vector and convert to numpy array
        record_vec = np.array(record['vector'], dtype=np.float32)
        
        # Compute cosine similarity
        similarity = np.dot(vec, record_vec) / (np.linalg.norm(vec) * np.linalg.norm(record_vec))
        
        results.append({
            'title': record['title'],
            'snippet': record['text_content'][:200] + "…" if len(record['text_content']) > 200 else record['text_content'],
            'score': float(similarity),
        })
    
    # Sort by score and return top k
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:body.k]

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
