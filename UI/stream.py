from openai import OpenAI
import streamlit as st
import shelve
import pandas as pd
import numpy as np
from openai import AzureOpenAI



#df = pd.read_csv(r"C:\Users\USithiah\Documents\Incidents_Test_Database.csv")
df = pd.read_csv(r"C:\Hackathon\Azure Hackathon V2\UI\Incidents_Test_Database.csv")
# # st.write ("data",data)

with st.sidebar:
     st.title('IT Incidents')
     streaming_on = st.toggle('Streaming')

st.title("Streamlit Chatbot Interface")

inci_type = df["incident type"].unique()
incident_choice = st.sidebar.selectbox('Select Your Incident Type:', inci_type)

label = df["label"].loc[df["incident type"] == incident_choice].unique()
label_choice = st.sidebar.selectbox('Select Your label:', label)


chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["incident type", "label"])
st.area_chart(chart_data)



USER_AVATAR = "👤"
BOT_AVATAR = "🤖"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

deployment_name = "gpt-4o"

client = AzureOpenAI(
    azure_endpoint = 'https://gh018-m3fob2dq-swedencentral.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview',
    api_key = '5JYysB7CedH4g26m0WwUhPqDgkcvDKu6PWVmMTwHfKpvhwZ6pbizJQQJ99AKACfhMk5XJ3w3AAAAACOGjeKe',
    api_version = '2024-08-01-preview',
)
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

# Load chat history from shelve file
# def load_chat_history():
#     with shelve.open("chat_history") as db:
#         return db.get("messages", [])


# # Save chat history to shelve file
# def save_chat_history(messages):
#     with shelve.open("chat_history") as db:
#         db["messages"] = messages


# Initialize or load chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = load_chat_history()
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]    

# Sidebar with a button to delete chat history
with st.sidebar:
    if st.button("Delete Chat History"):
        st.session_state.messages = []
        save_chat_history([])

# Display chat messages
for message in st.session_state.messages:
    avatar = USER_AVATAR if message["role"] == "user" else BOT_AVATAR
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
#full_response = ""
# Main chat interface
if prompt := st.chat_input("How can I help?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=USER_AVATAR):
         #st.markdown(prompt)
         st.write(prompt)

    with st.chat_message("assistant", avatar=BOT_AVATAR):
        message_placeholder = st.empty()
        full_response = ""

        response = client.chat.completions.create(
            model=deployment_name,            
            messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"}],                    
                    )
        # for response in client.chat.completions.create (
        #     model=deployment_name,
        #     messages=[
        #         {"role": "system", "content": "You are a helpful assistant."},
        #         {"role": "user", "content": "What is Azure OpenAI?"}]
        #         ):
        full_response = response.choices[0].message.content
            #or ""
            #message_placeholder.markdown(full_response + "|")
    message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})