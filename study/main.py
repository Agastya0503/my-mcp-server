from fastapi import FastAPI, HTTPException
from models import NotesInput, OutputData
from utils import summarize_text, generate_fixed_er_question, classify_level

app = FastAPI(title="Smart Study Buddy")

@app.post("/process_notes", response_model=OutputData)
def process_notes(notes: NotesInput):
    topic = notes.topic.lower().strip()
    content = notes.content.lower()

    if topic not in content:
        raise HTTPException(
            status_code=400,
            detail="Invalid topic: not found in the document."
        )

    summary = summarize_text(notes.content)
    qna = generate_fixed_er_question()
    level = classify_level(notes.content)

    return OutputData(
        summary=summary,
        twelve_mark_question=qna,
        level=level
    )