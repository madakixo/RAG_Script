#RAG Script madakixo dec 2025 
#use google drive dlfer to index file using indexer.py
#load pdf from driveloader.py
import os
import argparse
from drive_loader import DriveLoader
from indexer import RAGIndexer

def main():
    parser = argparse.ArgumentParser(description="Download Hadith Corpus from Drive and Index it.")
    parser.add_argument("file_id", help="The Google Drive File ID of the corpus.")
    parser.add_argument("--output", default="corpus_data.txt", help="Local filename to save the downloaded file.")
    parser.add_argument("--query", help="Optional query to test the index after building.")
    
    args = parser.parse_args()
    
    # 1. Download
    print("Initializing Drive Loader...")
    try:
        drive = DriveLoader()
        local_path = drive.download_file(args.file_id, args.output)
    except Exception as e:
        print(f"Error downloading file: {e}")
        print("Make sure 'credentials.json' is present in the directory.")
        return

    # 2. Index
    print("Initializing RAG Indexer...")
    try:
        indexer = RAGIndexer()
        indexer.process_and_index(local_path)
    except Exception as e:
        print(f"Error indexing file: {e}")
        return

    # 3. Test Query (Optional)
    if args.query:
        print(f"Running test query: '{args.query}'")
        results = indexer.query(args.query)
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(doc.page_content[:200] + "...")
            print(f"Source: {doc.metadata}")

if __name__ == "__main__":
    main()
