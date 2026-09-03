# pyduck-janitor-embeddings

Bundled embedding models for [pyduck-janitor](https://github.com/ezraair555/pyduck-janitor).

This companion wheel ships sentence-transformers model weights inside the
package so `pyduck_janitor.embed_install()` works **without contacting
HuggingFace**. It's the offline install path for air-gapped machines, CI,
and anyone who'd rather not pull weights at first use.

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