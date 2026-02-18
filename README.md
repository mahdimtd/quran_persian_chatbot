# Quran Persian Chatbot

A Persian Quran question-answering chatbot built with a Retrieval-Augmented Generation (RAG) pipeline using LlamaIndex, ChromaDB, and OpenRouter.

## Features
- Modular and maintainable Python package in `src/`
- Vector index generation from Quran interpretation text files
- Interactive terminal chat mode
- Environment-based configuration
- Basic tests and CI workflow included

## Project Structure
```text
.
├── src/quran_persian_chatbot/
│   ├── cli.py
│   ├── config.py
│   ├── indexing.py
│   ├── prompting.py
│   └── rag.py
├── tests/
├── data/
├── artifacts/
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── .env.example
```

## Requirements
- Python 3.10+
- `uv` (optional, recommended)
- OpenRouter API key

## Setup
1. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

2. Install dependencies:
```bash
uv pip install -r requirements-dev.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Set OPENROUTER_API_KEY in .env
```

## Build the Index
If you already have `data/majmaolbayan.txt` and `data/alborhan.txt`:
```bash
PYTHONPATH=src python -m quran_persian_chatbot build-index --data-dir data --persist-dir artifacts/chroma_index
```

If you want to download the default data files automatically:
```bash
PYTHONPATH=src python -m quran_persian_chatbot build-index --download-default-data
```

## Run Chat
```bash
PYTHONPATH=src python -m quran_persian_chatbot chat --persist-dir artifacts/chroma_index
```

Type `quit` to exit.

## Test and Lint
```bash
pytest
ruff check .
```

## GitHub Notes
- Local folders like `.venv`, `data`, and `artifacts` are ignored via `.gitignore`.
- CI is configured through GitHub Actions in `.github/workflows/python-app.yml`.
