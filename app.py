import os
import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Set up sidebar with subject checkboxes
with st.sidebar:
    st.header("Select a Subject")
    subjects = ["Maths", "Physics", "Chemistry", "Biology", "English", "Urdu", "Pak Studies", "General Mathematics",
                "Computer Science"]
    selected_subject = None
    for subject in subjects:
        if st.checkbox(subject):
            selected_subject = subject
            break

st.title("💬 My Chatbot for 9th Grade ")
st.caption("🚀 A Streamlit chatbot powered by Me")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not selected_subject:
        st.info("Please select a subject to continue.")
        st.stop()

    openai.api_key = openai_api_key
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Constructing a prompt that includes the selected subject
    subject_prompt = f"The student is studying {selected_subject}. Please provide a helpful and detailed response."
    full_prompt = f"{subject_prompt}\n\n{prompt}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": subject_prompt}] + st.session_state.messages
    )
    msg = response.choices[0].message["content"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
