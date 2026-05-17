"""
AI ANALYZER - Intelligent resume analysis engine
"""
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from typing import List, Dict, Tuple
import os


class AIAnalyzer:
    """AI-powered resume analyzer"""
    
    def __init__(self):
        """Initialize the analyzer"""
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords', quiet=True)
        
        self.stop_words = set(stopwords.words('english'))
    
    def extract_keywords(self, text: str, top_n: int = 20) -> List[str]:
        """Extract important keywords using TF-IDF"""
        # Clean and tokenize
        words = word_tokenize(text.lower())
        words = [w for w in words if w.isalnum() and w not in self.stop_words and len(w) > 2]
        
        # Use TF-IDF if we have enough words
        if len(words) > 5:
            vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
            try:
                tfidf_matrix = vectorizer.fit_transform([' '.join(words)])
                feature_names = vectorizer.get_feature_names_out()
                return list(feature_names[:top_n])
            except:
                # Fallback to frequency-based
                from collections import Counter
                word_freq = Counter(words)
                return [word for word, _ in word_freq.most_common(top_n)]
        
        return list(set(words))[:top_n]
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        # Common technical skills (expandable)
        skill_patterns = [
            # Programming Languages
            r'\b(python|java|javascript|typescript|c\+\+|c#|ruby|go|rust|swift|kotlin|php|scala|r\b|matlab)\b',
            # Web Technologies
            r'\b(react|angular|vue|node\.?js|express|django|flask|fastapi|spring|asp\.net|html|css|sass|tailwind)\b',
            # Databases
            r'\b(sql|mysql|postgresql|mongodb|redis|cassandra|oracle|dynamodb|firebase)\b',
            # Cloud & DevOps
            r'\b(aws|azure|gcp|docker|kubernetes|jenkins|git|ci/cd|terraform|ansible)\b',
            # Data Science & AI
            r'\b(machine learning|ml|deep learning|nlp|tensorflow|pytorch|scikit-learn|pandas|numpy|opencv)\b',
            r'\b(data analysis|data science|analytics|tableau|power bi|excel)\b',
            # Other
            r'\b(api|rest|graphql|microservices|agile|scrum|jira|linux|unix)\b',
        ]
        
        skills = set()
        text_lower = text.lower()
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            skills.update(matches)
        
        return sorted(list(skills))
    
    def calculate_match_score(self, resume_text: str, jd_text: str) -> Dict:
        """Calculate overall match score between resume and JD"""
        # Extract keywords from both
        resume_keywords = set(self.extract_keywords(resume_text, 30))
        jd_keywords = set(self.extract_keywords(jd_text, 30))
        
        # Calculate keyword overlap
        matched_keywords = resume_keywords.intersection(jd_keywords)
        missing_keywords = jd_keywords - resume_keywords
        
        keyword_match_score = (len(matched_keywords) / len(jd_keywords) * 100) if jd_keywords else 0
        
        # Calculate semantic similarity using TF-IDF and cosine similarity
        vectorizer = TfidfVectorizer(stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            semantic_score = similarity * 100
        except:
            semantic_score = keyword_match_score
        
        # Extract skills
        resume_skills = set(self.extract_skills(resume_text))
        jd_skills = set(self.extract_skills(jd_text))
        
        matched_skills = resume_skills.intersection(jd_skills)
        missing_skills = jd_skills - resume_skills
        
        skill_match_score = (len(matched_skills) / len(jd_skills) * 100) if jd_skills else 0
        
        # Calculate weighted overall score
        overall_score = (
            keyword_match_score * 0.4 +
            semantic_score * 0.3 +
            skill_match_score * 0.3
        )
        
        return {
            "overall_score": round(overall_score, 2),
            "keyword_match_score": round(keyword_match_score, 2),
            "semantic_score": round(semantic_score, 2),
            "skill_match_score": round(skill_match_score, 2),
            "matched_keywords": list(matched_keywords)[:10],
            "missing_keywords": list(missing_keywords)[:10],
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills),
            "total_resume_keywords": len(resume_keywords),
            "total_jd_keywords": len(jd_keywords)
        }
    
    def generate_suggestions(self, resume_text: str, jd_text: str, match_data: Dict) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        # Based on overall score
        if match_data['overall_score'] < 50:
            suggestions.append("🔴 LOW MATCH: Your resume needs significant improvements to match this JD")
            suggestions.append("Consider tailoring your resume specifically for this role")
        elif match_data['overall_score'] < 70:
            suggestions.append("🟡 MODERATE MATCH: Your resume is somewhat aligned but needs optimization")
        else:
            suggestions.append("🟢 GOOD MATCH: Your resume aligns well with this job description")
        
        # Missing skills suggestions
        if match_data['missing_skills']:
            suggestions.append(f"📚 Add these skills if you have them: {', '.join(match_data['missing_skills'][:5])}")
        
        # Missing keywords suggestions
        if match_data['missing_keywords']:
            suggestions.append(f"🔑 Include these keywords naturally: {', '.join(match_data['missing_keywords'][:5])}")
        
        # Check resume length
        word_count = len(resume_text.split())
        if word_count < 200:
            suggestions.append("📄 Your resume seems too short - add more details about your experience")
        elif word_count > 800:
            suggestions.append("📄 Your resume might be too long - keep it concise (aim for 400-600 words)")
        
        # Check for numbers/metrics
        numbers = re.findall(r'\d+', resume_text)
        if len(numbers) < 3:
            suggestions.append("📊 Add quantifiable achievements (e.g., 'Increased efficiency by 30%')")
        
        # Check for action verbs
        action_verbs = ['developed', 'implemented', 'managed', 'led', 'created', 'designed', 'improved']
        verb_count = sum(1 for verb in action_verbs if verb in resume_text.lower())
        if verb_count < 3:
            suggestions.append("💪 Use more action verbs (developed, implemented, managed, led, etc.)")
        
        # Skill gap analysis
        if match_data['skill_match_score'] < 40:
            suggestions.append("⚠️ SKILL GAP: Consider upskilling in the missing technical areas")
        
        return suggestions
    
    def analyze_resume_structure(self, text: str) -> Dict:
        """Analyze resume structure and sections"""
        sections = {
            'experience': False,
            'education': False,
            'skills': False,
            'projects': False,
            'summary': False
        }
        
        text_lower = text.lower()
        
        # Check for common section headers
        if any(word in text_lower for word in ['experience', 'work history', 'employment']):
            sections['experience'] = True
        
        if any(word in text_lower for word in ['education', 'academic', 'degree']):
            sections['education'] = True
        
        if any(word in text_lower for word in ['skills', 'technical skills', 'competencies']):
            sections['skills'] = True
        
        if any(word in text_lower for word in ['projects', 'portfolio']):
            sections['projects'] = True
        
        if any(word in text_lower for word in ['summary', 'objective', 'profile']):
            sections['summary'] = True
        
        # Calculate completeness
        completeness_score = (sum(sections.values()) / len(sections)) * 100
        
        missing_sections = [section for section, present in sections.items() if not present]
        
        return {
            "sections_found": sections,
            "completeness_score": round(completeness_score, 2),
            "missing_sections": missing_sections
        }
    
    def get_strength_weakness_analysis(self, match_data: Dict, structure_data: Dict) -> Dict:
        """Analyze strengths and weaknesses"""
        strengths = []
        weaknesses = []
        
        # Strengths
        if match_data['overall_score'] >= 70:
            strengths.append("Strong overall match with job requirements")
        
        if match_data['skill_match_score'] >= 60:
            strengths.append("Good technical skill alignment")
        
        if len(match_data['matched_skills']) >= 3:
            strengths.append(f"Multiple relevant skills: {', '.join(match_data['matched_skills'][:3])}")
        
        if structure_data['completeness_score'] >= 80:
            strengths.append("Well-structured resume with all key sections")
        
        # Weaknesses
        if match_data['overall_score'] < 50:
            weaknesses.append("Low overall match - needs significant tailoring")
        
        if match_data['skill_match_score'] < 40:
            weaknesses.append("Significant skill gap with job requirements")
        
        if len(match_data['missing_skills']) > 5:
            weaknesses.append(f"Missing key skills: {', '.join(match_data['missing_skills'][:3])}")
        
        if structure_data['missing_sections']:
            weaknesses.append(f"Missing sections: {', '.join(structure_data['missing_sections'])}")
        
        # Default messages if empty
        if not strengths:
            strengths.append("Resume uploaded successfully - ready for optimization")
        
        if not weaknesses:
            weaknesses.append("No major weaknesses detected")
        
        return {
            "strengths": strengths,
            "weaknesses": weaknesses
        }
