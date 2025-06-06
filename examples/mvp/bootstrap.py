import argparse
from contextframe import FrameDataset

def main():
    parser = argparse.ArgumentParser(description="Bootstrap an empty Lance dataset for ContextFrame MVP.")
    parser.add_argument("path", type=str, help="Output Lance dataset directory (should end with .lance)")
    parser.add_argument("--embed-dim", type=int, default=768, help="Embedding vector dimension (default: 768)")
    args = parser.parse_args()

    ds = FrameDataset.create(args.path, embed_dim=args.embed_dim)
    print(f"Created Lance dataset: {ds._dataset.uri} [dim={args.embed_dim}]")

if __name__ == "__main__":
    main()
