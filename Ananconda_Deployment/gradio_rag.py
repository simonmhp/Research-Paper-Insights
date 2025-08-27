import os
import json
import requests
import chromadb
import gradio as gr
from pathlib import Path
from tqdm import tqdm

# ------------------------
# 1. Settings 
# ------------------------
MODEL_NAME = "mistral:latest"
EMBED_MODEL = "nomic-embed-text"  # embedding model name (if Ollama supports it)
OLLAMA_API = "http://localhost:11434"
DATA_DIR = Path(r"C:\Users\Vinod\Downloads\project\new\texts")
CHROMA_DB_DIR = Path(r"C:\Users\Vinod\Downloads\project\new\chroma_db")  # persistent storage

CHUNK_SIZE = 5000  # updated chunk size

# ------------------------
# 2. ChromaDB setup (persistent)
# ------------------------
chroma_client = chromadb.PersistentClient(path=str(CHROMA_DB_DIR))
collection = chroma_client.get_or_create_collection(name="research_papers")

# ------------------------
# 3. Embedding function (uses Ollama embeddings endpoint)
# ------------------------
def get_embedding(text: str):
    r = requests.post(f"{OLLAMA_API}/api/embeddings", json={
        "model": EMBED_MODEL,
        "prompt": text
    })
    r.raise_for_status()
    return r.json()["embedding"]

# ------------------------
# 4. Helper: create chunks from .txt files
# ------------------------
def load_all_chunks(data_dir: Path, chunk_size: int = CHUNK_SIZE):
    chunks = []
    files = sorted(list(data_dir.glob("*.txt")))
    for file in files:
        text = file.read_text(encoding="utf-8").strip()
        if not text:
            continue
        file_chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        chunks.extend(file_chunks)
    return chunks

# ------------------------
# 5. Build / update index (called by Gradio button)
# ------------------------
def build_index():
    all_chunks = load_all_chunks(DATA_DIR, CHUNK_SIZE)
    total = len(all_chunks)
    if total == 0:
        return "No .txt files found in the research_papers folder."

    existing_ids = set()
    if collection.count() > 0:
        result = collection.get(limit=collection.count())
        existing_ids = set(result.get("ids", []))

    with gr.Progress(total=total) as progress:
        for idx, chunk in enumerate(all_chunks):
            chunk_id = str(idx)
            if chunk_id in existing_ids:
                progress((idx + 1), desc=f"Skipping {idx+1}/{total} (exists)")
                continue
            try:
                emb = get_embedding(chunk)
            except Exception as e:
                return f"Error getting embedding from Ollama: {e}"
            collection.add(ids=[chunk_id], documents=[chunk], embeddings=[emb])
            progress((idx + 1), desc=f"Embedded {idx+1}/{total}")

    return f"Index built/updated. {collection.count()} total vectors stored."

# ------------------------
# 6. Streaming query function
# ------------------------
def ask_with_context_stream(question: str, top_k: int = 3):
    if not question or question.strip() == "":
        yield "Please enter a question."
        return

    try:
        q_emb = get_embedding(question)
    except Exception as e:
        yield f"Error getting question embedding: {e}"
        return

    try:
        results = collection.query(query_embeddings=[q_emb], n_results=top_k)
    except Exception as e:
        yield f"Error querying ChromaDB: {e}"
        return

    docs = results.get("documents", [[]])[0]
    context = "\n\n".join(docs) if docs else ""

    prompt = (
        "Use the following research context to answer the question concisely and accurately:\n\n"
        f"{context}\n\nQuestion: {question}\nAnswer:"
    )

    stream_url = f"{OLLAMA_API}/api/generate"
    payload = {"model": MODEL_NAME, "prompt": prompt, "stream": True}

    try:
        with requests.post(stream_url, json=payload, stream=True, timeout=120) as r:
            r.raise_for_status()
            accumulated = ""
            for line in r.iter_lines():
                if line:
                    try:
                        text_line = line.decode("utf-8").strip()
                        if text_line.startswith("data:"):
                            json_part = text_line[len("data:"):].strip()
                        else:
                            json_part = text_line
                        if json_part in ("[DONE]", ""):
                            continue
                        payload_chunk = json.loads(json_part)
                        chunk_text = ""
                        if isinstance(payload_chunk, dict):
                            chunk_text = payload_chunk.get("response", "")
                            if not chunk_text and "choices" in payload_chunk:
                                choices = payload_chunk["choices"]
                                if choices and isinstance(choices, list):
                                    for ch in choices:
                                        if isinstance(ch, dict):
                                            chunk_text += ch.get("delta", {}).get("content", "") or ch.get("text", "") or ""
                        if chunk_text:
                            accumulated += chunk_text
                            yield accumulated
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        yield f"Error calling Ollama generate API: {e}"
        return

    yield accumulated

# ------------------------
# 7. Gradio Interface
# ------------------------
with gr.Blocks(title="Ollama RAG Demo") as demo:
    gr.Markdown("## Research papers Analysis")
    with gr.Row():
        with gr.Column(scale=2):
            q_input = gr.Textbox(label="Question", placeholder="e.g. What is Machine learning?", lines=2)
            top_k = gr.Slider(minimum=1, maximum=8, value=3, step=1, label="Top K retrieved chunks")
            ask_btn = gr.Button("Ask (stream)")
            output = gr.Textbox(label="Model answer (streamed)", lines=10)

    ask_btn.click(fn=ask_with_context_stream, inputs=[q_input, top_k], outputs=[output])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
