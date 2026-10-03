# 🧭 Codebase Knowledge Navigator

An AI-powered codebase analysis tool that lets developers upload source files, search them semantically, ask natural-language questions, and inspect simple local dependencies.

## Why this project is different

This is not a generic chatbot. The knowledge source is the actual software project. Answers are grounded in retrieved source-code chunks and accompanied by file/chunk references.

## Features

- Multi-file source-code upload
- Semantic code retrieval with Ollama embeddings
- RAG-based codebase Q&A
- File/chunk source references
- Simple Python/JavaScript dependency detection
- Streamlit interface
- Local-first setup with Ollama

## Architecture

```text
Source Files
     ↓
Code Chunking
     ↓
Ollama Embeddings
     ↓
ChromaDB
     ↓
Semantic Retrieval
     ↓
Relevant Code Context
     ↓
Ollama LLM
     ↓
Grounded Answer + Sources
```

## Setup

### 1. Install Ollama

Install Ollama from the official Ollama website and make sure it is running.

Pull a chat model and embedding model, for example:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Run

```powershell
streamlit run app.py
```

Open the local Streamlit URL shown in the terminal.

## Example questions

- Where is the database connection created?
- Explain the authentication flow.
- Which file handles user registration?
- Where is the API request processed?
- What functions depend on the database module?

## Resume skills demonstrated

Python, RAG, LangChain, Ollama, vector databases, embeddings, semantic search, Streamlit, source-code analysis, dependency analysis, Git/GitHub.

## Future improvements

- GitHub repository URL ingestion
- AST-based parsing
- Function/class-level indexing
- Interactive dependency graph
- Code change impact analysis
- Bug investigation mode
- Repository-wide documentation generation
- Automated unit-test suggestions
