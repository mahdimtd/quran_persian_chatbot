from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATA_FILES = ("majmaolbayan.txt", "alborhan.txt")
DEFAULT_EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
DEFAULT_COLLECTION_NAME = "quran_persian_collection"
DEFAULT_PERSIST_DIR = Path("artifacts/chroma_index")
DEFAULT_DATA_DIR = Path("data")
DEFAULT_LLM_MODEL = "deepseek/deepseek-chat-v3-0324:free"
DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"


def _path_from_env(key: str, default: Path) -> Path:
    return Path(os.getenv(key, str(default))).expanduser().resolve()


@dataclass(slots=True)
class AppConfig:
    persist_dir: Path = DEFAULT_PERSIST_DIR
    data_dir: Path = DEFAULT_DATA_DIR
    collection_name: str = DEFAULT_COLLECTION_NAME
    embed_model_name: str = DEFAULT_EMBED_MODEL
    llm_model: str = DEFAULT_LLM_MODEL
    openrouter_base_url: str = DEFAULT_OPENROUTER_BASE_URL
    openrouter_api_key: str | None = None

    @classmethod
    def from_env(cls) -> AppConfig:
        return cls(
            persist_dir=_path_from_env("QPQ_INDEX_DIR", DEFAULT_PERSIST_DIR),
            data_dir=_path_from_env("QPQ_DATA_DIR", DEFAULT_DATA_DIR),
            collection_name=os.getenv("QPQ_COLLECTION_NAME", DEFAULT_COLLECTION_NAME),
            embed_model_name=os.getenv("QPQ_EMBED_MODEL", DEFAULT_EMBED_MODEL),
            llm_model=os.getenv("OPENROUTER_MODEL", DEFAULT_LLM_MODEL),
            openrouter_base_url=os.getenv(
                "OPENROUTER_BASE_URL", DEFAULT_OPENROUTER_BASE_URL
            ),
            openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        )
