import streamlit as st
import openai
import base64

# Replace with your actual encoded API key
encoded_api_key = "c2stcHJvai1OQktuTWx3Y0tKZmZOck5Zc0hpdVQzQmxia0ZKU3hvM1RiUWZhdjVGQ1Y4YVk1eWY="

# Ensure correct padding
if len(encoded_api_key) % 4 != 0:
    encoded_api_key += "=" * (4 - len(encoded_api_key) % 4)

# Decode the API key
try:
    openai_api_key = base64.b64decode(encoded_api_key).decode("utf-8")
except Exception as e:
    print("Error decoding API key:", e)
    raise

# Set up OpenAI API key
openai.api_key = openai_api_key

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

st.title("💬 My Chatbot for 9th Grade")
st.caption("🚀 A Streamlit chatbot powered by Me")

# Initialize the session state to store messages
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from the session state
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Chat input and processing
if prompt := st.chat_input():
    if not selected_subject:
        st.info("Please select a subject to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Constructing a prompt that includes the selected subject
    subject_prompt = f"The student is studying {selected_subject}. Please provide a helpful and detailed response."
    full_prompt = f"{subject_prompt}\n\n{prompt}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": subject_prompt}] + st.session_state.messages
    )
    msg = response.choices[0]["message"]["content"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
