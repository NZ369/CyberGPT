from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from llms.azure_llms import create_azure_embedder
from llms.cohere_llms import create_cohere_embedder
from langchain.vectorstores import FAISS

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks, type="azure", database="FAISS"):
    if type == "azure":
        embeddings = create_azure_embedder()
    else:
        embeddings = create_cohere_embedder()
    if database == "FAISS":
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    else:
        vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore