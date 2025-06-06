# ContextFrame MVP - Quickstart

Follow these steps to run the full MVP pipeline (file → embed → Lance → fastapi search → LLM):

## Quick Start (5 minutes)

```bash
# Clone and setup
cd examples/mvp
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Create dataset and ingest docs
python bootstrap.py kb.lance
python ingest.py --docs sample_docs --dataset kb.lance

# Start search API (new terminal)
uvicorn app:app --reload

# Test LLM integration (new terminal)
export OPENAI_API_KEY=sk-...
python llm_integration.py
# Try: "What is ContextFrame?"
```

## Detailed Steps

### 1. Install dependencies

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Bootstrap an empty Lance dataset

```bash
python bootstrap.py kb.lance --embed-dim 384  # Use 384 for all-MiniLM-L6-v2
```

### 3. Ingest sample markdown documents
Sample test docs live in `sample_docs/` (add your own as .md for more variety).

```bash
python ingest.py --docs sample_docs --dataset kb.lance
```

### 4. Run the similarity search API

```bash
uvicorn app:app --reload
```
POST to `http://localhost:8000/query` with JSON: `{ "q": "my question", "k": 4 }`

### 5. LLM Integration Demo

Requires the OpenAI API key as `OPENAI_API_KEY` env var.

```bash
export OPENAI_API_KEY=sk-...
python llm_integration.py
```

---

## File/Script Overview
- `bootstrap.py` : creates a new Lance dataset with given embedding dimension
- `ingest.py`    : batch-ingests markdown docs and stores them with embeddings
- `app.py`       : FastAPI server for similarity search via SentenceTransformers
- `llm_integration.py` : demo script for OpenAI Retrieval-Augmented QA
- `requirements.txt`   : all package pins for quick setup
- `sample_docs/`       : drop your .md files here to experiment

---

## Success Criteria
- Can initialize and ingest documents
- Can query over embeddings
- Can return context to LLM for QA
