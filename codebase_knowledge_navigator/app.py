import os
import shutil
import tempfile
from pathlib import Path

import streamlit as st
from src.indexer import build_index
from src.rag import ask_codebase
from src.dependencies import build_dependency_graph

st.set_page_config(page_title="Codebase Knowledge Navigator", page_icon="🧭", layout="wide")
st.title("🧭 Codebase Knowledge Navigator")
st.caption("Ask questions about a software project using code-aware RAG.")

SUPPORTED = {".py", ".js", ".ts", ".java", ".c", ".cpp", ".h", ".hpp", ".html", ".css", ".sql", ".json", ".md", ".txt"}

with st.sidebar:
    st.header("Project")
    uploaded = st.file_uploader(
        "Upload source files",
        type=[x[1:] for x in sorted(SUPPORTED)],
        accept_multiple_files=True,
    )
    model = st.text_input("Ollama chat model", value="llama3.2")
    embedding_model = st.text_input("Ollama embedding model", value="nomic-embed-text")

if uploaded:
    if st.button("🚀 Index Codebase", use_container_width=True):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for f in uploaded:
                out = base / Path(f.name).name
                out.write_bytes(f.getbuffer())
            st.session_state["index_dir"] = build_index(base, embedding_model)
            st.session_state["file_count"] = len(uploaded)
            st.session_state["model"] = model
        st.success(f"Indexed {len(uploaded)} source files.")

if "index_dir" not in st.session_state:
    st.info("Upload source files in the sidebar and click 'Index Codebase'.")
    st.stop()

tab1, tab2 = st.tabs(["💬 Ask the Codebase", "🕸️ Dependencies"])

with tab1:
    question = st.text_input(
        "Ask a question",
        placeholder="Where is database connection created?",
    )
    if st.button("Ask", type="primary") and question.strip():
        with st.spinner("Searching the codebase..."):
            answer, sources = ask_codebase(
                st.session_state["index_dir"],
                question,
                st.session_state["model"],
                embedding_model,
            )
        st.subheader("Answer")
        st.write(answer)
        st.subheader("Sources")
        for s in sources:
            st.code(s, language="text")

with tab2:
    if st.button("Analyze Dependencies"):
        graph = build_dependency_graph(Path(st.session_state["index_dir"]) / "source_files")
        if graph:
            for file, deps in graph.items():
                st.write(f"**{file}** → {', '.join(deps) if deps else 'No local dependencies detected'}")
        else:
            st.info("No simple local dependencies were detected.")
