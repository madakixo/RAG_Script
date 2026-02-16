# Hadith Corpus RAG Pipeline (Gemini Edition)

This project implements a Retrieval-Augmented Generation (RAG) pipeline that downloads a Hadith corpus from Google Drive, indexes it using Google Gemini Embeddings and ChromaDB, and allows for semantic searching and answer generation using Gemini 1.5 Pro.

## Prerequisites

- Python 3.8+
- A Google Cloud Project with the Drive API enabled.
- A Google AI Studio API Key (for Gemini).
- A Google Cloud Service Account JSON key.

## Setup

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**:
    - Set your Google API Key:
      ```bash
      export GOOGLE_API_KEY=your-gemini-api-key
      ```
    - (Optional) Set your Service Account JSON as an environment variable:
      ```bash
      export GOOGLE_SERVICE_ACCOUNT_JSON='{"type": "service_account", ...}'
      ```

3. **Google Drive Credentials**:
    - Place your Service Account JSON file in this directory and rename it to `credentials.json`.

## Usage

### 1. Streamlit Web App (Recommended)

Run the Streamlit app for a web-based interface:

```bash
streamlit run streamlit_app.py
```

### 2. CLI Tool

You can also run the pipeline from the command line:

```bash
python main.py <FILE_ID> --query "What does the prophet say about fasting?"
```

## Features

- **PDF Focus**: Optimized for indexing and searching PDF documents.
- **Gemini Powered**: Uses `models/embedding-001` for embeddings and `gemini-1.5-pro` for RAG.
- **Service Account Auth**: Seamless integration for cloud deployments (Google Cloud, Streamlit Cloud).
- **Session-based Indexing**: The index is rebuilt each session to ensure data freshness and compatibility with ephemeral cloud storage.
