import streamlit as st
import os
import json
from drive_loader import DriveLoader
from indexer import RAGIndexer

st.set_page_config(page_title="Hadith Corpus RAG", layout="wide")

st.title("📖 Hadith Corpus RAG Pipeline")
st.markdown("Download a Hadith corpus from Google Drive, index it with Gemini, and ask questions.")

# Sidebar for Configuration
with st.sidebar:
    st.header("Settings")
    google_api_key = st.text_input("Google API Key (Gemini)", type="password", value=os.environ.get("GOOGLE_API_KEY", ""))

    st.markdown("---")
    st.subheader("Google Drive Service Account")
    sa_json = st.text_area("Paste Service Account JSON here (optional if credentials.json or ENV exists)", height=200)

    if google_api_key:
        os.environ["GOOGLE_API_KEY"] = google_api_key

# Initialize Session State
if "indexer" not in st.session_state:
    st.session_state.indexer = None
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main UI
file_id = st.text_input("Google Drive File ID", placeholder="Enter the ID from the Drive sharing link")
output_filename = st.text_input("Output Filename", value="corpus_data.pdf")

if st.button("Download and Index"):
    if not file_id:
        st.error("Please enter a Google Drive File ID.")
    elif not google_api_key:
        st.error("Please enter a Google API Key.")
    else:
        try:
            with st.spinner("Connecting to Google Drive..."):
                # Handle Service Account
                credentials_info = None
                if sa_json:
                    credentials_info = json.loads(sa_json)

                drive = DriveLoader(credentials_info=credentials_info)

            with st.spinner("Downloading file..."):
                local_path = drive.download_file(file_id, output_filename)
                st.success(f"Downloaded to {local_path}")

            with st.spinner("Indexing with Gemini..."):
                indexer = RAGIndexer(google_api_key=google_api_key)
                indexer.process_and_index(local_path)
                st.session_state.indexer = indexer
                st.success("Indexing complete! You can now ask questions.")

        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("---")

# Chat Interface
if st.session_state.indexer:
    st.subheader("Ask a Question")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know about the corpus?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.indexer.query(prompt)
                    answer = response["result"]
                    sources = response["source_documents"]

                    st.markdown(answer)

                    with st.expander("View Sources"):
                        for i, doc in enumerate(sources):
                            st.markdown(f"**Source {i+1}** (Page {doc.metadata.get('page', 'N/A')}):")
                            st.write(doc.page_content[:500] + "...")

                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error querying index: {e}")
else:
    st.info("Download and index a file to start chatting.")
