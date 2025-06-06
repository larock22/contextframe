import tempfile
from pathlib import Path
import numpy as np
import shutil
from contextframe import FrameDataset, FrameRecord, RecordType
from sentence_transformers import SentenceTransformer

def test_full_pipeline():
    with tempfile.TemporaryDirectory() as tmpdir:
        ds_path = Path(tmpdir) / "test_e2e.lance"
        ds = FrameDataset.create(ds_path, embed_dim=16)

        # Use sentence-transformers to embed two small docs
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        doc1 = "The quick brown fox."
        doc2 = "Jumps over the lazy dog."

        rec1 = FrameRecord.create(title="Doc1", content=doc1, vector=model.encode([doc1])[0][:16].astype(np.float32), record_type=RecordType.DOCUMENT)
        rec2 = FrameRecord.create(title="Doc2", content=doc2, vector=model.encode([doc2])[0][:16].astype(np.float32), record_type=RecordType.DOCUMENT)
        ds.add(rec1)
        ds.add(rec2)

        # Search in vector space for "quick"
        search_vec = model.encode(["quick"])[0][:16].astype(np.float32)
        hits = ds.knn_search(search_vec, k=1)
        assert any("quick" in getattr(h, "content", getattr(h, "text_content", "")) for h in hits)
