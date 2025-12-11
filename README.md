# AI-Powered Resume Analyzer (NLP + Streamlit + Sentence Transformers)

A complete Resume Analyzer that uses NLP and semantic similarity to evaluate resumes, extract skills, compute ATS match scores, and compare resumes against job descriptions. Includes a Streamlit UI and supports running in Google Colab using ngrok.

## Features
- Extracts resume text from PDF, DOCX, and TXT
- Cleans and preprocesses text
- Skill extraction using keyword matching
- ATS-style scoring based on similarity + skills
- Semantic similarity using SentenceTransformer MiniLM-L6-v2
- Streamlit UI
- ngrok tunnel support for Colab

## Tech Stack
Python, Streamlit, SentenceTransformers, docx2txt, PyMuPDF, ngrok

## Local Installation
pip install -r requirements.txt
streamlit run resume_app.py

## Running in Google Colab (ngrok)
!pip install streamlit pyngrok docx2txt pymupdf sentence-transformers
!ngrok config add-authtoken "YOUR_NGROK_TOKEN"

from pyngrok import ngrok
ngrok.kill()
public_url = ngrok.connect(8501)
print("Streamlit URL:", public_url)

!streamlit run resume_app.py & sleep 3

## Example Output
Extracted Skills: ['python', 'sql', 'nlp']
ATS Score: 82.45%
Missing Skills: ['aws', 'tensorflow']

## License
MIT License
