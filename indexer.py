import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

class RAGIndexer:
    def __init__(self, persist_directory="./chroma_db"):
        self.persist_directory = persist_directory
        self.embeddings = OpenAIEmbeddings() # Requires OPENAI_API_KEY environment variable
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )

    def load_document(self, file_path):
        """Loads a document based on its extension."""
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        if ext == '.pdf':
            loader = PyPDFLoader(file_path)
        elif ext == '.csv':
            loader = CSVLoader(file_path)
        else:
            # Default to text loader
            loader = TextLoader(file_path, encoding='utf-8')
            
        return loader.load()

    def process_and_index(self, file_path):
        """Loads, splits, and indexes the document."""
        print(f"Loading document: {file_path}")
        docs = self.load_document(file_path)
        
        print(f"Splitting {len(docs)} documents...")
        splits = self.text_splitter.split_documents(docs)
        print(f"Created {len(splits)} chunks.")
        
        print(f"Indexing to {self.persist_directory}...")
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings, 
            persist_directory=self.persist_directory
        )
        print("Indexing complete.")
        return vectorstore

    def query(self, query_text, k=3):
        """Simple query interface for verification."""
        vectorstore = Chroma(
            persist_directory=self.persist_directory, 
            embedding=self.embeddings
        )
        results = vectorstore.similarity_search(query_text, k=k)
        return results

if __name__ == "__main__":
    # Example usage for standalone testing
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        indexer = RAGIndexer()
        indexer.process_and_index(path)
