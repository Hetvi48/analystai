# AnalystAI

An AI-powered document question-answering system built with
**Retrieval-Augmented Generation (RAG)**. The project implements an
end-to-end ingestion pipeline for extracting, chunking, and indexing
document content, followed by semantic retrieval and a LangChain-based
chatbot for answering questions from the indexed knowledge base.

## 🚀 Overview

**AnalystAI** is designed to turn unstructured documents into a
searchable knowledge base and provide grounded answers through a
conversational interface.

The project follows a modular RAG architecture:

``` text
                 ┌─────────────────────┐
                 │      Documents      │
                 │       (PDF)         │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Extraction     │
                 │      extract.py     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │       Chunking      │
                 │     chunking.py     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Vector Ingestion  │
                 │    insertion.py     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Vector DB       │
                 │  Semantic Search    │
                 └──────────┬──────────┘
                            │
                     Relevant Chunks
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Retrieval      │
                 │  chunk_retrieval.py │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   LangChain Chatbot │
                 │     groq_chat.py    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Grounded Answer   │
                 └─────────────────────┘
```

## ✨ Key Features

-   **PDF document ingestion** for building a knowledge base.
-   **Document extraction** to convert source files into processable
    content.
-   **Recursive text chunking** to divide documents into
    retrieval-friendly pieces.
-   **Vector database integration** for semantic similarity search.
-   **Modular retrieval pipeline** for fetching relevant document
    chunks.
-   **RAG-based question answering** to ground responses in retrieved
    context.
-   **LangChain chatbot integration** for conversational interaction.
-   **Groq-powered LLM integration** for generating responses.
-   **Environment-based configuration** using `.env` files.
-   Modular project structure separating ingestion, retrieval, model,
    and configuration components.

## 🗂️ Project Structure

``` text
analyst_advisor/
│
├── config/
│   └── settings.py              # Application configuration and settings
│
├── ingestion/
│   ├── data/
│   │   └── report.pdf           # Source document(s)
│   │
│   ├── extraction/
│   │   ├── chunking.py          # Document chunking logic
│   │   └── extract.py           # Document extraction logic
│   │
│   └── vector_db/
│       ├── insertion.py         # Vector database insertion/upsert
│       └── test.py              # Vector DB related tests
│
├── model/
│   ├── groq_chat.py             # Groq/LangChain chatbot implementation
│   └── test.py                  # Model-related tests
│
├── retrieval/
│   └── chunk_retrieval.py       # Retrieval of relevant document chunks
│
├── .env                         # Local environment variables (not committed)
├── .env.example                 # Example environment configuration
├── .gitignore
└── requirements.txt              # Python dependencies
```

## 🔄 RAG Pipeline

The application is organized into two major stages.

### 1. Ingestion Pipeline

The ingestion pipeline prepares documents for retrieval:

1.  **Extraction** -- reads the source PDF and converts its content into
    processable documents.
2.  **Chunking** -- splits the extracted content into smaller
    overlapping chunks.
3.  **Embedding & indexing** -- converts chunks into vector
    representations and stores them in the vector database.

This stage creates the searchable knowledge base used by the chatbot.

### 2. Retrieval & Generation

When a user asks a question:

1.  The question is processed for retrieval.
2.  Relevant chunks are retrieved from the vector database using
    semantic similarity.
3.  The retrieved context is passed to the LangChain-based chatbot.
4.  The LLM generates an answer using the retrieved information.

This approach helps the chatbot answer questions using information
contained in the indexed documents instead of relying only on the
model's internal knowledge.

## 🛠️ Tech Stack

  Technology                   Purpose
  ---------------------------- ------------------------------------------
  **Python**                   Core programming language
  **LangChain**                RAG and LLM application orchestration
  **Groq**                     LLM inference
  **Pinecone**                 Vectordb for Embedding storage and semantic retrieval
  **PyPDFLoader**              Source document format
  **python-dotenv / `.env`**   Environment configuration

## ⚙️ Setup

### 1. Clone the repository

``` bash
git clone <your-repository-url>
cd analyst_advisor
```

### 2. Create a virtual environment

``` bash
python -m venv venv
```

Activate it:

**Windows**

``` bash
venv\Scripts\activate
```

**macOS / Linux**

``` bash
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file based on `.env.example`:

``` bash
cp .env.example .env
```

For Windows, you can also create the file manually.

Add the required API keys and configuration values to `.env`.

> **Important:** Never commit `.env` or API keys to GitHub.

## ▶️ Running the Project

The project is organized as separate modules for ingestion, retrieval,
and generation.

### Run document ingestion

Use the extraction and chunking modules to process the source document
and then run the vector database insertion module to index the chunks.

Example:

``` bash
python ingestion/extraction/extract.py
python ingestion/extraction/chunking.py
python ingestion/vector_db/insertion.py
```

### Run the chatbot

After the document has been indexed, start the LangChain/Groq chatbot:

``` bash
python model/groq_chat.py
```

> The exact execution flow may vary depending on how the modules are
> connected in your local implementation.

## 🧠 Why RAG?

A standard LLM may not have access to private or domain-specific
documents. RAG addresses this by retrieving relevant information from an
external knowledge base before generating an answer.

``` text
User Question
      │
      ▼
Semantic Retrieval
      │
      ▼
Relevant Context
      │
      ▼
LLM + Context
      │
      ▼
Grounded Response
```

This makes the system particularly useful for querying reports,
documentation, internal knowledge bases, and other domain-specific
content.

## 📌 Future Improvements

-   Add conversation memory for multi-turn interactions.
-   Add source/citation display for retrieved chunks.
-   Support multiple document formats.
-   Add document metadata filtering.
-   Implement retrieval evaluation metrics such as Recall@K and MRR.
-   Add reranking for improved retrieval quality.
-   Add a web-based UI using Streamlit or FastAPI + frontend.
-   Add automated tests for the complete ingestion-to-generation
    pipeline.
-   Containerize the application using Docker.

## 👩‍💻 Author

**Hetvi Khadela**

Computer Science Engineering --- Data Science

------------------------------------------------------------------------

⭐ If you find this project useful, consider giving the repository a
star!
