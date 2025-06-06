from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer
from contextframe import FrameRecord, FrameDataset, RecordType

import argparse

def main():
    parser = argparse.ArgumentParser(description="Bulk-ingest markdown files into Lance dataset with embeddings.")
    parser.add_argument("--docs", type=str, default="./sample_docs", help="Directory containing markdown files")
    parser.add_argument("--dataset", type=str, default="./kb.lance", help="Lance dataset path (.lance)")
    parser.add_argument("--model", type=str, default="sentence-transformers/all-MiniLM-L6-v2", help="SentenceTransformer model")
    args = parser.parse_args()

    MODEL = SentenceTransformer(args.model)
    DS = FrameDataset.open(args.dataset)

    def embed(text: str) -> np.ndarray:
        return MODEL.encode([text])[0].astype(np.float32)

    root = Path(args.docs)
    n = 0
    for f in root.rglob("*.md"):
        text = f.read_text(encoding="utf-8")
        rec = FrameRecord.create(
            title = f.name,
            content = text,
            vector = embed(text),
            tags = [f.suffix.lstrip(".")],
            source_file = str(f),
            record_type = RecordType.DOCUMENT,
        )
        DS.add(rec)
        n += 1
        print(f"Ingested: {f}")
    print(f"Ingested {n} documents into {args.dataset}")

if __name__ == "__main__":
    main()
