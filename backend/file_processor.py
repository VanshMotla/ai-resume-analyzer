"""
FILE PROCESSOR - Extract text from PDF and DOCX files
"""
import fitz  # PyMuPDF
from docx import Document
import re


class FileProcessor:
    """Handles resume file processing (PDF/DOCX)"""
    
    @staticmethod
    def extract_text_from_pdf(file_path):
        """Extract text from PDF file"""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def extract_text_from_docx(file_path):
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    @staticmethod
    def extract_text(file_path):
        """Auto-detect file type and extract text"""
        if file_path.lower().endswith('.pdf'):
            return FileProcessor.extract_text_from_pdf(file_path)
        elif file_path.lower().endswith('.docx'):
            return FileProcessor.extract_text_from_docx(file_path)
        else:
            raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
    
    @staticmethod
    def clean_text(text):
        """Clean extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\-\(\)\@]', '', text)
        return text.strip()
    
    @staticmethod
    def check_ats_compatibility(text):
        """Check ATS compatibility issues"""
        issues = []
        score = 100
        
        # Check for tables (common ATS issue)
        if text.count('\t') > 5:
            issues.append("Contains multiple tabs - may have tables (not ATS-friendly)")
            score -= 15
        
        # Check for special characters
        special_chars = len(re.findall(r'[★☆●○■□▪▫◆◇]', text))
        if special_chars > 3:
            issues.append(f"Contains {special_chars} special characters/symbols - avoid fancy bullets")
            score -= 10
        
        # Check for columns (detected by multiple consecutive line breaks)
        if text.count('\n\n') > 20:
            issues.append("Possible multi-column layout detected - use single column for ATS")
            score -= 10
        
        # Check for headers/footers (common issue)
        lines = text.split('\n')
        if len(lines) > 0:
            first_line = lines[0].lower()
            if any(word in first_line for word in ['page', 'resume', 'cv']):
                issues.append("Possible header/footer detected - remove them for ATS")
                score -= 5
        
        # Check for images (can't detect directly but check for very short text)
        if len(text) < 100:
            issues.append("Very short text - resume may contain images instead of text")
            score -= 20
        
        # Check for standard sections
        section_keywords = ['experience', 'education', 'skills', 'projects']
        found_sections = sum(1 for keyword in section_keywords if keyword in text.lower())
        
        if found_sections < 2:
            issues.append("Missing standard sections (Experience, Education, Skills)")
            score -= 15
        
        recommendations = []
        if score < 70:
            recommendations.append("Use a simple, single-column layout")
            recommendations.append("Replace special characters with standard bullets (•)")
            recommendations.append("Ensure all text is selectable (no images of text)")
            recommendations.append("Use standard section headings")
        
        return {
            "score": max(0, score),
            "issues": issues if issues else ["No major ATS issues detected"],
            "recommendations": recommendations if recommendations else ["Your resume appears ATS-friendly"]
        }
