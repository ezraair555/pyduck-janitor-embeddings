#!/usr/bin/env python3
"""Fetch embedding model weights into the companion wheel's data dir.

Run this before building the wheel so the weights ship with the
package. Without this step, the wheel contains only the metadata
files; the user has to call ``pyduck_janitor.embed_install()`` to
fetch from HuggingFace at first use.

Usage:
    python scripts/fetch_models.py
    python -m build   # then upload to PyPI

License attribution: each bundled model gets a NOTICE file inside
its data dir naming the model, the upstream URL, the license, and a
copy of the upstream LICENSE when one is available on the Hub.
This keeps the redistribution trail auditable inside the wheel.
"""

from __future__ import annotations

import sys
from pathlib import Path
from urllib.request import urlopen

# Models to bundle. Add to this list to include more.
# (huggingface_repo_id, display_name, license, license_filename)
MODELS = [
    (
        "sentence-transformers/all-MiniLM-L6-v2",
        "sentence-transformers/all-MiniLM-L6-v2",
        "Apache-2.0",
        "LICENSE",
    ),
    # ("BAAI/bge-small-en-v1.5", "BAAI/bge-small-en-v1.5", "MIT", "LICENSE"),
]

APACHE_LICENSE_URL = "https://www.apache.org/licenses/LICENSE-2.0.txt"


def fetch(model_id: str, target_root: Path) -> Path:
    from huggingface_hub import snapshot_download

    slug = model_id.replace("/", "__").replace("@", "_at_")
    target = target_root / slug
    if target.exists():
        print(f"  already present: {target}")
        return target

    target.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {model_id} -> {target}")
    snapshot_download(
        repo_id=model_id,
        local_dir=str(target),
        local_dir_use_symlinks=False,
        allow_patterns=[
            "*.json",
            "*.txt",
            "*.safetensors",
            "tokenizer.*",
            "vocab.*",
            "merges.txt",
            "special_tokens_map.json",
            "LICENSE",
            "LICENSE.*",
            "NOTICE",
            "NOTICE.*",
        ],
    )
    # Some Hub repos declare Apache-2.0 without committing a LICENSE file.
    # Keep the redistribution trail complete inside the wheel.
    license_path = target / "LICENSE"
    if not license_path.exists():
        with urlopen(APACHE_LICENSE_URL, timeout=30) as response:
            license_path.write_bytes(response.read())
    return target


def write_notice(
    target: Path, display_name: str, license_name: str, license_filename: str | None
) -> None:
    """Write a NOTICE file naming the upstream source and license."""
    upstream_url = f"https://huggingface.co/{display_name}"
    text = (
        f"This directory contains model weights redistributed from\n"
        f"  {upstream_url}\n\n"
        f"Model: {display_name}\n"
        f"License: {license_name}\n"
    )
    if license_filename is not None:
        text += (
            f"\nThe full upstream LICENSE is included in this directory\n"
            f"as '{license_filename}'.\n"
        )
    text += (
        "\npyduck-janitor-embeddings is MIT-licensed. The bundled weights\n"
        "are governed by the upstream license above; redistribution is\n"
        "permitted under the terms of that license.\n"
    )
    (target / "NOTICE").write_text(text)
    print(f"  wrote NOTICE: {target / 'NOTICE'}")


def main() -> int:
    src_root = Path(__file__).resolve().parent.parent
    target_root = (
        src_root / "src" / "pyduck_janitor_embeddings" / "data" / "embeddings"
    )
    target_root.mkdir(parents=True, exist_ok=True)

    for model_id, display, license_name, license_filename in MODELS:
        try:
            target = fetch(model_id, target_root)
            write_notice(target, display, license_name, license_filename)
        except Exception as exc:
            print(f"  FAILED: {model_id}: {exc}", file=sys.stderr)
            return 1
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
