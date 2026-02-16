# RAG Script Updated for Gemini and Service Account
import os
import argparse
from drive_loader import DriveLoader
from indexer import RAGIndexer

def main():
    parser = argparse.ArgumentParser(description="Download Hadith Corpus from Drive and Index it using Gemini.")
    parser.add_argument("file_id", help="The Google Drive File ID of the corpus.")
    parser.add_argument("--output", default="corpus_data.pdf", help="Local filename to save the downloaded file.")
    parser.add_argument("--query", help="Optional query to test the index after building.")
    
    args = parser.parse_args()
    
    # 1. Download
    print("Initializing Drive Loader...")
    try:
        # Assumes credentials.json is present or GOOGLE_SERVICE_ACCOUNT_JSON env var is set
        drive = DriveLoader()
        local_path = drive.download_file(args.file_id, args.output)
    except Exception as e:
        print(f"Error downloading file: {e}")
        print("Make sure 'credentials.json' is present or GOOGLE_SERVICE_ACCOUNT_JSON is set.")
        return

    # 2. Index
    print("Initializing RAG Indexer...")
    try:
        # Assumes GOOGLE_API_KEY env var is set
        indexer = RAGIndexer()
        indexer.process_and_index(local_path)
    except Exception as e:
        print(f"Error indexing file: {e}")
        return

    # 3. Test Query (Optional)
    if args.query:
        print(f"Running test query: '{args.query}'")
        try:
            response = indexer.query(args.query)
            print("\nAnswer:")
            print(response["result"])
            print("\nSources:")
            for i, doc in enumerate(response["source_documents"]):
                print(f"[{i+1}] {doc.metadata}")
        except Exception as e:
            print(f"Error querying index: {e}")

if __name__ == "__main__":
    main()
