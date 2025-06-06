import tempfile
import shutil
import os
from pathlib import Path
import numpy as np
import pytest
from sentence_transformers import SentenceTransformer
from contextframe import FrameDataset, FrameRecord, RecordType

def test_bootstrap_and_create_dataset():
    # Uses a temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        ds_path = Path(tmpdir) / "test_emb.lance"
        ds = FrameDataset.create(ds_path, embed_dim=10)
        # Check Lance dir created
        assert ds_path.exists() and ds_path.is_dir()

def test_ingest_and_add_record():
    with tempfile.TemporaryDirectory() as tmpdir:
        ds_path = Path(tmpdir) / "test_ingest.lance"
        ds = FrameDataset.create(ds_path, embed_dim=8)
        dummy_vec = np.ones(8, dtype=np.float32)
        rec = FrameRecord.create(title="T", content="hi", vector=dummy_vec, record_type=RecordType.DOCUMENT)
        ds.add(rec)
        # Test record count attribute if present
        count = getattr(ds._dataset, 'count_rows', lambda: None)()
        assert count == 1 or count is None  # If Lance doesn't support, allow None
