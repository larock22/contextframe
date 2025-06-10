from pathlib import Path
import argparse
from contextframe.frame import FrameRecord, FrameDataset
from contextframe.helpers import get_embedding_model, get_embed_dim_for_model
from contextframe.schema import RecordType

def main():
    parser = argparse.ArgumentParser(description="Bulk-ingest markdown files into Lance dataset with embeddings.")
    parser.add_argument("--docs", type=str, default="./sample_docs", help="Directory containing markdown files")
    parser.add_argument("--dataset", type=str, required=True, help="Path to Lance dataset")
    parser.add_argument("--model", type=str, default="all-MiniLM-L6-v2", help="SentenceTransformer model name")
    args = parser.parse_args()

    ds = FrameDataset.open(args.dataset)
    model_name = f"sentence-transformers/{args.model}" if not args.model.startswith("sentence-transformers/") else args.model
    model = get_embedding_model(model_name)
    embed_dim = get_embed_dim_for_model(model_name)

    root = Path(args.docs)
    n_ingested = 0
    for path in root.glob("**/*.md"):
        print(f"Ingesting {path}...")
        content = path.read_text(encoding="utf-8")
        title = path.stem

        rec = FrameRecord.create(
            title=title,
            content=content,
            vector=model.encode(content),
            embed_dim=embed_dim,
            tags=[path.suffix.lstrip(".")],
            source_url=path.resolve().as_uri(),
            record_type=RecordType.DOCUMENT,
        )
        ds.add(rec)
        n_ingested += 1

    print(f"Ingested {n_ingested} documents into {ds._dataset.uri}")

if __name__ == "__main__":
    main()
