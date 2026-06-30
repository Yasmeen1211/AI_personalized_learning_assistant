from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_core.documents import Document

import os
import shutil


def build_vector_store(text):

    # --------------------------------
    # DELETE OLD VECTOR STORE
    # --------------------------------

    if os.path.exists("faiss_index"):

        shutil.rmtree("faiss_index")

    # --------------------------------
    # SPLIT TEXT
    # --------------------------------

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=500,

        chunk_overlap=50
    )

    chunks = splitter.split_text(text)

    # --------------------------------
    # CREATE DOCUMENTS
    # --------------------------------

    docs = [

        Document(page_content=chunk)

        for chunk in chunks
    ]

    # --------------------------------
    # EMBEDDINGS
    # --------------------------------

    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # --------------------------------
    # CREATE FAISS VECTOR STORE
    # --------------------------------

    db = FAISS.from_documents(

        docs,

        embeddings
    )

    # --------------------------------
    # SAVE VECTOR STORE
    # --------------------------------

    db.save_local("faiss_index")

    return db

