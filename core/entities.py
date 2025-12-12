# core/entities.py
from dataclasses import dataclass
from typing import List

@dataclass
class DocumentChunk:
    id: str
    text: str

@dataclass
class ChatMessage:
    role: str   # "user" or "assistant" or "system"
    text: str
