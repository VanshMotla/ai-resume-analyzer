"""
FILE PROCESSOR - Extract text from PDF and DOCX files
"""

import pymupdf as fitz
from docx import Document
import re


class FileProcessor:
    """Handles resume file processing (PDF/DOCX)"""

    @staticmethod
    def extract_text_from_pdf(file_path):
        """Extract text from PDF file"""
        try:
            doc = pymupdf.open(file_path)

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

            text = "\n".join(
                [paragraph.text for paragraph in doc.paragraphs]
            )

            return text.strip()

        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")

    @staticmethod
    def extract_text(file_path):
        """Auto-detect file type and extract text"""

        if file_path.lower().endswith(".pdf"):
            return FileProcessor.extract_text_from_pdf(file_path)

        elif file_path.lower().endswith(".docx"):
            return FileProcessor.extract_text_from_docx(file_path)

        else:
            raise ValueError(
                "Unsupported file format. Only PDF and DOCX are supported."
            )

    @staticmethod
    def clean_text(text):
        """Clean extracted text"""

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        # Remove special characters but keep punctuation
        text = re.sub(r"[^\w\s\.\,\;\:\-\(\)\@]", "", text)

        return text.strip()

    @staticmethod
    def check_ats_compatibility(text):
        """Check ATS compatibility issues"""

        issues = []
        score = 100

        # Check for tables
        if text.count("\t") > 5:
            issues.append(
                "Contains multiple tabs - may have tables (not ATS-friendly)"
            )
            score -= 15

        # Check special characters
        special_chars = len(
            re.findall(r"[★☆●○■□▪▫◆◇]", text)
        )

        if special_chars > 3:
            issues.append(
                f"Contains {special_chars} special characters/symbols"
            )
            score -= 10

        # Check for columns
        if text.count("\n\n") > 20:
            issues.append(
                "Possible multi-column layout detected"
            )
            score -= 10

        # Check header/footer
        lines = text.split("\n")

        if len(lines) > 0:
            first_line = lines[0].lower()

            if any(word in first_line for word in ["page", "resume", "cv"]):
                issues.append(
                    "Possible header/footer detected"
                )
                score -= 5

        # Check text length
        if len(text) < 100:
            issues.append(
                "Very short text detected"
            )
            score -= 20

        # Standard sections
        section_keywords = [
            "experience",
            "education",
            "skills",
            "projects"
        ]

        found_sections = sum(
            1 for keyword in section_keywords
            if keyword in text.lower()
        )

        if found_sections < 2:
            issues.append(
                "Missing standard resume sections"
            )
            score -= 15

        recommendations = []

        if score < 70:
            recommendations.append(
                "Use a simple single-column layout"
            )
            recommendations.append(
                "Use standard bullet points"
            )
            recommendations.append(
                "Ensure text is selectable"
            )
            recommendations.append(
                "Use standard section headings"
            )

        return {
            "score": max(0, score),
            "issues": issues if issues else [
                "No major ATS issues detected"
            ],
            "recommendations": recommendations if recommendations else [
                "Your resume appears ATS-friendly"
            ]
        }