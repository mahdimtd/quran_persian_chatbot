from __future__ import annotations

from pathlib import Path

from .prompting import build_rag_prompt


class QuranRAGService:
    def __init__(
        self,
        index,
        openrouter_api_key: str,
        llm_model: str,
        openrouter_base_url: str,
    ) -> None:
        self.index = index
        self.openrouter_api_key = openrouter_api_key
        self.llm_model = llm_model
        self.openrouter_base_url = openrouter_base_url

    @classmethod
    def from_chroma(
        cls,
        persist_dir: Path,
        collection_name: str,
        embed_model_name: str,
        openrouter_api_key: str,
        llm_model: str,
        openrouter_base_url: str,
    ) -> QuranRAGService:
        if not persist_dir.exists():
            raise FileNotFoundError(
                f"Index directory not found at '{persist_dir}'. Build the index first."
            )

        import chromadb
        from llama_index.core import VectorStoreIndex
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        from llama_index.vector_stores.chroma import ChromaVectorStore

        embed_model = HuggingFaceEmbedding(model_name=embed_model_name)
        chroma_client = chromadb.PersistentClient(path=str(persist_dir))
        collection_names = {collection.name for collection in chroma_client.list_collections()}

        if not collection_names:
            raise RuntimeError(f"No Chroma collections found at '{persist_dir}'.")
        if collection_name not in collection_names:
            available = ", ".join(sorted(collection_names))
            raise RuntimeError(
                f"Collection '{collection_name}' not found. Available collections: {available}"
            )

        chroma_collection = chroma_client.get_collection(name=collection_name)
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embed_model,
        )

        return cls(
            index=index,
            openrouter_api_key=openrouter_api_key,
            llm_model=llm_model,
            openrouter_base_url=openrouter_base_url,
        )

    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        retriever = self.index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)
        return "\n\n".join(node.text for node in nodes if getattr(node, "text", "").strip())

    def answer_query(
        self,
        query: str,
        top_k: int = 5,
        temperature: float = 0.1,
        max_tokens: int = 1200,
    ) -> str:
        if not query.strip():
            return "سوال خالی است. لطفا سوال خود را وارد کنید."

        context = self.retrieve_context(query=query, top_k=top_k)
        prompt = build_rag_prompt(query=query, context=context)

        from openai import OpenAI

        client = OpenAI(
            base_url=self.openrouter_base_url,
            api_key=self.openrouter_api_key,
        )

        completion = client.chat.completions.create(
            model=self.llm_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return completion.choices[0].message.content or "پاسخی تولید نشد."
