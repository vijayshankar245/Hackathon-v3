from flask import Flask,redirect,url_for,render_template,request,jsonify
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
import getpass
import os

LANGCHAIN_TRACING_V2=True
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="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"
LANGCHAIN_PROJECT="pr-overcooked-density-92"



app = Flask(__name__)

# Serve the main HTML page
@app.route('/')
def index():
    return render_template("UI v3.html")


loader = TextLoader("Tickets.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100,separators=["\n\n","\n","."," ",""])
texts = text_splitter.split_documents(documents)
vectorstore = Chroma.from_documents(
    texts,
    embedding=OpenAIEmbeddings(),
)

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

message = """
Answer this question using the provided context only.

{question}

Context:
{context}
"""



llm = ChatOpenAI(model="gpt-4o-mini")

prompt = ChatPromptTemplate.from_messages([("human", message)])

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

@app.route('/run-script', methods=['POST'])
def llm_call():
    prompt =  request.json.get('content', '')
    response = rag_chain.invoke(prompt)
    llm_result = response.content
    return llm_result
    
if __name__ == '__main__':
    app.run(debug=True)






 