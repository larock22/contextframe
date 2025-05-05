"""
Context Frame is a file format and toolkit for working with
documents with structured metadata for AI workflows.
"""

# Direct imports for convenience
from .frame import FrameRecord, FrameDataset

# Collection helpers are still applicable (operate via FrameDataset internally)
# from .collection import Collection  # type: ignore  # noqa: E402

# Convenience exports
from .helpers.metadata_utils import create_metadata, get_standard_fields  # noqa: E402
from .schema import get_schema, RecordType, MimeTypes  # noqa: E402

# Define version
__version__ = "0.1.0"

# CLI entry point
def cli():
    """Command-line interface entry point."""
    from .cli import main
    main()

# Public re-exports
__all__ = [
    "FrameRecord",
    "FrameDataset",
    "create_metadata",
    "get_standard_fields",
    "get_schema",
    "RecordType",
    "MimeTypes",
]