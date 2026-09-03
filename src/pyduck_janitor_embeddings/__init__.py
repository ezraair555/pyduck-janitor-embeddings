"""Bundled embedding models for pyduck-janitor.

This companion wheel packages sentence-transformers model weights
inside ``pyduck_janitor_embeddings.data.embeddings.<slug>/`` so
they can be installed into the local cache without contacting
HuggingFace Hub.

Models bundled:
  - sentence-transformers/all-MiniLM-L6-v2  (default, 384-dim, ~90MB)

To populate this directory during build, run:
    python scripts/fetch_models.py
from the repository root.
"""

from __future__ import annotations

from pathlib import Path

_PACKAGE_ROOT = Path(__file__).resolve().parent
_DATA_ROOT = _PACKAGE_ROOT / "data" / "embeddings"

# Models bundled in this wheel. Slug -> display name.
BUNDLED_MODELS: dict[str, str] = {
    "sentence-transformers__all-MiniLM-L6-v2": "sentence-transformers/all-MiniLM-L6-v2",
}


def bundled_model_path(model: str) -> Path | None:
    """Resolve a bundled model directory by display name.

    Returns None when the requested model isn't bundled.
    """
    slug = model.replace("/", "__").replace("@", "_at_")
    candidate = _DATA_ROOT / slug
    if candidate.exists():
        return candidate
    return None


def list_bundled() -> list[str]:
    """Return the display names of all bundled models."""
    if not _DATA_ROOT.exists():
        return []
    out: list[str] = []
    for entry in sorted(_DATA_ROOT.iterdir()):
        if entry.is_dir():
            slug = entry.name
            display = BUNDLED_MODELS.get(slug, slug.replace("__", "/"))
            out.append(display)
    return out
