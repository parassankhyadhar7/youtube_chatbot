# 🎥 YouTube RAG Chatbot

A Retrieval-Augmented Generation (RAG) application that allows users to chat with YouTube videos using their transcripts.

The application:

- Extracts transcripts from YouTube videos
- Supports both standard YouTube URLs and shared URLs
- Supports English and Hindi transcripts
- Splits transcripts into chunks
- Generates embeddings using Hugging Face Embedding Models
- Stores vectors in Qdrant Vector Database
- Retrieves relevant transcript chunks using semantic search
- Uses a Hugging Face LLM to answer questions based on retrieved context
- Provides a Streamlit-based web interface

---

## Features

- Ask questions about any YouTube video with available transcripts
- Support for English and Hindi transcripts
- Support for YouTube video URLs, share URLs, Shorts URLs, and Embed URLs
- Hugging Face Embeddings
- Hugging Face LLM Integration
- Qdrant Vector Database
- Semantic Search Retrieval
- Streamlit UI
- Collection reuse for previously processed videos

---

## Tech Stack

- Python
- Streamlit
- LangChain
- Hugging Face Inference API
- Qdrant
- YouTube Transcript API

---

## Architecture

```text
YouTube Video
      │
      ▼
Transcript Extraction
      │
      ▼
Text Chunking
      │
      ▼
Hugging Face Embeddings
      │
      ▼
Qdrant Vector Store
      │
      ▼
Retriever
      │
      ▼
Hugging Face LLM
      │
      ▼
Answer
```

---

## Project Structure

```text
project/
│
├── main.py          # RAG Logic
├── ui.py            # Streamlit UI
├── requirements.txt
├── .env
└── README.md
```

---

## Setup

### 1. Clone Repository

```bash
git clone <your-repository-url>
cd <repository-name>
```

---

### 2. Create Virtual Environment

#### Windows

```bash
python -m venv venv
```

Activate the virtual environment:

```bash
venv\Scripts\activate
```

#### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root.

```env
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key

HUGGINGFACEHUB_API_TOKEN=your_huggingface_token
```

---

### 5. Run the Application

Start the Streamlit application:

```bash
streamlit run ui.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Supported YouTube URLs

### Standard URL

```text
https://www.youtube.com/watch?v=_GlFjR6N1Xw
```

### Share URL

```text
https://youtu.be/_GlFjR6N1Xw
```

### Shorts URL

```text
https://youtube.com/shorts/VIDEO_ID
```

### Embed URL

```text
https://www.youtube.com/embed/VIDEO_ID
```

---

## Supported Languages

### English

Fetches the default transcript.

### Hindi

Fetches Hindi transcripts when available.

> Note: Transcript availability depends on captions provided by YouTube.

---

## How It Works

### 1. Transcript Extraction

The transcript is fetched from YouTube using the YouTube Transcript API.

### 2. Text Chunking

The transcript is divided into smaller chunks:

- Chunk Size: 300
- Chunk Overlap: 100

### 3. Embedding Generation

The application uses the following embedding model:

```text
sentence-transformers/all-mpnet-base-v2
```

to generate semantic embeddings.

### 4. Vector Storage

Embeddings are stored inside Qdrant.

If the video has already been processed, the existing collection is reused.

### 5. Retrieval

Relevant transcript chunks are retrieved using similarity search.

### 6. Answer Generation

The retrieved context is passed to the following Hugging Face model:

```text
MiniMaxAI/MiniMax-M2.5
```

The model generates an answer based on the retrieved transcript context.

---

## Example

### Input

Video URL:

```text
https://www.youtube.com/watch?v=xxxxxxxxxxx
```

Question:

```text
What is the story being discussed in the video?
```

### Output

```text
The speaker explains...
```

---

## Environment Variables

| Variable | Description |
|-----------|-------------|
| `QDRANT_URL` | Qdrant Cloud URL |
| `QDRANT_API_KEY` | Qdrant API Key |
| `HUGGINGFACEHUB_API_TOKEN` | Hugging Face API Token |

---

## Future Improvements

- Conversational RAG
- Chat History
- Streaming Responses
- Multi-Video Search
- MMR Retrieval
- Contextual Compression Retrieval
- Hybrid Search
- Source Citations
- Docker Deployment
- Authentication

---

## License

This project is open-source.