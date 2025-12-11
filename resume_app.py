import streamlit as st
import re
import docx2txt
import fitz
import pandas as pd
from sentence_transformers import SentenceTransformer, util

# --------------------------
# LOAD MODEL
# --------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------
# TEXT EXTRACTION
# --------------------------
def extract_text(file):
    if file.name.endswith(".pdf"):
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = " ".join(page.get_text() for page in doc)
        return text

    elif file.name.endswith(".docx"):
        return docx2txt.process(file)

    elif file.name.endswith(".txt"):
        return file.read().decode("utf-8")

    else:
        return "Unsupported file format."

# --------------------------
# CLEANING
# --------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

# --------------------------
# SKILL EXTRACTION
# --------------------------
skills_list = [
    "python","java","sql","nlp","machine learning","deep learning",
    "pandas","numpy","tensorflow","pytorch","docker","kubernetes",
    "power bi","tableau","excel","data analysis","statistics","aws","git"
]

def extract_skills(text):
    found = []
    for skill in skills_list:
        if skill in text:
            found.append(skill)
    return list(set(found))

# --------------------------
# STREAMLIT APP
# --------------------------
st.title("📄 Resume Analyzer (NLP + ML)")

uploaded_file = st.file_uploader("Upload Resume (PDF / DOCX / TXT)", type=["pdf","docx","txt"])

job_description = st.text_area("Paste Job Description Here:")

if uploaded_file and job_description:

    st.subheader("Extracting Resume Text...")
    resume_text = extract_text(uploaded_file)

    if resume_text == "Unsupported file format.":
        st.error("Please upload PDF, DOCX or TXT only.")
    else:
        clean_resume = clean_text(resume_text)

        st.subheader("Extracted Skills")
        skills = extract_skills(clean_resume)
        st.write(skills)

        st.subheader("Similarity Score")
        resume_emb = model.encode(clean_resume, convert_to_tensor=True)
        jd_emb = model.encode(job_description, convert_to_tensor=True)

        similarity = util.cos_sim(resume_emb, jd_emb).item()
        st.metric("Resume Match %", f"{similarity*100:.2f}%")

        missing = set(skills_list) - set(skills)
        st.subheader("Missing Skills")
        st.write(list(missing))

        st.subheader("Raw Extracted Text")
        with st.expander("Show Resume Text"):
            st.write(resume_text)
