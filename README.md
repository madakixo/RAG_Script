# Hadith Corpus RAG Pipeline

This project implements a Retrieval-Augmented Generation (RAG) pipeline that downloads a Hadith corpus from Google Drive, indexes it using OpenAI Embeddings and ChromaDB, and allows for semantic searching.

## Prerequisites

- Python 3.8+
- A Google Cloud Project with the Drive API enabled.
- An OpenAI API Key.

## Setup

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**:
    - Rename or copy `.env.example` (if provided) to `.env`.
    - Edit `.env` and add your OpenAI API Key:

      ```
      OPENAI_API_KEY=sk-your-key-here
      ```

3. **Google Drive Credentials**:
    - Download your OAuth 2.0 Client IDs JSON file from the Google Cloud Console.
    - Rename it to `credentials.json` and place it in this directory.
    - *Note*: On the first run, a browser window will open to authorize access. A `token.pickle` file will be created for subsequent runs.

## Usage

### 1. Indexing a File from Drive

You need the **File ID** from Google Drive. You can get this from the sharing link (e.g., `https://drive.google.com/file/d/THIS_IS_THE_FILE_ID/view`).

Run the pipeline:

```bash
python main.py <FILE_ID>
```

This will:

1. Download the file associated with the ID.
2. Save it locally as `corpus_data.txt` (default).
3. Split the text into chunks.
4. Generate embeddings and store them in `./chroma_db`.

### 2. Custom Output Filename

```bash
python main.py <FILE_ID> --output my_hadith_book.pdf
```

*Supports .txt, .pdf, and .csv extensions.*

### 3. Testing the Index (Querying)

You can run a test query immediately after indexing:

```bash
python main.py <FILE_ID> --query "What does the prophet say about fasting?"
```

### 4. Querying an Existing Index

To query the index without re-downloading (create a separate script or just use the class):

```python
from indexer import RAGIndexer

indexer = RAGIndexer() # Loads from ./chroma_db
results = indexer.query("importance of prayer")
for doc in results:
    print(doc.page_content)
```
