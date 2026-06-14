# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) application that allows users to ask questions about YouTube videos using their transcripts.

The application:

- Extracts transcripts from YouTube videos
- Splits transcripts into chunks
- Creates embeddings using OpenAI
- Stores embeddings in Qdrant Vector Database
- Retrieves relevant transcript chunks
- Uses an LLM to answer questions based only on the retrieved context
- Provides a simple Streamlit user interface

---

## Features

- Ask questions about any YouTube video with available transcripts
- Supports English and Hindi transcripts
- Qdrant vector storage for efficient retrieval
- OpenAI embeddings and LLM integration
- Streamlit-based web UI
- Automatic collection reuse for previously processed videos

---

## Tech Stack

- Python
- Streamlit
- LangChain
- OpenAI
- Qdrant
- YouTube Transcript API

---

## Project Structure

```text
project/
│
├── main.py          # RAG logic
├── ui.py            # Streamlit UI
├── requirements.txt
├── .env
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows

```bash
venv\Scripts\activate
```

#### Mac/Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key

QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

---

## Running the Application

Start the Streamlit app:

```bash
streamlit run ui.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## How It Works

### 1. Transcript Extraction

The application fetches the transcript from the provided YouTube video.

### 2. Text Chunking

The transcript is split into smaller chunks using:

- Chunk Size: 300
- Chunk Overlap: 100

### 3. Embedding Generation

OpenAI Embeddings convert text chunks into vectors.

### 4. Vector Storage

Vectors are stored in Qdrant.

If a collection for the video already exists, the application reuses it instead of recreating embeddings.

### 5. Retrieval

Relevant chunks are retrieved using similarity search.

### 6. Answer Generation

The retrieved context is passed to the LLM, which answers only from the provided context.

Prompt:

```text
You are a helpful assistant.

Answer only from the provided context.
If the context is insufficient, just say you don't know.
```

---

## Supported Languages

### English

Fetches English transcript when available.

### Hindi

Fetches Hindi transcript when available.

> Note: Availability depends on captions provided by YouTube.

---

## Example

### Input

Video URL:

```text
https://www.youtube.com/watch?v=xxxxxxxxxxx
```

Question:

```text
Who is the guest in this podcast?
```

### Output

```text
The guest in the podcast is ...
```

---

## Future Improvements

- Chat history support
- Conversational RAG
- Multi-video search
- MMR retrieval
- Contextual compression retrieval
- Hybrid search
- Citation support
- Streaming responses
- Docker deployment
- User authentication

---

## License

This project is open-source and available under the MIT License.