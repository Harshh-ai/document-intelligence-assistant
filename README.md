# Document Intelligence Assistant

## Overview
The Document Intelligence Assistant is an AI-powered application that enables users to upload one or more PDF documents and interact with them through a conversational interface. The system allows users to extract information, compare documents, analyze resumes against job descriptions, and ask contextual questions grounded strictly in the uploaded content. The application is designed to be fast, modular, and production-ready, demonstrating a complete end-to-end Retrieval-Augmented Generation (RAG) workflow.

---

## Key Features
- **Multi-PDF upload support**: Upload and analyze multiple PDF documents simultaneously (e.g., resumes, job descriptions, research papers).
- **Conversational query interface**: Ask natural-language questions about uploaded documents using a chat-style UI.
- **Context-aware responses**: Answers are generated strictly from the content of uploaded documents, preventing hallucinations.
- **Multiple independent chats**: Each chat session maintains its own context, allowing focused conversations on the same document set.
- **Source attribution**: Retrieved document sources and page numbers are displayed for transparency and verification.
- **Efficient retrieval pipeline**: Uses vector embeddings and semantic search for accurate and relevant document retrieval.
- **Deployed & production-ready**: Fully deployed on Streamlit Cloud with secure API key management.

---

## How It Works (Architecture)

1. **Document loading**
   - PDF files are uploaded via the UI.
   - Each document is loaded page-by-page using `PyPDFLoader`.
   - Metadata (file name and page number) is attached to each document chunk.
2. **Text chunking**
   - Documents are split into overlapping text chunks using `RecursiveCharacterTextSplitter`.
   - This improves semantic retrieval and preserves context.
3. **Vector embedding**
   - Text chunks are converted into vector embeddings using `sentence-transformers/all-MiniLM-L6-v2`.
   - Embeddings are stored in a FAISS vector index.
4. **Semantic retrieval**
   - On each query, the system retrieves the most relevant chunks via similarity search.
5. **Response generation**
   - Retrieved chunks are combined into a contextual prompt.
   - A Groq-hosted LLM (`llama-3.1-8b-instant`) generates a concise, natural-language response constrained to the provided context.
6. **Chat management**
   - Chat histories are maintained using Streamlit session state.
   - Users can switch between multiple chats without losing context.

---

## Technology Stack
- **Frontend & deployment**: Streamlit
- **LLM inference**: Groq API (LLaMA 3.1)
- **Document processing**: LangChain, PyPDFLoader
- **Vector search**: FAISS
- **Embeddings**: HuggingFace Sentence Transformers
- **State management**: Streamlit session state
- **Security**: Environment variables and Streamlit Secrets for API key management

---

## Use Cases
- Resume analysis and job description matching
- Research paper summarization and Q&A
- Multi-document comparison
- Interview preparation based on uploaded material
- Internal document intelligence tools

---

## Deployment
The application is deployed on Streamlit Cloud and automatically redeploys on each push to the `main` branch. Environment variables (such as API keys) are securely managed using Streamlit Secrets and are not committed to the repository.

---
## Run Locally - the app can be run locally by using the following commands:
MAIN app file : 'app.py'
```bash
git clone https://github.com/Harshh-ai/document-intelligence-assistant.git
cd document-intelligence-assistant
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# create .env in the project root
GROQ_API_KEY="your_key_here"

streamlit run app.py
```
## Project Highlights
- Demonstrates a complete RAG pipeline from ingestion to inference
- Handles multi-document reasoning with source grounding
- Built with production considerations such as caching, error handling, and deployment
- Designed to be extensible for additional document types or models
``` markdown

## Live Demo

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]https://document-intelligence-assistant-wojitdjfpfcjrxv3eyx4xj.streamlit.app/
```


## ![App screenshot]
<img width="1439" height="777" alt="F9A14FBE-F19B-4033-BEB4-6DA5A158A119" src="https://github.com/user-attachments/assets/eaa3dc5c-2f71-46b1-b116-0dd32c6de7b3" />
<img width="1440" height="900" alt="079D2864-7466-48EA-BA97-D67C05DC4B3C" src="https://github.com/user-attachments/assets/f33ace9d-02ed-4f5d-9237-8a86c9ac462b" 
/><img width="1440" height="900" alt="006789CA-925D-4379-94B5-5432DDB603CC" src="https://github.com/user-attachments/assets/7a5ba138-aab2-400f-ab4d-6ad4d019a068" />

