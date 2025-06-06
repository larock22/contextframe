# ContextFrame Overview

ContextFrame is a lightweight Python framework for building context-aware applications using vector databases. It provides a simple abstraction layer over Lance, a modern columnar data format optimized for machine learning workloads.

## Key Features

- **Efficient Storage**: Built on Lance format for fast vector similarity search
- **Schema Validation**: Ensures data consistency with built-in validation
- **Type Safety**: Full type hints and runtime validation
- **Flexible Metadata**: Store arbitrary metadata alongside vectors
- **Simple API**: Intuitive methods for common operations

## Architecture

ContextFrame follows a simple architecture pattern:

1. **Data Ingestion**: Load documents and generate embeddings
2. **Storage Layer**: Persist vectors and metadata in Lance format
3. **Search Interface**: Query vectors using similarity search
4. **Result Processing**: Format and return relevant contexts

## Use Cases

- Building RAG (Retrieval Augmented Generation) applications
- Semantic search over document collections
- Question answering systems
- Knowledge base management
- Content recommendation engines

## Getting Started

To use ContextFrame, first install it along with your preferred embedding model:

```bash
pip install contextframe sentence-transformers
```

Then create a dataset and start adding documents with their embeddings.