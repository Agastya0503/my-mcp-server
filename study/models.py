from pydantic import BaseModel
from typing import Dict

class NotesInput(BaseModel):
    topic: str
    content: str

class OutputData(BaseModel):
    summary: str
    twelve_mark_question: Dict[str, str]
    level: str