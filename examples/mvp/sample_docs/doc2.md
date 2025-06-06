# Working with FrameRecords

FrameRecords are the core data structure in ContextFrame. Each record represents a document or piece of content with its associated vector embedding and metadata.

## Creating Records

To create a new FrameRecord, use the `create()` method:

```python
from contextframe import FrameRecord, RecordType
import numpy as np

record = FrameRecord.create(
    title="My Document",
    content="This is the document content",
    vector=np.array([0.1, 0.2, 0.3], dtype=np.float32),
    tags=["tutorial", "example"],
    record_type=RecordType.DOCUMENT
)
```

## Record Fields

### Required Fields
- **id**: Unique identifier (auto-generated if not provided)
- **title**: Human-readable title
- **content**: Main text content
- **vector**: Embedding vector as numpy array
- **record_type**: Type classification (DOCUMENT, SNIPPET, etc.)

### Optional Fields
- **tags**: List of string tags for categorization
- **metadata**: Dictionary of additional properties
- **source_file**: Original file path
- **created_at**: Timestamp (auto-generated)
- **updated_at**: Timestamp (auto-updated)

## Best Practices

1. **Consistent Embeddings**: Always use the same model for generating vectors
2. **Meaningful Titles**: Use descriptive titles for better search results
3. **Rich Metadata**: Include relevant metadata for filtering
4. **Appropriate Types**: Choose the correct RecordType for your content

## Vector Search

Once records are added to a FrameDataset, you can search using vector similarity:

```python
results = dataset.knn_search(query_vector, k=5)
for record in results:
    print(f"{record.title}: {record.metadata.get('score', 0)}")
```

The search returns the k most similar records based on vector distance.