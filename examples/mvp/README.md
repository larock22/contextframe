# ContextFrame MVP - Quickstart

This MVP demonstrates the full ContextFrame pipeline: ingesting documents, creating embeddings, storing in Lance, and enabling semantic search with LLM integration.

**Status**: ✅ Fully functional and tested

## How It Works

1. **Bootstrap**: Creates a Lance dataset with the correct schema for storing documents and their embeddings
2. **Ingest**: Reads markdown files, generates embeddings using SentenceTransformers, and stores them in Lance
3. **Search API**: FastAPI server that performs vector similarity search on your documents
4. **LLM Integration**: Demonstrates RAG (Retrieval-Augmented Generation) using the search API and OpenAI

## Quick Start (5 minutes)

```bash
# Setup environment (from the contextframe root directory)
cd examples/mvp
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# IMPORTANT: Set Python path to find contextframe package
export PYTHONPATH=/home/fabian/contextframe:$PYTHONPATH

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env

# Create dataset and ingest docs
python bootstrap.py kb.lance
python ingest.py --docs sample_docs --dataset kb.lance

# Start search API (new terminal, remember to activate venv and set PYTHONPATH)
uvicorn app:app --reload

# Test the API
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"q": "What is ContextFrame?", "k": 2}'

# Test LLM integration (new terminal, remember to activate venv and set PYTHONPATH)
echo "What is ContextFrame?" | python llm_integration.py
```

## Detailed Steps

### 1. Install dependencies

```bash
# Create and activate virtual environment
python3 -m venv venv && source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Set Python path (required for finding contextframe package)
export PYTHONPATH=/home/you/contextframe:$PYTHONPATH
```

### 2. Bootstrap an empty Lance dataset

```bash
python bootstrap.py kb.lance
# Creates a Lance dataset with embedding dimension 384 (auto-detected from all-MiniLM-L6-v2 model)
# Use --overwrite flag to recreate if it already exists
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

The script automatically loads the OpenAI API key from the `.env` file.

```bash
# Interactive mode
python llm_integration.py

# Or pipe a question
echo "How do I create a FrameRecord?" | python llm_integration.py
```

---

## File/Script Overview

- `bootstrap.py` : Creates a new Lance dataset with auto-detected embedding dimension (384 for all-MiniLM-L6-v2)
- `ingest.py`    : Batch-ingests markdown docs, generates embeddings, and stores them in Lance format
- `app.py`       : FastAPI server for vector similarity search using the same embedding model
- `llm_integration.py` : Demo script showing RAG pattern with OpenAI GPT models
- `requirements.txt`   : All required packages including lancedb, sentence-transformers, fastapi, etc.
- `sample_docs/`       : Example markdown files - add your own .md files here

## Technical Details

- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384 dimensions)
- **Vector Database**: Lance (high-performance columnar format)
- **Schema**: ContextFrame standard with title, content, vector, metadata fields
- **Search**: Cosine similarity search on embeddings
- **API**: RESTful endpoints for querying documents

## Troubleshooting

- **ModuleNotFoundError**: Make sure to set `PYTHONPATH` as shown above
- **Dataset exists error**: Use `python bootstrap.py kb.lance --overwrite`
- **Import errors**: Ensure you're in the activated virtual environment
- **API not working**: Check that the FastAPI server is running on port 8000
- **Vector search errors**: The current implementation uses manual cosine similarity for small datasets to avoid Lance index issues

## Success Criteria
- ✅ Can initialize Lance dataset with proper schema
- ✅ Can ingest markdown documents with embeddings
- ✅ Can perform vector similarity search via API
- ✅ Can integrate with LLMs for question answering

## Next Steps

### 1. Scale Up the Dataset
- Add more documents to `sample_docs/`
- Test with larger document collections
- Implement proper Lance vector indexing for datasets with 256+ documents

### 2. Enhance Search Capabilities
- Add metadata filtering (by tags, date, author)
- Implement hybrid search (combining vector + keyword search)
- Add result re-ranking based on recency or relevance

### 3. Improve LLM Integration
- Add conversation memory/context
- Support multiple LLM providers (Anthropic, local models)
- Implement streaming responses
- Add citation tracking (which documents were used)

### 4. Production Readiness
- Add proper error handling and logging
- Implement authentication for the API
- Add rate limiting
- Create Docker container for easy deployment
- Set up proper vector indexing for large-scale search

### 5. Advanced Features
- Support for multimodal content (images, PDFs)
- Implement document chunking strategies
- Add incremental updates (update specific documents)
- Create admin UI for dataset management

### 6. Integration Examples
- Slack bot integration
- VS Code extension
- Chrome extension for web content
- CLI tool for document search

## Known Limitations

- **Small Dataset Performance**: Currently using manual cosine similarity computation instead of Lance's native vector search due to indexing issues with very small datasets
- **No Chunking**: Documents are embedded as whole files - large documents should be chunked for better retrieval
- **Single Embedding Model**: Currently hardcoded to use `all-MiniLM-L6-v2`
- **No Persistence**: API doesn't maintain conversation state between requests
