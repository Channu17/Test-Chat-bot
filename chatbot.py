import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage
import os
from dotenv import load_dotenv
load_dotenv()


groq_api_key = os.getenv("GROQ_API_KEY")

llm = ChatGroq(groq_api_key  = groq_api_key, model="llama-3.3-70b-versatile", temperature=0.75)

st.title("Conversational chat bot with context")

store={}

if 'flowmessages' not in st.session_state:
    st.session_state['flowmessages'] = [
        AIMessage(content="Hello! I am your Assistant. How can I Help you today?")
    ]


def get_response(question):
    st.session_state['flowmessages'].append(HumanMessage(content=question))
    answer = llm(st.session_state['flowmessages'])
    st.session_state['flowmessages'].append(AIMessage(content=answer.content))
    return answer.content
    
def get_joke():
    return get_response("Tell me a joke")

def get_ideas():
    return get_response("Give me a Gen Ai project ideas")

def food():
    return get_response("suggest me north indian food")

st.button("Tell me a joke", on_click=get_joke)
st.button("Gen Ai project ideas", on_click=get_ideas)
st.button("North Indian food", on_click=food)

for message in st.session_state['flowmessages']:
    if isinstance(message, HumanMessage):
        st.write(f"**You:** {message.content}")
    elif isinstance(message, AIMessage):
        st.write(f"**AI:** {message.content}")

if user_input := st.chat_input(placeholder="Ask anything"):
    response = get_response(user_input)
    st.write(f"**You:** {user_input}")
    st.write(f"**AI:** {response}")
    max_history = 10
    if len(st.session_state['flowmessages']) > max_history:
        st.session_state['flowmessages'] = st.session_state['flowmessages'][-max_history:]

st.button("clear chat", on_click=lambda: st.session_state.pop('flowmessages', None))