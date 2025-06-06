PRD for ContextFrame exexution 

file → embed → Lance row → search layer → LLM



---


## 1. Set up env

```bash
python -m venv .venv && source .venv/bin/activate
pip install contextframe lance==0.9.3 fastapi uvicorn \
             sentence-transformers tiktoken  # or openai>=1.0.0
```

ContextFrame pulls in Lance for you, but pinning keeps the wheel turning on day-one. ([github.com][1])

---

## 2. Bootstrap an empty dataset (5 min)

```python
# bootstrap.py
from contextframe import FrameDataset
ds = FrameDataset.create("kb.lance", embed_dim=768)   # match your encoder
print("Docset Created", ds._native.uri)
```

---

## 3. One-file ingestion script (1 h)

```python
# ingest.py
from pathlib import Path
import numpy as np, json, uuid, datetime
from sentence_transformers import SentenceTransformer
from contextframe import FrameRecord, FrameDataset, RecordType

MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
DS    = FrameDataset.open("kb.lance")

def embed(text:str)->np.ndarray:
    return MODEL.encode([text])[0].astype(np.float32)

root = Path("docs/")
for f in root.rglob("*.md"):
    text = f.read_text()
    rec  = FrameRecord.create(
        title    = f.name,
        content  = text,
        vector   = embed(text),
        tags     = [f.suffix.lstrip(".")],
        source_file=str(f),
        record_type=RecordType.DOCUMENT,
    )
    DS.add(rec)
print("✅ Ingested", DS.count(), "records")
```

*No chunking yet—each file = 1 row. Good enough to prove the flow, but long term we prob want chunking.

---

## 4. Build the thin search layer

```python
# app.py
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np, uvicorn
from contextframe import FrameDataset
from sentence_transformers import SentenceTransformer

app  = FastAPI()
DS   = FrameDataset.open("kb.lance")
ENC  = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

class Query(BaseModel):
    q: str
    k: int = 4

@app.post("/query")
def query(body: Query):
    vec  = ENC.encode([body.q])[0].astype(np.float32)
    hits = DS.knn_search(vec, k=body.k)
    return [
        {"title": r.title,
         "snippet": r.content[:200]+"…",
         "score": r.metadata["score"]}
        for r in hits
    ]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

`knn_search` and `full_text_search` are ready-made helpers in FrameDataset, so you avoid raw SQL. ([github.com][1])

---

## 5. Wire in LLM

```python
import openai, os, requests
def ask_llm(question:str):
    ctx = requests.post("http://localhost:8000/query",
                        json={"q": question, "k": 4}).json()
    system = "You are a helpful assistant."
    docs   = "\n\n".join([f"{i+1}. {c['snippet']}" for i,c in enumerate(ctx)])
    prompt = f"Answer using these docs:\n{docs}\n\nQ: {question}\nA:"
    rsp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":system},
                  {"role":"user","content":prompt}]
    )
    return rsp.choices[0].message.content
```


