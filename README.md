
# Research-Paper-Insights

A project focused on extracting insights and summarizing academic research papers using **RAG (Retrieval-Augmented Generation)** and **LLMs**. This repository contains sample PDFs of research papers along with notebooks demonstrating different approaches for automated summarization and analysis.

## 📂 Repository Structure


Research-Paper-Insights/
│
├─ samples/ # Sample research paper PDFs
│ ├─ paper1.pdf
│ ├─ paper2.pdf
│ └─ ...
│
├─ notebooks/
│ ├─ RAG_with_Ollama.ipynb # Notebook using Ollama for RAG-based summarization
│ ├─ LLM_Collab_GPT2.ipynb # Notebook using GPT-2 on Colab for summarization
│
└─ README.md


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

## 📄 PDF Samples
- `samples/` folder contains example research papers in PDF format for testing and demonstration.
- These can be replaced with your own research papers.

## ⚡ How to Use
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/Research-Paper-Insights.git
   cd Research-Paper-Insights

