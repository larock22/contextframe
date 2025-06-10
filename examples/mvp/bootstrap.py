import argparse
from contextframe.frame import FrameDataset
from contextframe.helpers import get_embedding_model, get_embed_dim_for_model

def main():
    parser = argparse.ArgumentParser(description="Bootstrap an empty Lance dataset for ContextFrame MVP.")
    parser.add_argument("path", type=str, help="Output Lance dataset directory (should end with .lance)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite if dataset exists")
    args = parser.parse_args()

    model_name = "sentence-transformers/all-MiniLM-L6-v2"
    model = get_embedding_model(model_name)
    embed_dim = get_embed_dim_for_model(model_name)

    ds = FrameDataset.create(args.path, embed_dim=embed_dim, overwrite=args.overwrite)
    print(f"Created Lance dataset: {ds._dataset.uri} [dim={embed_dim}]")

if __name__ == "__main__":
    main()
