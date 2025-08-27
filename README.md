
# Research-Paper-Insights

A project focused on extracting insights and summarizing academic research papers using **RAG (Retrieval-Augmented Generation)** and **LLMs**. This repository contains sample PDFs of research papers along with notebooks demonstrating different approaches for automated summarization and analysis.

## 🛠 Notebooks Overview

### 1. RAG_with_Ollama.ipynb
- Implements **Retrieval-Augmented Generation** (RAG) on research papers.
- Uses **Ollama** as the retrieval backend.
- Steps:
  1. Load PDF documents.
  2. Extract text and create embeddings.
  3. Query the RAG model to generate paper summaries and key insights.

### 2. LLM_Collab_GPT2.ipynb
- Demonstrates using **GPT-2** for summarization in **Google Colab**.
- Steps:
  1. Load PDF documents.
  2. Preprocess text for LLM input.
  3. Generate summaries using GPT-2.
- Great for experimentation with smaller models or local notebooks.

## 🚀 Features
- 📄 **PDF Ingestion** – Upload and extract text from research papers
- 🧠 **Text Embeddings** – Store and search using ChromaDB
- 🔎 **Question Answering** – Ask questions and get context-aware answers
- 🎨 **Interactive UI** – Powered by [Gradio](https://gradio.app/)
- 🔧 **Customizable Pipeline** – Modify preprocessing, embeddings, or models easily

---

Research-Paper-Insight/
├── Ananconda_Deployment/   # Deployment files, environment setup for Anaconda
├── Data/                   # Dataset and related files 
├── NoteBook/               # Jupyter notebooks for experiments, analysis, and model building
├── README.md               # Project documentation

Note: Data folder has 3 subfolders, pdf_4 is the actual pdfs used to train the models.
---

## ⚡ How to Use
```bash
# Clone the repo
git clone https://github.com/<your-username>/Research-Paper-Insights.git
cd Research-Paper-Insights/Ananconda_Deployment

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

---
##Usage:

# Run Gradio app
python gradio_rag.py
```

NOTE: Pull requests are welcome! For major changes, please open an issue first.

