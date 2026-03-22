# streamlit run simple_web_chatbot.py

import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_classic.chains import LLMChain
from langchain_core.prompts import PromptTemplate


# --- Streamlit UI ---
st.title("Ollama Chatbot with Streamlit & Langchain")

# Initialize session state to store conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# --- LLM Setup ---
model_name = "gemma3"  # Replace with your Ollama model name
llm = OllamaLLM(model=model_name, verbose=False)  # verbose=True for debugging


# --- Prompt Template ---
template = """You are a helpful assistant.  Answer the user's questions based on your knowledge.
{question}"""
prompt = PromptTemplate(template=template, input_variables=["question"])


# --- Chat Interface ---
def generate_response(user_input):
    """Generates a response from the LLM."""
    try:
        response = llm.invoke(prompt.format(question=user_input))
        return response
    except Exception as e:
        return f"An error occurred: {e}"


st.write("Enter your message:")
user_input = st.text_input("Message:", "")

if user_input:
    with st.spinner("Generating response..."):
        response = generate_response(user_input)
    st.write(f"Assistant: {response}")
    st.session_state.conversation_history.append({"user": user_input, "assistant": response})

# --- Display Conversation History (Optional) ---
# if st.checkbox("Show Conversation History"):
#     for turn in st.session_state.conversation_history:
#         st.write(f"User: {turn['user']}")
#         st.write(f"Assistant: {turn['assistant']}")

