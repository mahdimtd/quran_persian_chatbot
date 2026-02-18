from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

from .config import DEFAULT_DATA_FILES

DEFAULT_DATA_URLS = {
    "majmaolbayan.txt": "https://filedn.eu/l1MYFwJMIh4Y60BIIrYyMiy/Quran_Persian_QA/majmaolbayan.txt",
    "alborhan.txt": "https://filedn.eu/l1MYFwJMIh4Y60BIIrYyMiy/Quran_Persian_QA/alborhan.txt",
}


def download_file(url: str, destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as output:
        output.write(response.read())
    return destination


def download_default_data(data_dir: Path) -> list[Path]:
    downloaded: list[Path] = []
    for filename, url in DEFAULT_DATA_URLS.items():
        destination = data_dir / filename
        if destination.exists():
            downloaded.append(destination)
            continue
        downloaded.append(download_file(url, destination))
    return downloaded


def find_text_files(data_dir: Path) -> list[Path]:
    preferred = [data_dir / file_name for file_name in DEFAULT_DATA_FILES]
    existing_preferred = [path for path in preferred if path.exists()]
    if existing_preferred:
        return existing_preferred

    return sorted(path for path in data_dir.glob("*.txt") if path.is_file())


def build_chroma_index(
    input_files: list[Path],
    persist_dir: Path,
    collection_name: str,
    embed_model_name: str,
    chunk_size: int = 512,
    chunk_overlap: int = 100,
    reset_collection: bool = False,
) -> Path:
    if not input_files:
        raise ValueError("No input text files provided for index creation.")

    import chromadb
    from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    from llama_index.vector_stores.chroma import ChromaVectorStore

    persist_dir.mkdir(parents=True, exist_ok=True)

    documents = SimpleDirectoryReader(input_files=[str(p) for p in input_files]).load_data()
    embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
    node_parser = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    chroma_client = chromadb.PersistentClient(path=str(persist_dir))
    if reset_collection:
        try:
            chroma_client.delete_collection(name=collection_name)
        except Exception:
            pass

    chroma_collection = chroma_client.get_or_create_collection(name=collection_name)
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        node_parser=node_parser,
        show_progress=True,
    )
    return persist_dir


def archive_index(persist_dir: Path, output_zip_path: Path) -> Path:
    output_zip_path.parent.mkdir(parents=True, exist_ok=True)
    archive_path = shutil.make_archive(
        str(output_zip_path.with_suffix("")), "zip", root_dir=str(persist_dir)
    )
    return Path(archive_path)
