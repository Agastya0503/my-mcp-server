from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Smart Study Buddy")

class NotesInput(BaseModel):
    topic: str
    content: str

class OutputData(BaseModel):
    summary: str
    twelve_mark_question: Dict[str, str]
    level: str

def summarize_text(text: str) -> str:
    import re
    sentences = re.split(r'(?<=[.!?]) +', text)
    summary = " ".join(sentences[:3]) if sentences else text[:300]
    return summary.strip()

def generate_fixed_er_question() -> Dict[str, str]:
    question = (
        "Describe the Entity-Relationship (ER) Model in detail. "
        "Explain its key components such as entities, attributes, and relationships. "
        "Illustrate how ER modeling is used in designing databases with real-life examples."
    )

    answer = (
        "The Entity-Relationship (ER) Model is a conceptual framework used to describe the structure of a database in terms of entities, "
        "their attributes, and relationships. It was proposed by Peter Chen in 1976 and serves as the first step in the database design process, "
        "particularly for relational databases.\n\n"
        "An entity is an object or concept about which data is stored. Entities can be physical (like Student, Car, Employee) or abstract "
        "(like Course, Project). Each entity has a set of attributes, which are properties that describe the entity. For instance, a Student entity "
        "may have attributes like Student_ID, Name, Email, and DOB.\n\n"
        "A relationship represents an association between two or more entities. For example, a Student enrolls in a Course, or a Teacher teaches a Subject. "
        "Relationships can have cardinalities such as one-to-one, one-to-many, or many-to-many, which describe how many instances of one entity relate to another.\n\n"
        "There are also special constructs like: Weak entities, which depend on other entities; Multi-valued attributes, which can have multiple values (e.g., PhoneNumbers); "
        "and Generalization/specialization, which define hierarchies among entities.\n\n"
        "ER Diagrams are visual representations of the ER model. They use rectangles for entities, ellipses for attributes, diamonds for relationships, and lines to connect them.\n\n"
        "In real life, ER modeling is used in designing systems such as: University Databases – where Students, Courses, and Faculty are entities; "
        "E-commerce Platforms – with entities like User, Order, Product, and Payment.\n\n"
        "In conclusion, the ER Model provides a clear and logical blueprint for designing normalized, relational database schemas that ensure data consistency and easy maintenance."
    )

    return {"question": question, "answer": answer}

def classify_level(text: str) -> str:
    word_count = len(text.split())
    if word_count < 50:
        return "Beginner"
    elif word_count < 150:
        return "Intermediate"
    return "Advanced"

@app.post("/process_notes", response_model=OutputData)
def process_notes(notes: NotesInput):
    topic = notes.topic.lower().strip()
    content = notes.content.lower()

    # Return 400 if topic not found
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
