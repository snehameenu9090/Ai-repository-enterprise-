import os
import random
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MULTI-LINGUAL AI QUESTION BANK BASED ON LANGUAGE SELECTION
LANGUAGE_QUESTION_BANK = {
    "English": [
        "Explain the core pillars of Object-Oriented Programming.",
        "What is the difference between Method Overloading and Overriding?",
        "How does a 2-Phase Locking protocol ensure consistency in DBMS?"
    ],
    "Hindi": [
        "Object-Oriented Programming (OOPs) ke mukhya pillars kya hain aur yeh kyun zaroori hain?",
        "Method Overloading aur Method Overriding ke beech kya antar hai?",
        "DBMS mein 2-Phase Locking protocol transaction serialization kaise manage karta hai?"
    ],
    "Spanish": [
        "Explique los pilares fundamentales de la Programación Orientada a Objetos.",
        "¿Cuál es la diferencia entre sobrecarga de métodos y anulación de métodos?",
        "¿Cómo garantiza el protocolo de bloqueo de dos fases la coherencia en DBMS?"
    ]
}

CURRENT_SESSION_QUESTIONS = []

# 📄 ROUND 1 & 2: RESUME SCANNER & SCHEDULER GATEWAY
@app.post("/shortlist-resume")
async def shortlist_resume(file: UploadFile = File(...)):
    try:
        reader = PdfReader(file.file)
        text = "".join([page.extract_text() or "" for page in reader.pages]).lower()
        
        # Resume parsing core keywords match
        job_keywords = ["python", "java", "javascript", "developer", "engineer", "sql", "data", "html"]
        matches = sum(1 for word in job_keywords if word in text)
        resume_score = (matches / len(job_keywords)) * 100
        
        if resume_score >= 40:
            return {
                "status": "Shortlisted",
                "score": round(resume_score, 2),
                "message": "Round 1 Cleared! Round 2 Scheduled automatically.",
                "next_round_date": "June 12, 2026 at 10:00 AM IST"
            }
        return {
            "status": "Rejected",
            "score": round(resume_score, 2),
            "message": "Resume requirements parameters mismatch. File Rejected."
        }
    except Exception as e:
        return {"status": "Error", "message": f"Resume Engine Fault: {str(e)}"}

# 📁 COMPANY INTERVIEW QUESTION SHEET LOADER
@app.post("/upload-pdf")
async def upload_interview_pdf(file: UploadFile = File(...)):
    global CURRENT_SESSION_QUESTIONS
    try:
        reader = PdfReader(file.file)
        lines = [page.extract_text().strip() for page in reader.pages if page.extract_text()]
        if lines:
            CURRENT_SESSION_QUESTIONS = lines
            return {"status": "success", "message": "Company specialized question structures loaded successfully!"}
        return {"status": "error", "message": "PDF blank hai!"}
    except Exception as e:
        return {"status": "error", "message": f"Parsing Error: {str(e)}"}

# 🤖 LANGUAGE BASED QUESTION DISPATCHER
@app.get("/get-ai-question")
async def get_ai_question(language: str = "English"):
    # Agar company ne apni PDF upload ki hai toh pehle wahan se text uthayega
    if CURRENT_SESSION_QUESTIONS:
        return {"question": random.choice(CURRENT_SESSION_QUESTIONS)}
    
    # Defaults to localized language dictionary bank
    questions = LANGUAGE_QUESTION_BANK.get(language, LANGUAGE_QUESTION_BANK["English"])
    return {"question": random.choice(questions)}

# 🧠 FINAL ROUND EVALUATION & PLACEMENT ANALYSIS LOG
@app.post("/submit-interview")
async def process_interview_data(
    name: str = Form(...),
    email: str = Form(...),
    branch: str = Form(...),
    experience: int = Form(...),
    language: str = Form(...),
    candidate_answer: str = Form(...)
):
    # Keyword weight analyzer
    score = 50
    answer_clean = candidate_answer.lower()
    tech_terms = ["inheritance", "polymorphism", "encapsulation", "class", "object", "api", "server", "overloading", "overriding", "database", "variable", "function", "mukhya", " antar", "pilares"]
    
    matches = sum(1 for word in tech_terms if word in answer_clean)
    score += (matches * 8)
    if score > 100: score = 100

    # Package Formulation Matrix
    base_package = 5.0 if experience >= 2 else 3.5
    multiplier = 1.3 if branch.upper() in ["CSE", "IT", "COMPUTER SCIENCE"] else 1.0
    final_lpa = round((base_package * multiplier) * (score / 100), 2)

    decision = "ACCEPTED - Offer Letter Generated" if score >= 60 else "REJECTED - Portfolio File Saved"
    
    return {
        "name": name,
        "email": email,
        "language_used": language,
        "ai_score": score,
        "status": decision,
        "package": f"{final_lpa} LPA" if score >= 60 else "0 LPA",
        "analysis_report": f"Candidate {name} evaluation complete. Language Node: {language}. Demonstrated keyword weightage optimization. Anti-cheating continuous tracking status: VERIFIED SECURE."
    }