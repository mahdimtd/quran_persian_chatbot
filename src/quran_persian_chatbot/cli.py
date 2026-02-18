from __future__ import annotations

import argparse
from pathlib import Path

from .config import (
    DEFAULT_COLLECTION_NAME,
    DEFAULT_EMBED_MODEL,
    DEFAULT_LLM_MODEL,
    DEFAULT_OPENROUTER_BASE_URL,
    AppConfig,
)
from .indexing import build_chroma_index, download_default_data, find_text_files
from .rag import QuranRAGService


def _add_common_index_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--persist-dir",
        type=Path,
        default=Path("artifacts/chroma_index"),
        help="Directory to store ChromaDB index.",
    )
    parser.add_argument(
        "--collection-name",
        default=DEFAULT_COLLECTION_NAME,
        help="Chroma collection name.",
    )
    parser.add_argument(
        "--embed-model",
        default=DEFAULT_EMBED_MODEL,
        help="Embedding model name.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Quran Persian chatbot (RAG with LlamaIndex + ChromaDB)",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser_cmd = subparsers.add_parser(
        "build-index",
        help="Build Chroma index from text data.",
    )
    build_parser_cmd.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data"),
        help="Directory containing source .txt files.",
    )
    build_parser_cmd.add_argument(
        "--download-default-data",
        action="store_true",
        help="Download default data files if they do not exist.",
    )
    build_parser_cmd.add_argument("--chunk-size", type=int, default=512, help="Text chunk size.")
    build_parser_cmd.add_argument(
        "--chunk-overlap",
        type=int,
        default=100,
        help="Chunk overlap size.",
    )
    build_parser_cmd.add_argument(
        "--reset-collection",
        action="store_true",
        help="Delete and recreate target collection before indexing.",
    )
    _add_common_index_args(build_parser_cmd)

    chat_parser_cmd = subparsers.add_parser("chat", help="Run interactive QA chat in terminal.")
    _add_common_index_args(chat_parser_cmd)
    chat_parser_cmd.add_argument("--api-key", help="OpenRouter API key.")
    chat_parser_cmd.add_argument(
        "--model",
        default=DEFAULT_LLM_MODEL,
        help="OpenRouter model id.",
    )
    chat_parser_cmd.add_argument(
        "--base-url",
        default=DEFAULT_OPENROUTER_BASE_URL,
        help="OpenRouter base URL.",
    )
    chat_parser_cmd.add_argument("--top-k", type=int, default=5, help="Retriever top-k.")

    return parser


def _run_build_index(args: argparse.Namespace) -> int:
    if args.download_default_data:
        download_default_data(args.data_dir)

    input_files = find_text_files(args.data_dir)
    if not input_files:
        message = (
            f"No .txt files found in '{args.data_dir}'. "
            "Add data files or run with --download-default-data."
        )
        print(
            message
        )
        return 1

    build_chroma_index(
        input_files=input_files,
        persist_dir=args.persist_dir,
        collection_name=args.collection_name,
        embed_model_name=args.embed_model,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        reset_collection=args.reset_collection,
    )
    print(f"Index created at: {args.persist_dir}")
    print(f"Collection: {args.collection_name}")
    return 0


def _run_chat(args: argparse.Namespace) -> int:
    config = AppConfig.from_env()
    api_key = args.api_key or config.openrouter_api_key
    if not api_key:
        print("OpenRouter API key not found. Set OPENROUTER_API_KEY or pass --api-key.")
        return 1

    service = QuranRAGService.from_chroma(
        persist_dir=args.persist_dir,
        collection_name=args.collection_name,
        embed_model_name=args.embed_model,
        openrouter_api_key=api_key,
        llm_model=args.model,
        openrouter_base_url=args.base_url,
    )

    print("Interactive mode. Type 'quit' to exit.")
    while True:
        try:
            query = input("\nسوال شما: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat.")
            return 0

        if query.lower() in {"quit", "exit", "خروج"}:
            print("Exiting chat.")
            return 0

        try:
            response = service.answer_query(query=query, top_k=args.top_k)
            print(f"\nپاسخ:\n{response}")
        except Exception as exc:
            print(f"Error while generating answer: {exc}")


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "build-index":
        return _run_build_index(args)
    if args.command == "chat":
        return _run_chat(args)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
