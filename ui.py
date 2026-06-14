import streamlit as st
from main import ask_question

st.set_page_config(
    page_title="YouTube RAG",
    page_icon="🎥"
)

st.title("🎥 YouTube RAG")

youtube_url = st.text_input(
    "YouTube URL"
)

language = st.selectbox(
    "Video Language",
    ["English", "Hindi"]
)

question = st.text_area(
    "Ask a question"
)

if st.button("Submit"):

    if not youtube_url:
        st.warning("Please enter a YouTube URL")

    elif not language:
        st.warning("Please enter a language")

    elif not question:
        st.warning("Please enter a question")

    else:
        with st.spinner("Processing..."):

            try:
                answer = ask_question(
                    youtube_url,
                    question,
                    language
                )

                st.success("Completed")

                st.subheader("Answer")
                st.write(answer)

            except Exception as e:
                st.error(str(e))