#!/usr/bin/env python3
"""Fetch embedding model weights into the companion wheel's data dir.

Run this before building the wheel so the weights ship with the
package. Without this step, the wheel contains only the metadata
files; the user has to call ``pyduck_janitor.embed_install()`` to
fetch from HuggingFace at first use.

Usage:
    python scripts/fetch_models.py
    python -m build   # then upload to PyPI
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

# Models to bundle. Add to this list to include more.
MODELS = [
    "sentence-transformers/all-MiniLM-L6-v2",
    # "BAAI/bge-small-en-v1.5",
]


def fetch(model: str, target_root: Path) -> Path:
    from huggingface_hub import snapshot_download

    slug = model.replace("/", "__").replace("@", "_at_")
    target = target_root / slug
    if target.exists():
        print(f"  already present: {target}")
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {model} -> {target}")
    snapshot_download(
        repo_id=model,
        local_dir=str(target),
        local_dir_use_symlinks=False,
        allow_patterns=[
            "*.json",
            "*.txt",
            "*.safetensors",
            "*.bin",
            "tokenizer.*",
            "vocab.*",
            "merges.txt",
            "special_tokens_map.json",
        ],
    )
    return target


def main() -> int:
    src_root = Path(__file__).resolve().parent.parent
    target_root = src_root / "src" / "pyduck_janitor_embeddings" / "data" / "embeddings"
    target_root.mkdir(parents=True, exist_ok=True)

    for m in MODELS:
        try:
            fetch(m, target_root)
        except Exception as exc:
            print(f"  FAILED: {m}: {exc}", file=sys.stderr)
            return 1
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
