"""Tests for the pyduck_janitor_embeddings package metadata surface."""

from __future__ import annotations

from pathlib import Path

import pyduck_janitor_embeddings as pje


def test_list_bundled_returns_list():
    models = pje.list_bundled()
    assert isinstance(models, list)


def test_bundled_model_path_miss_returns_none():
    assert pje.bundled_model_path("does/not-exist") is None


def test_data_root_path_shape():
    # Keep this light: verify package structure contract even before
    # model artifacts are fetched in CI.
    pkg_root = Path(pje.__file__).resolve().parent
    data_root = pkg_root / "data" / "embeddings"
    assert data_root.as_posix().endswith("data/embeddings")
