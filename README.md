# GenAI-Powered Open Source Onboarding Assistant

## 🚀 Overview
This project is a GenAI-powered system designed to help new contributors
understand large open-source codebases, identify suitable issues, and
begin contributing faster with less mentor intervention.

The tool analyzes a GitHub repository, understands its structure using
static analysis and embeddings, and provides:
- Natural language explanations of the codebase
- Semantic search over source code
- Beginner-friendly issue recommendations

---

## 🎯 Problem Statement
Open-source projects often struggle with contributor onboarding due to:
- Large and complex codebases
- Outdated or insufficient documentation
- High mentor workload for repeated questions

This results in low contributor retention and slow onboarding.

---

## 💡 Solution
This system automatically:
- Parses and understands repository source code
- Builds semantic embeddings of code components
- Uses Retrieval-Augmented Generation (RAG) for accurate explanations
- Maps GitHub issues to relevant code and skills
- Suggests beginner-friendly issues for new contributors

---

## 🧠 Key Features
- 🔍 Semantic code search using embeddings
- 🧠 GenAI-based code explanations (RAG)
- 📌 Issue-to-code relevance mapping
- 🎯 Difficulty and skill estimation for contributors
- 🌐 Simple web UI for easy interaction

---

## 🏗️ Architecture
The system consists of:
1. Repository ingestion and static analysis (AST)
2. Embedding generation and vector storage (FAISS)
3. Retrieval pipeline for relevant code context
4. Local LLM inference using Ollama
5. Contributor intelligence layer
6. Streamlit-based UI

(Architecture diagram provided below)

---

## 🧪 Tested Repositories
- Flask (pallets/flask)
- Requests (psf/requests)
- FastAPI (tiangolo/fastapi)

---

## 🛠️ Tech Stack
- Python
- SentenceTransformers
- FAISS
- Ollama (Mistral / LLaMA)
- Streamlit
- GitHub REST API

---

## 📈 Future Work
- Repository-level caching
- Multi-language support
- Pull request recommendation
- Mentor feedback integration
- CI/CD documentation sync

---

## 🤝 Contribution
This project is open to contributions. Please check issues and
follow standard open-source contribution practices.






ARCHITECTURE DIAGRAM : -

User
  ↓
Streamlit UI
  ↓
Repo Ingestion → AST Parser
  ↓
Embeddings → FAISS
  ↓
Retriever → LLM (Ollama)
  ↓
Answer / Issue Suggestions

