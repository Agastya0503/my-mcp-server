import streamlit as st
import requests
import fitz  # PyMuPDF

st.set_page_config(page_title="Smart Study Buddy", page_icon="📚")

st.title("📚 Smart Study Buddy")
st.subheader("AI-powered summary, important topics, 12-mark question & topic level")

# Step 1: Topic input
topic = st.text_input("📌 Enter Topic")

# Step 2: File upload
st.markdown("### 📂 Import your file here (Text, Markdown, PDF)")
uploaded_file = st.file_uploader("Upload your notes", type=["txt", "md", "pdf"])

# Helper: extract text
def read_file(file) -> str:
    ext = file.name.split(".")[-1].lower()
    if ext in ["txt", "md"]:
        return file.read().decode("utf-8")
    elif ext == "pdf":
        with fitz.open(stream=file.read(), filetype="pdf") as doc:
            return "\n".join(page.get_text() for page in doc)
    return ""

# Helper: extract keywords (basic)
def extract_keywords(text, top_n=5):
    from collections import Counter
    import re
    words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
    stopwords = {"this", "that", "with", "from", "have", "they", "which", "their", "about", "where", "will", "your"}
    filtered = [w for w in words if w not in stopwords]
    most_common = Counter(filtered).most_common(top_n)
    return [word.title() for word, _ in most_common]

# Generate output
if topic and uploaded_file:
    content = read_file(uploaded_file)

    if st.button("📊 Generate Output"):
        with st.spinner("Analyzing..."):
            try:
                response = requests.post("http://localhost:8000/process_notes", json={
                    "topic": topic,
                    "content": content
                })

                if response.status_code == 200:
                    result = response.json()
                    st.success("✅ Output Generated")

                    # Summary
                    st.markdown("### ✨ Summary")
                    st.info(result["summary"])

                    # Important topics
                    st.markdown("### 📖 Important Topics to Learn")
                    keywords = extract_keywords(content, top_n=6)
                    for kw in keywords:
                        st.write(f"- {kw}")

                    # 12-mark Q&A
                    st.markdown("### 📝 12-Mark Question & Answer")
                    st.write(f"**Q:** {result['twelve_mark_question']['question']}")
                    st.write(f"**A:** {result['twelve_mark_question']['answer']}")

                    # Topic level
                    st.markdown("### 📊 Topic Level")
                    st.write(f"**Level:** {result['level']}")
                else:
                    st.error("❌ Failed to process notes.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
else:
    st.info("Please enter a topic and upload your notes to begin.")
