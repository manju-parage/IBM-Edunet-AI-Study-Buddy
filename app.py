import streamlit as st
import google.generativeai as genai

#  PAGE SETTINGS 
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Study Buddy")
st.write("Learn any topic and also ask questions instantly")

#  GEMINI API SETUP 
genai.configure(api_key="YOUR_API_KEY_HERE")
model = genai.GenerativeModel("gemini-2.5-flash")

#  SESSION MEMORY 
if "topic" not in st.session_state:
    st.session_state.topic = ""

if "content" not in st.session_state:
    st.session_state.content = ""

#   CHAT HISTORY MEMORY
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

#  SIDEBAR HISTORY 
st.sidebar.title("🕒 Chat History")

for chat in st.session_state.chat_history:
    st.sidebar.write("❓ " + chat["question"])

#  Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat history cleared!")

#  TOPIC INPUT 
topic_input = st.text_input("📚 Enter topic you want to learn")

generate_btn = st.button("🚀 Generate Study Content")

#  CONTENT GENERATION 
if generate_btn and topic_input:

    st.session_state.topic = topic_input

    with st.spinner("Generating content..."):

        prompt = f"""
        Topic: {topic_input}

        Create study material in SIMPLE student-friendly language.

        Give output in this format:

        ### Explanation
        Explain clearly with examples.

        ### Notes
        Give short bullet point notes.

        ### Quiz
        Create 5 MCQ questions with answers.
        """

        response = model.generate_content(prompt)
        st.session_state.content = response.text

#  SHOW CONTENT 
if st.session_state.content:
    st.success("Content Generated Successfully!")
    st.markdown(st.session_state.content)

    #  DOWNLOAD BUTTON
    st.download_button(
        label="📥 Download Study Notes",
        data=st.session_state.content,
        file_name="study_notes.txt",
        mime="text/plain"
    )

#  ASK QUESTION SECTION 
st.divider()
st.subheader("💬 Ask Your Question")

question = st.text_input("Type your question here")
ask_btn = st.button("Ask AI")

if ask_btn and question and st.session_state.topic:

    with st.spinner("Thinking..."):

        reply = model.generate_content(
            f"Topic is {st.session_state.topic}. Answer simply for student:\n{question}"
        )

    #  SAVE CHAT
    st.session_state.chat_history.append(
        {"question": question, "answer": reply.text}
    )

#  SHOW FULL CHAT 
for chat in st.session_state.chat_history:
    st.write("### ❓ You:")
    st.write(chat["question"])
    st.write("### 🤖 AI:")
    st.write(chat["answer"])
