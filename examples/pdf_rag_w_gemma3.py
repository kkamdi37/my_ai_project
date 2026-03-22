#!/bin/env python3
#
# pip3 install langchain langchain-community langchain-core
# pip3 install langchain-ollama pypdf faiss-cpu
#

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from langchain_ollama import OllamaEmbeddings

# Load your document (replace with your file path)
loader = PyPDFLoader("ENTER_YOUR_PDF_FILE_HERE")
documents = loader.load()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(documents)

embeddings = OllamaEmbeddings( model="nomic-embed-text" )

# Create a FAISS vector store in memory
vectorstore = FAISS.from_documents(docs, embeddings)
retriever = vectorstore.as_retriever()


################################################################################


from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
llm = ChatOllama(model="gemma3")

# Define a strict prompt to ensure the model uses only the provided context
template = """Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
{context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)


################################################################################


from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Build the RAG chain
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}

    | prompt
    | llm
    | StrOutputParser()
)

# Invoke the chain with a question
question = "Summarize the main idea of this document."
response = rag_chain.invoke(question)

print( response )

