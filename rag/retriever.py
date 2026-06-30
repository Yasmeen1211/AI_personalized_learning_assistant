from langchain_community.vectorstores import FAISS

from langchain_community.embeddings import HuggingFaceEmbeddings

def retrieve_topic_content(topic):

    embeddings = HuggingFaceEmbeddings(

        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(

        "faiss_index",

        embeddings,

        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(

        topic,

        k=3
    )

    retrieved_text = ""

    for doc in docs:

        retrieved_text += doc.page_content + "\n"

    return retrieved_text