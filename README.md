# AI Resume Analyzer

AI Resume Analyzer is a web-based application that analyzes a candidate's resume against a job description and provides an ATS-style compatibility analysis.

The application uses Python, Streamlit, Natural Language Processing (NLP), and Google Gemini AI to identify matching skills, missing skills, strengths, and areas for improvement.

## Features

- Upload a resume in PDF format
- Enter a job description
- Extract text from the resume
- Analyze the resume against job requirements
- Calculate a resume-job match percentage
- Identify matched skills
- Identify missing skills
- Display candidate strengths
- Suggest practical resume improvements
- Generate final feedback
- Use a local ATS fallback when the Gemini API is temporarily unavailable

## Technologies Used

- Python
- Streamlit
- Google Gemini AI
- Google GenAI SDK
- Natural Language Processing (NLP)
- spaCy
- NLTK
- PyPDF
- Scikit-learn
- python-dotenv

## Project Structure

```text
AI-Resume-Analyser/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── prompts/
│   └── resume_prompt.txt
│
└── src/
    ├── __init__.py
    ├── config.py
    ├── llm_analyzer.py
    ├── pdf_extractor.py
    ├── preprocessing.py
    └── similarity.py