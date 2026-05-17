# 🎯 AI-Powered Resume Analyzer

> **Full-Stack Web Application** that uses AI and NLP to analyze resumes against job descriptions, providing actionable feedback, scoring, and ATS compatibility checks.

Built by **Vansh Motla** | Portfolio Project for AI Developer Role

---

## 🌟 Features

### ✨ Core Functionality
- ✅ **Resume Upload** - Supports PDF and DOCX formats
- ✅ **AI-Powered Analysis** - Uses NLP and machine learning
- ✅ **Match Scoring** - Calculates overall compatibility (0-100%)
- ✅ **Keyword Analysis** - Identifies matched and missing keywords
- ✅ **Skill Gap Detection** - Shows required skills you're missing
- ✅ **ATS Compatibility Check** - Ensures resume passes ATS systems
- ✅ **Smart Suggestions** - AI-generated improvement recommendations
- ✅ **Visual Dashboard** - Beautiful charts and progress bars
- ✅ **Printable Reports** - Export analysis results

### 🧠 AI/ML Features
- TF-IDF for keyword extraction
- Cosine similarity for semantic matching
- NLP-based skill extraction
- Multi-factor scoring algorithm
- Automated weakness detection

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **spaCy & NLTK** - Natural Language Processing
- **scikit-learn** - Machine Learning algorithms
- **PyMuPDF** - PDF text extraction
- **python-docx** - DOCX file processing

### Frontend
- **HTML5/CSS3** - Modern, responsive UI
- **Vanilla JavaScript** - No frameworks needed
- **Chart.js** - Data visualization (ready to integrate)

### AI/NLP
- **TF-IDF Vectorization** - Keyword importance
- **Cosine Similarity** - Semantic matching
- **Named Entity Recognition** - Skill extraction
- **Pattern Matching** - Technical skill detection

---

## 📋 Prerequisites

Before running this project, make sure you have:

- **Python 3.8+** installed
- **pip** (Python package manager)
- **Modern web browser** (Chrome, Firefox, Edge)
- **Terminal/Command Prompt** access

---

## 🚀 Installation & Setup

### **Step 1: Install Backend Dependencies**

```bash
# Navigate to backend directory
cd resume-analyzer/backend

# Install all Python packages
pip install -r requirements.txt

# Download NLTK data (required)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

**Note:** Installation may take 2-3 minutes depending on your internet speed.

---

### **Step 2: Start the Backend Server**

```bash
# Make sure you're in the backend directory
cd resume-analyzer/backend

# Start the FastAPI server
python app.py
```

**Expected Output:**
```
🚀 Starting AI Resume Analyzer API Server...
📡 Server will run on: http://localhost:8000
📚 API docs available at: http://localhost:8000/docs
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **Backend is now running!** Keep this terminal window open.

---

### **Step 3: Open the Frontend**

**Option 1: Simple File Open**
```bash
# In a new terminal, navigate to frontend directory
cd resume-analyzer/frontend

# Open index.html in your default browser (Linux/Mac)
xdg-open index.html

# Or on Mac
open index.html

# On Windows, just double-click index.html
```

**Option 2: Using Python HTTP Server (Recommended)**
```bash
# Navigate to frontend directory
cd resume-analyzer/frontend

# Start a simple HTTP server
python -m http.server 3000

# Open browser and go to: http://localhost:3000
```

---

## 📖 How to Use

### **Step-by-Step Guide:**

1. **Open the Application**
   - Open `http://localhost:3000` in your browser
   - You'll see the upload form

2. **Upload Your Resume**
   - Click the "Browse" button
   - Select your resume file (PDF or DOCX)
   - File must be under 5MB

3. **Paste Job Description**
   - Copy the complete job description
   - Paste it into the text area
   - Minimum 50 characters required

4. **Click "Analyze Resume"**
   - The AI will process your resume (takes 5-10 seconds)
   - Loading animation will show progress

5. **Review Results**
   - **Overall Match Score** - Your compatibility percentage
   - **Keyword Analysis** - What matched and what's missing
   - **Skill Gap** - Required skills you don't have
   - **ATS Score** - Will your resume pass ATS systems?
   - **Suggestions** - Actionable improvement tips

6. **Take Action**
   - Print the report for reference
   - Update your resume based on suggestions
   - Re-analyze to see improvement

---

## 📊 Understanding the Scores

### **Overall Match Score (0-100%)**
- **80-100%** - Excellent match, apply with confidence
- **60-79%** - Good match, minor improvements needed
- **40-59%** - Moderate match, significant tailoring required
- **0-39%** - Poor match, major updates needed

### **Component Scores:**
- **Keyword Match** - How many JD keywords appear in your resume
- **Semantic Similarity** - Overall meaning/context alignment
- **Skill Match** - Technical skills alignment
- **ATS Compatibility** - Will ATS systems parse it correctly?

---

## 🎨 Project Structure

```
resume-analyzer/
│
├── backend/
│   ├── app.py                 # FastAPI server (main entry point)
│   ├── ai_analyzer.py         # AI analysis engine
│   ├── file_processor.py      # PDF/DOCX text extraction
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── index.html             # Main webpage
│   ├── styles.css             # Modern styling
│   └── app.js                 # Frontend logic & API calls
│
├── uploads/                   # Temporary file storage (auto-created)
│
└── README.md                  # This file
```

---

## 🔧 API Endpoints

### **Health Check**
```
GET /health
Response: {"status": "healthy", "timestamp": "..."}
```

### **Analyze Resume**
```
POST /api/analyze
Body (multipart/form-data):
  - resume: File (PDF/DOCX)
  - job_description: String

Response: Complete analysis report (JSON)
```

### **API Documentation**
Visit `http://localhost:8000/docs` for interactive API docs (Swagger UI)

---

## 🐛 Troubleshooting

### **Backend won't start:**
```bash
# Check if port 8000 is already in use
# Kill existing process or change port in app.py

# Verify Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### **"Cannot connect to API" error:**
- Ensure backend server is running on port 8000
- Check if `http://localhost:8000/health` returns data
- Verify no firewall is blocking the connection

### **File upload fails:**
- Check file size (must be under 5MB)
- Verify file format (only PDF and DOCX supported)
- Ensure file is not corrupted or password-protected

### **Low/inaccurate scores:**
- Provide a detailed job description (200+ words recommended)
- Ensure resume has clear section headings
- Use standard formatting (no images/tables)

---

## 🚀 Advanced Features (Future Enhancements)

### **Potential Upgrades:**
1. **OpenAI Integration** - Add GPT-4 for resume rewriting
2. **Resume Builder** - Auto-generate optimized resume
3. **LinkedIn Integration** - Analyze LinkedIn profile
4. **Database Storage** - Save analysis history
5. **User Accounts** - Track improvements over time
6. **Batch Analysis** - Compare multiple resumes
7. **Email Reports** - Send PDF reports via email
8. **Real-time Suggestions** - As-you-type feedback

---

## 📝 Sample Test Case

**Use this to test the application:**

1. **Resume**: Upload any technical resume (PDF/DOCX)

2. **Job Description**:
```
We are seeking a skilled Python Developer to join our AI team.

Requirements:
- 3+ years of Python development experience
- Strong knowledge of FastAPI, Django, or Flask
- Experience with machine learning libraries (scikit-learn, TensorFlow)
- Proficiency in SQL databases (PostgreSQL, MySQL)
- Familiarity with AWS or Azure cloud services
- Understanding of CI/CD pipelines and Docker
- Bachelor's degree in Computer Science or related field

Responsibilities:
- Develop and maintain Python-based applications
- Build REST APIs using FastAPI
- Implement machine learning models
- Collaborate with cross-functional teams
- Write clean, maintainable code
```

---

## 🎓 Learning Outcomes

This project demonstrates:

✅ **Full-Stack Development** - Backend API + Frontend UI  
✅ **AI/ML Integration** - NLP, TF-IDF, Cosine Similarity  
✅ **API Design** - RESTful endpoints, error handling  
✅ **File Processing** - PDF/DOCX parsing  
✅ **Data Visualization** - Progress bars, charts  
✅ **Real-World Application** - Solves actual hiring problems  

---

## 👨‍💻 About the Developer

**Vansh Motla**  
- Final-year B.Tech CS student at Galgotias University
- Aspiring AI Developer
- Skills: Python, SQL, Machine Learning, FastAPI
- GitHub: [github.com/VanshMotla/ai-developer-journey](https://github.com/VanshMotla/ai-developer-journey)

---

## 📞 Support

If you encounter any issues:

1. Check the **Troubleshooting** section above
2. Review terminal logs for error messages
3. Verify all dependencies are installed correctly
4. Ensure both backend (port 8000) and frontend are running

---

## 📄 License

This project is created for educational and portfolio purposes.

---

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **spaCy** - Industrial-strength NLP
- **scikit-learn** - Machine learning library
- **PyMuPDF** - PDF processing

---

**🎯 Happy Analyzing! May your resume land you the perfect job! 🚀**
