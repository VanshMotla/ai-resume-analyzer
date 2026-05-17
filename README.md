# 🎯 AI-Powered Resume Analyzer

> Full-stack web application that uses AI and NLP to analyze resumes against job descriptions, providing actionable feedback, scoring, and ATS compatibility checks.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

- ✅ **Resume Upload** - Supports PDF and DOCX formats
- ✅ **AI-Powered Analysis** - Uses NLP and machine learning
- ✅ **Match Scoring** - Calculates overall compatibility (0-100%)
- ✅ **Keyword Analysis** - Identifies matched and missing keywords
- ✅ **Skill Gap Detection** - Shows required skills you're missing
- ✅ **ATS Compatibility Check** - Ensures resume passes ATS systems
- ✅ **Smart Suggestions** - AI-generated improvement recommendations
- ✅ **Visual Dashboard** - Beautiful charts and progress bars

## 🛠️ Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- spaCy & NLTK - Natural Language Processing
- scikit-learn - Machine Learning algorithms
- PyPDF - PDF text extraction
- python-docx - DOCX file processing

**Frontend:**
- HTML5/CSS3 - Modern, responsive UI
- Vanilla JavaScript - No frameworks needed
- Chart.js - Data visualization

**AI/ML:**
- TF-IDF Vectorization - Keyword importance
- Cosine Similarity - Semantic matching
- Pattern Matching - Technical skill detection

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository:**
```bash
git clone https://github.com/YOUR-USERNAME/ai-resume-analyzer.git
cd ai-resume-analyzer
```

2. **Install backend dependencies:**
```bash
cd backend
pip install -r requirements.txt
python -m nltk.downloader punkt stopwords punkt_tab
```

3. **Start the backend server:**
```bash
python app.py
```

4. **Start the frontend** (in a new terminal):
```bash
cd frontend
python -m http.server 3000
```

5. **Open in browser:**
http://localhost:3000
## 📖 Usage

1. Upload your resume (PDF or DOCX)
2. Paste the job description
3. Click "Analyze Resume"
4. Review the AI-generated insights:
   - Overall match score
   - Keyword analysis
   - Skill gaps
   - ATS compatibility
   - Improvement suggestions

## 📊 Project Structure
