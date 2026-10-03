import chromadb
from langchain_ollama import OllamaEmbeddings, ChatOllama

def ask_codebase(index_dir, question, chat_model, embedding_model, top_k=6):
    client = chromadb.PersistentClient(path=str(index_dir + "/chroma"))
    collection = client.get_collection("codebase")
    embeddings = OllamaEmbeddings(model=embedding_model)
    qvec = embeddings.embed_query(question)

    result = collection.query(query_embeddings=[qvec], n_results=top_k)
    docs = result.get("documents", [[]])[0]
    metas = result.get("metadatas", [[]])[0]

    context_parts = []
    sources = []
    for doc, meta in zip(docs, metas):
        source = f"{meta['file']} (chunk {meta['chunk']})"
        context_parts.append(f"FILE: {source}\n{doc}")
        sources.append(source)

    context = "\n\n---\n\n".join(context_parts)
    prompt = f"""You are a codebase analysis assistant.
Answer the user's question using ONLY the supplied code context.
If the context does not contain enough evidence, say so.
Mention relevant file names and functions when visible.
Do not invent code that is not present.

USER QUESTION:
{question}

CODE CONTEXT:
{context}
"""

    llm = ChatOllama(model=chat_model, temperature=0)
    response = llm.invoke(prompt)
    return response.content, list(dict.fromkeys(sources))
