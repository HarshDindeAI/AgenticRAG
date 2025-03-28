import os
import json
import hashlib
import pymupdf
import pandas as pd
import pymupdf4llm
from langchain_postgres import PGVector
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import dotenv
dotenv.load_dotenv()
DATA_FOLDER = "../../data"  # Folder where PDFs are stored
class Vectorizer:
    def __init__(self):
        
        model = HuggingFaceEmbeddings(model_name = "all-MiniLM-L6-v2", model_kwargs = {"device": os.getenv("DEVICE","cpu")})

        self.vector_store = PGVector(
            embeddings=model,
            collection_name=os.getenv("COLLECTION_NAME","my_docs"),
            connection=os.getenv("POSTGRES_CONNECTION_STRING",),
            use_jsonb=True,
        )
    def convert_text(self, text, metadata=None):
        doc = []
        i=0
        if metadata is not None:
            for page in text:
                doc.append(Document(page_content=page,metadata=metadata[i]))
                i+=1
        else:
            for page in text:
                doc.append(Document(page_content=page))
        return doc
    def embed_text(self, text, metadata=None):
        return self.vector_store.add_documents(self.convert_text(text, metadata = metadata))

def load_existing_hashes(pdf_path):
    """Load existing hashes from a JSON file."""
    if os.path.exists(pdf_path+".md5"):
        with open(pdf_path+".md5", "r") as f:
            return f.read()
    return None


def generate_md5(file_path):
    """Generate MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def extract_text_pagewise(pdf_path):
    """Extract text from a PDF file page by page."""
    doc = pymupdf.open(pdf_path)
    pages_text = []
    metadata = []
    for i in range(doc.page_count):
        page_md = pymupdf4llm.to_markdown(doc, pages=[i])
        pages_text.append(page_md)
        metadata.append({"page_number": i+1, "pdf_name":pdf_path.split("\\")[-1] })
    return pages_text, metadata

def process_pdfs():
    """Check PDFs, process new or updated ones, and save extracted text as JSON."""
    client = Vectorizer()
    for file_name in os.listdir(DATA_FOLDER):
        file_path = os.path.join(DATA_FOLDER, file_name)
        existing_hashes = load_existing_hashes(file_path)
        if os.path.isfile(file_path) and file_name.lower().endswith(".pdf"):
            new_md5 = generate_md5(file_path)
            print
            if existing_hashes is None or existing_hashes != new_md5:
                # Process the updated or new PDF
                print(f"Processing: {file_name}")
                text , metadata = extract_text_pagewise(file_path)
                print(metadata)
                try:
                    client.embed_text( text, metadata = metadata)
                except Exception as e:
                    print(f"Error: {e}")
                    return None
                with open(file_path+".md5", "w") as f:
                    f.write(new_md5)             
            else:
                print(f"Skipping (No Changes): {file_name}")



if __name__ == "__main__":
    process_pdfs()
