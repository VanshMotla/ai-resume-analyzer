"""
FASTAPI BACKEND - Resume Analyzer API Server
Run with: uvicorn app:app --reload --port 8000
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import shutil
from datetime import datetime
from file_processor import FileProcessor
from ai_analyzer import AIAnalyzer

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Analyzer API",
    description="Intelligent resume analysis with AI-powered insights",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
file_processor = FileProcessor()
ai_analyzer = AIAnalyzer()

# Upload directory
UPLOAD_DIR = "../uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "AI Resume Analyzer API is running",
        "version": "1.0.0",
        "endpoints": {
            "analyze": "/api/analyze",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """
    Main endpoint: Analyze resume against job description
    
    Args:
        resume: PDF or DOCX file
        job_description: Job description text
    
    Returns:
        Comprehensive analysis report
    """
    try:
        # Validate file type
        if not resume.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(
                status_code=400,
                detail="Invalid file format. Only PDF and DOCX are supported."
            )
        
        # Validate job description
        if not job_description or len(job_description.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Job description is too short. Please provide a detailed JD (minimum 50 characters)."
            )
        
        # Save uploaded file temporarily
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(resume.filename)[1]
        temp_filename = f"resume_{timestamp}{file_extension}"
        temp_filepath = os.path.join(UPLOAD_DIR, temp_filename)
        
        with open(temp_filepath, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        
        # Extract text from resume
        try:
            resume_text = file_processor.extract_text(temp_filepath)
            resume_text = file_processor.clean_text(resume_text)
        except Exception as e:
            # Clean up file
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            raise HTTPException(
                status_code=500,
                detail=f"Error processing resume file: {str(e)}"
            )
        
        # Validate extracted text
        if len(resume_text) < 100:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            raise HTTPException(
                status_code=400,
                detail="Could not extract sufficient text from resume. The file may be an image or corrupted."
            )
        
        # Clean job description
        jd_text = file_processor.clean_text(job_description)
        
        # Perform AI analysis
        try:
            # 1. Calculate match scores
            match_analysis = ai_analyzer.calculate_match_score(resume_text, jd_text)
            
            # 2. Check ATS compatibility
            ats_analysis = file_processor.check_ats_compatibility(resume_text)
            
            # 3. Analyze resume structure
            structure_analysis = ai_analyzer.analyze_resume_structure(resume_text)
            
            # 4. Generate suggestions
            suggestions = ai_analyzer.generate_suggestions(resume_text, jd_text, match_analysis)
            
            # 5. Get strengths and weaknesses
            strength_weakness = ai_analyzer.get_strength_weakness_analysis(
                match_analysis, structure_analysis
            )
            
            # Compile comprehensive report
            analysis_report = {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "resume_info": {
                    "filename": resume.filename,
                    "word_count": len(resume_text.split()),
                    "character_count": len(resume_text)
                },
                "scores": {
                    "overall_match": match_analysis['overall_score'],
                    "keyword_match": match_analysis['keyword_match_score'],
                    "semantic_similarity": match_analysis['semantic_score'],
                    "skill_match": match_analysis['skill_match_score'],
                    "ats_compatibility": ats_analysis['score'],
                    "structure_completeness": structure_analysis['completeness_score']
                },
                "keyword_analysis": {
                    "matched_keywords": match_analysis['matched_keywords'],
                    "missing_keywords": match_analysis['missing_keywords'],
                    "total_resume_keywords": match_analysis['total_resume_keywords'],
                    "total_jd_keywords": match_analysis['total_jd_keywords']
                },
                "skill_analysis": {
                    "matched_skills": match_analysis['matched_skills'],
                    "missing_skills": match_analysis['missing_skills'],
                    "skill_gap_severity": "High" if match_analysis['skill_match_score'] < 40 else "Medium" if match_analysis['skill_match_score'] < 70 else "Low"
                },
                "ats_compatibility": {
                    "score": ats_analysis['score'],
                    "issues": ats_analysis['issues'],
                    "recommendations": ats_analysis['recommendations']
                },
                "structure_analysis": {
                    "sections_found": structure_analysis['sections_found'],
                    "completeness_score": structure_analysis['completeness_score'],
                    "missing_sections": structure_analysis['missing_sections']
                },
                "insights": {
                    "strengths": strength_weakness['strengths'],
                    "weaknesses": strength_weakness['weaknesses'],
                    "suggestions": suggestions
                },
                "match_category": (
                    "Excellent Match" if match_analysis['overall_score'] >= 80 else
                    "Good Match" if match_analysis['overall_score'] >= 70 else
                    "Moderate Match" if match_analysis['overall_score'] >= 50 else
                    "Needs Improvement"
                )
            }
            
            # Clean up temporary file
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            
            return JSONResponse(content=analysis_report)
        
        except Exception as e:
            # Clean up file on analysis error
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)
            raise HTTPException(
                status_code=500,
                detail=f"Error during analysis: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


@app.get("/api/test")
async def test_endpoint():
    """Test endpoint to verify API is working"""
    return {
        "message": "API is working correctly",
        "ai_analyzer": "initialized",
        "file_processor": "initialized"
    }


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI Resume Analyzer API Server...")
    print("📡 Server will run on: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
