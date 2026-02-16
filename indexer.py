import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

load_dotenv()

class RAGIndexer:
    def __init__(self, google_api_key=None):
        self.google_api_key = google_api_key or os.environ.get("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in environment variables.")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=self.google_api_key
        )
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            google_api_key=self.google_api_key,
            temperature=0
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            add_start_index=True,
        )
        self.vectorstore = None

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
        """Loads, splits, and indexes the document into an in-memory/temporary vectorstore."""
        print(f"Loading document: {file_path}")
        docs = self.load_document(file_path)
        
        print(f"Splitting {len(docs)} documents...")
        splits = self.text_splitter.split_documents(docs)
        print(f"Created {len(splits)} chunks.")
        
        print("Indexing...")
        # For session-based, we don't necessarily need a persist_directory
        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embeddings
        )
        print("Indexing complete.")
        return self.vectorstore

    def query(self, query_text):
        """Full RAG query implementation."""
        if not self.vectorstore:
            raise ValueError("Vectorstore not initialized. Run process_and_index first.")

        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vectorstore.as_retriever(),
            return_source_documents=True
        )

        response = qa_chain.invoke({"query": query_text})
        return response

if __name__ == "__main__":
    # Example usage for standalone testing
    import sys
    if len(sys.argv) > 1:
        path = sys.argv[1]
        try:
            indexer = RAGIndexer()
            indexer.process_and_index(path)
            res = indexer.query("Summarize this document")
            print(res["result"])
        except Exception as e:
            print(f"Error: {e}")
