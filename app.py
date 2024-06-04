import streamlit as st
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import openai
import tempfile
import os
import fitz  # PyMuPDF
import docx
import html2text

# Function to extract text from different file types and retain page numbers
def extract_text_from_file(file_path, file_type):
    text = ""
    metadata = []
    if file_type == "pdf":
        doc = fitz.open(file_path)
        for page_num, page in enumerate(doc, start=1):
            page_text = page.get_text()
            text += page_text
            metadata.append({'page_number': page_num, 'text': page_text})
    elif file_type == "docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
        metadata.append({'page_number': 1, 'text': text})
    elif file_type == "html":
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            text = html2text.html2text(html_content)
        metadata.append({'page_number': 1, 'text': text})
    elif file_type in ["txt", "rtf"]:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        metadata.append({'page_number': 1, 'text': text})
    return text, metadata

# Streamlit app
st.title("Document Parser with LlamaIndex and GPT-4")

# Input for OpenAI API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

if api_key:
    # Set the OpenAI API key
    openai.api_key = api_key

    # Initialize the OpenAI LLM with the provided API key
    llm = OpenAI(api_key=api_key, temperature=0, model="gpt-4")

    # Initialize the OpenAI embedding model
    embedding_model = OpenAIEmbedding(api_key=api_key)

    # Initialize session state for memory
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'query' not in st.session_state:
        st.session_state.query = ""

    # Button to clear conversation history
    if st.button("Clear History"):
        st.session_state.conversation_history = []
        st.session_state.query = ""

    # File uploader
    uploaded_file = st.file_uploader("Upload a file", type=["pdf", "txt", "doc", "docx", "rtf", "html"])

    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_file_path = tmp_file.name

        # Determine the file type
        file_type = uploaded_file.name.split(".")[-1].lower()

        # Extract text and metadata from the uploaded file
        text, metadata = extract_text_from_file(tmp_file_path, file_type)

        # Create a temporary text file with the extracted text
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_text_file:
            tmp_text_file.write(text.encode("utf-8"))
            tmp_text_file_path = tmp_text_file.name

        # Load the document and build the index
        reader = SimpleDirectoryReader(input_files=[tmp_text_file_path])
        data = reader.load_data()
        index = VectorStoreIndex.from_documents(data, embed_model=embedding_model)
        query_engine = index.as_query_engine(streaming=True, similarity_top_k=3)

        # Query input
        query = st.text_input("Enter your query:", value=st.session_state.query, key="query_input")

        if query:
            # Add the query to the conversation history
            st.session_state.conversation_history.append({"role": "user", "content": query})
            st.session_state.query = query

            # Stream response with page citation
            response = query_engine.query(query)
            response.print_response_stream()

            # Process the response to include page references
            response_text = ""
            for node in response.source_nodes:
                text_fmt = node.node.get_content().strip().replace("\n", " ")[:1000]
                page_number = node.node.metadata.get('page_label', 'unknown')
                response_text += f"{text_fmt} (page {page_number})\n\n"

            # Add the response to the conversation history
            st.session_state.conversation_history.append({"role": "assistant", "content": response_text})

            # Display the conversation history
            st.write("### Conversation History")
            for entry in st.session_state.conversation_history:
                if entry["role"] == "user":
                    st.write(f"**User:** {entry['content']}")
                else:
                    st.write(f"**Assistant:** {entry['content']}")

        # Clean up the temporary files
        os.remove(tmp_file_path)
        os.remove(tmp_text_file_path)
