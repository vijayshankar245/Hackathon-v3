import os
from flask import Flask,redirect,url_for,render_template,request,jsonify
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_community.retrievers import AzureAISearchRetriever
import getpass
import os


from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from langchain_openai import AzureChatOpenAI

os.environ["AZURE_AI_SEARCH_SERVICE_NAME"] = ""
os.environ["AZURE_AI_SEARCH_INDEX_NAME"] = "master-business-incidents2"
os.environ["AZURE_AI_SEARCH_API_KEY"] = ""

os.environ["AZURE_OPENAI_ENDPOINT"] = ""
os.environ["AZURE_OPENAI_API_KEY"] = ""


retriever = AzureAISearchRetriever(
    content_key="content", top_k=1, index_name="master-business-incidents2"
)



llm = AzureChatOpenAI(
    azure_deployment="gpt-4o",  # or your deployment
    api_version="2024-08-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    # other params...
)


message = """
<Instructions>

You are a powerful AI-Assistant and you will be given with historical ticket description and corresponding resolution as context , your task is to use this context to generate resolution for current ticket being raised by the user. The details of current ticket description will be provided to you as well.

<context>

{context}

</context>

Generate resolution for current ticket description using the context provided above, also make sure to follow the rules mentioned below

<rules>

1.The ticket resolution provided for current ticket should only be generated using context provided, if required information is not in the context provided then generate response as I do not have required information to provide resolution for this ticket.
2.The ticket resolution provided for current ticket should be in the same format as historical ticket resolution provided in the context
3.If the current ticket is a major incident then generate a detailed resolution with elaborate recommendation for next steps.If the current ticket is a major incident then generate a detailed resolution with elaborate recommendation for next steps.
4. Do not show title information in the generated response.


</rules>

Current Ticket Description:

{question}

</Instructions>

Assistant:"""
prompt = ChatPromptTemplate.from_messages([("human", message)])

rag_chain = {"context": retriever, "question": RunnablePassthrough()} | prompt | llm

app = Flask(__name__)

# Serve the main HTML page
@app.route('/')
def index():
    return render_template("UI v3.html")
    
# @app.route('/next_page')  
# def next_page():  
    # return render_template('second.html') 


@app.route('/run-script', methods=['POST'])
def llm_call():
    question =  request.json.get('content', '')
    response = rag_chain.invoke(question)
    llm_result = response.content
    return llm_result
    
if __name__ == '__main__':
    app.run(debug=True)






 