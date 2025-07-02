import streamlit as st
import requests

st.set_page_config(page_title="Smart Study Buddy", page_icon="📘")
st.title("📘 Smart Study Buddy")

st.markdown("""
<style>
    .stTextInput > label {
        font-weight: bold;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Topic input
topic = st.text_input("📌 Enter Topic")

# File upload
file = st.file_uploader("📂 Import your file here (Text or Markdown or PDF)", type=["txt", "md", "pdf"])

# Process button
if st.button("🚀 Process"):
    if not topic or not file:
        st.error("Please enter a topic and upload a file.")
    else:
        try:
            if file.name.endswith(".pdf"):
                import fitz
                with fitz.open(stream=file.read(), filetype="pdf") as doc:
                    content = "\n".join(page.get_text() for page in doc)
            else:
                content = file.read().decode("utf-8")
        except Exception as e:
            st.error(f"Could not read the uploaded file: {e}")
            content = ""

        payload = {"topic": topic, "content": content}
        try:
            response = requests.post("http://localhost:8000/process_notes", json=payload)
            if response.status_code == 200:
                data = response.json()
                st.success("✅ Topic Found and Processed!")
                st.markdown(f"### ✨ Summary\n{data['summary']}")
                st.markdown("### 📊 Topic Level")
                st.info(data['level'])
                st.markdown("### 📝 12-Mark Question")
                st.markdown(f"**Q: {data['twelve_mark_question']['question']}**")
                st.markdown(data['twelve_mark_question']['answer'])
            else:
                st.error(response.json()['detail'])
        except Exception as e:
            st.error(f"Something went wrong: {e}")
