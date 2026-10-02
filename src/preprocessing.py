import re
import streamlit as st
from src.pdf_extractor import extract_text_from_pdf


# Skill list
SKILLS = [
    "python",
    "sql",
    "pandas",
    "numpy",
    "machine learning",
    "deep learning",
    "git",
    "excel",
    "java",
    "c++",
    "html",
    "css",
    "javascript"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    text = clean_text(text)

    found = []

    for skill in SKILLS:
        if skill in text:
            found.append(skill.title())

    return sorted(found)