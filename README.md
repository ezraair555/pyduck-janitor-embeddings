# pyduck-janitor-embeddings

[![PyPI version](https://img.shields.io/pypi/v/pyduck-janitor-embeddings.svg)](https://pypi.org/project/pyduck-janitor-embeddings/)
[![Python versions](https://img.shields.io/pypi/pyversions/pyduck-janitor-embeddings.svg)](https://pypi.org/project/pyduck-janitor-embeddings/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/ezraair555/pyduck-janitor-embeddings/actions/workflows/ci.yml/badge.svg)](https://github.com/ezraair555/pyduck-janitor-embeddings/actions/workflows/ci.yml)

Bundled embedding models for [pyduck-janitor](https://github.com/ezraair555/pyduck-janitor).

This companion wheel ships sentence-transformers model weights inside the
package so `pyduck_janitor.embed_install()` works **without contacting
HuggingFace**. It's the offline install path for air-gapped machines, CI,
and anyone who'd rather not pull weights at first use.

## License

- The companion wheel's code (this `pyduck_janitor_embeddings/` package) is **MIT**, matching the parent `pyduck-janitor`.
- The bundled model weights are redistributed under their **upstream license** (Apache 2.0 for `all-MiniLM-L6-v2`); a `NOTICE` file inside each model directory documents the source URL and full attribution.
- See `data/embeddings/<slug>/NOTICE` inside the installed wheel for the per-model trail.

## Install

```bash
# Recommended — pulls the companion wheel + sentence-transformers
pip install pyduck-janitor[embeddings]

# Or install this wheel directly
pip install pyduck-janitor-embeddings
```

## Use

```python
import pyduck_janitor as pj

# Copies the bundled weights to the local cache. No network.
pj.embed_install()

# Inspect
pj.embed_list_installed()
```

## Models bundled

| Model | Dim | Size | License |
|---|---|---|---|
| `sentence-transformers/all-MiniLM-L6-v2` | 384 | ~90 MB | Apache 2.0 |

Model weights are redistributed under their original licenses; see
`data/embeddings/<model>/LICENSE` inside the wheel for the full text.

## Want a different model?

The bundled default is fine for most tasks, but `pyduck_janitor.embed_install`
accepts any sentence-transformers-compatible model from HuggingFace Hub:

```python
import pyduck_janitor as pj

pj.embed_install("hf:BAAI/bge-small-en-v1.5")               # better quality
pj.embed_install("hf:intfloat/multilingual-e5-small")      # multilingual
pj.embed_install("hf:org/model@sha256:abc123...")           # pinned revision
pj.embed_install("/opt/models/my-finetuned-encoder")        # local path
```

For gated/private models, set `HF_TOKEN` in your environment. See the
parent project's README for the full guide.

## Rebuilding the wheel (maintainers)

The weights are **not** committed to git. To populate them before a build:

```bash
pip install -e ".[build]"
python scripts/fetch_models.py   # downloads into src/.../data/embeddings/
python -m build                  # wheel now carries the weights
```

## Why a separate wheel?

`pyduck-janitor` stays small (~50 KB) so users who only need the icu/fts
text verbs don't download 90 MB of model weights. This companion package
is only pulled when you ask for embeddings — via the `[embeddings]` extra
or an explicit install.