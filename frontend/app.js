/**
 * RESUME ANALYZER - FRONTEND JAVASCRIPT
 * Handles form submission, API calls, and result visualization
 */

// Configuration
const API_BASE_URL = 'http://localhost:8000';
const MIN_JD_LENGTH = 50;

// DOM Elements
let resumeFile = null;
let analysisData = null;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeFileUpload();
    initializeForm();
    initializeCharCounter();
});

/**
 * Initialize file upload functionality
 */
function initializeFileUpload() {
    const fileInput = document.getElementById('resumeFile');
    const fileName = document.querySelector('.file-name');
    const fileDisplay = document.querySelector('.file-upload-display');
    const browseBtn = document.querySelector('.browse-btn');

    // Handle file selection
    fileInput.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
            const file = this.files[0];
            resumeFile = file;
            
            // Validate file type
            const validTypes = ['.pdf', '.docx'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            if (!validTypes.includes(fileExtension)) {
                showError('Invalid file type. Please upload a PDF or DOCX file.');
                this.value = '';
                fileName.textContent = 'No file selected';
                return;
            }
            
            // Validate file size (max 5MB)
            const maxSize = 5 * 1024 * 1024;
            if (file.size > maxSize) {
                showError('File is too large. Maximum size is 5MB.');
                this.value = '';
                fileName.textContent = 'No file selected';
                return;
            }
            
            // Update display
            fileName.textContent = file.name;
            fileName.style.color = 'var(--success-color)';
            fileDisplay.style.borderColor = 'var(--success-color)';
            fileDisplay.style.background = 'rgba(16, 185, 129, 0.05)';
        }
    });

    // Trigger file input on button click
    browseBtn.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        fileInput.click();
    });

    // Trigger file input on display click
    fileDisplay.addEventListener('click', function() {
        fileInput.click();
    });
}

/**
 * Initialize form submission
 */
function initializeForm() {
    const form = document.getElementById('analyzeForm');
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Validate inputs
        const jobDescription = document.getElementById('jobDescription').value.trim();
        
        if (!resumeFile) {
            showError('Please upload your resume (PDF or DOCX)');
            return;
        }
        
        if (jobDescription.length < MIN_JD_LENGTH) {
            showError(`Job description is too short. Please provide at least ${MIN_JD_LENGTH} characters.`);
            return;
        }
        
        // Start analysis
        await analyzeResume(resumeFile, jobDescription);
    });
}

/**
 * Initialize character counter for job description
 */
function initializeCharCounter() {
    const textarea = document.getElementById('jobDescription');
    const charCount = document.getElementById('charCount');
    
    textarea.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count;
        
        if (count >= MIN_JD_LENGTH) {
            charCount.style.color = 'var(--success-color)';
        } else {
            charCount.style.color = 'var(--danger-color)';
        }
    });
}

/**
 * Analyze resume by calling the API
 */
async function analyzeResume(file, jobDescription) {
    try {
        // Show loading state
        showSection('loadingSection');
        hideSection('uploadSection');
        hideSection('resultsSection');
        hideSection('errorSection');
        
        // Prepare form data
        const formData = new FormData();
        formData.append('resume', file);
        formData.append('job_description', jobDescription);
        
        // Call API
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Analysis failed');
        }
        
        const data = await response.json();
        analysisData = data;
        
        // Display results
        displayResults(data);
        
    } catch (error) {
        console.error('Analysis error:', error);
        showError(error.message || 'Failed to analyze resume. Please try again.');
    }
}

/**
 * Display analysis results
 */
function displayResults(data) {
    // Hide loading, show results
    hideSection('loadingSection');
    showSection('resultsSection');
    
    // Animate sections with delay
    setTimeout(() => {
        // Overall score
        updateOverallScore(data.scores.overall_match);
        updateMatchBadge(data.match_category);
        
        // Detailed scores
        updateDetailedScores(data.scores);
        
        // Skills analysis
        updateSkillsAnalysis(data.skill_analysis);
        
        // Keywords analysis
        updateKeywordsAnalysis(data.keyword_analysis);
        
        // Insights
        updateInsights(data.insights);
        
        // ATS compatibility
        updateATSReport(data.ats_compatibility);
        
    }, 100);
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Update overall score circle
 */
function updateOverallScore(score) {
    const scoreNumber = document.getElementById('overallScoreNumber');
    const scoreFill = document.getElementById('scoreFillCircle');
    
    // Animate number
    animateValue(scoreNumber, 0, Math.round(score), 1500);
    
    // Animate circle
    const circumference = 2 * Math.PI * 90;
    const offset = circumference - (score / 100) * circumference;
    scoreFill.style.strokeDashoffset = offset;
    
    // Set color based on score
    if (score >= 80) {
        scoreFill.style.stroke = 'var(--success-color)';
    } else if (score >= 50) {
        scoreFill.style.stroke = '#fbbf24'; // yellow
    } else {
        scoreFill.style.stroke = 'var(--danger-color)';
    }
}

/**
 * Update match badge
 */
function updateMatchBadge(category) {
    const badge = document.getElementById('matchBadge');
    badge.textContent = category;
    
    // Set background color
    if (category.includes('Excellent')) {
        badge.style.background = 'rgba(16, 185, 129, 0.3)';
    } else if (category.includes('Good')) {
        badge.style.background = 'rgba(251, 191, 36, 0.3)';
    } else {
        badge.style.background = 'rgba(239, 68, 68, 0.3)';
    }
}

/**
 * Update detailed scores
 */
function updateDetailedScores(scores) {
    updateProgressBar('keywordProgress', 'keywordScore', scores.keyword_match);
    updateProgressBar('semanticProgress', 'semanticScore', scores.semantic_similarity);
    updateProgressBar('skillProgress', 'skillScore', scores.skill_match);
    updateProgressBar('atsProgress', 'atsScore', scores.ats_compatibility);
}

/**
 * Update a single progress bar
 */
function updateProgressBar(progressId, scoreId, value) {
    const progress = document.getElementById(progressId);
    const scoreElement = document.getElementById(scoreId);
    
    setTimeout(() => {
        progress.style.width = value + '%';
        animateValue(scoreElement, 0, Math.round(value), 1000, '%');
    }, 100);
}

/**
 * Update skills analysis
 */
function updateSkillsAnalysis(skillData) {
    const matchedSkills = document.getElementById('matchedSkills');
    const missingSkills = document.getElementById('missingSkills');
    
    // Matched skills
    if (skillData.matched_skills && skillData.matched_skills.length > 0) {
        matchedSkills.innerHTML = skillData.matched_skills
            .map(skill => `<span class="skill-tag matched">${skill}</span>`)
            .join('');
    } else {
        matchedSkills.innerHTML = '<span class="skill-tag">No matched skills found</span>';
    }
    
    // Missing skills
    if (skillData.missing_skills && skillData.missing_skills.length > 0) {
        missingSkills.innerHTML = skillData.missing_skills
            .map(skill => `<span class="skill-tag missing">${skill}</span>`)
            .join('');
    } else {
        missingSkills.innerHTML = '<span class="skill-tag">No missing skills</span>';
    }
}

/**
 * Update keywords analysis
 */
function updateKeywordsAnalysis(keywordData) {
    const matchedKeywords = document.getElementById('matchedKeywords');
    const missingKeywords = document.getElementById('missingKeywords');
    
    // Matched keywords
    if (keywordData.matched_keywords && keywordData.matched_keywords.length > 0) {
        matchedKeywords.textContent = keywordData.matched_keywords.join(', ');
    } else {
        matchedKeywords.textContent = 'No matched keywords found';
    }
    
    // Missing keywords
    if (keywordData.missing_keywords && keywordData.missing_keywords.length > 0) {
        missingKeywords.textContent = keywordData.missing_keywords.join(', ');
    } else {
        missingKeywords.textContent = 'No missing keywords';
    }
}

/**
 * Update insights (strengths, weaknesses, suggestions)
 */
function updateInsights(insights) {
    // Strengths
    const strengthsList = document.getElementById('strengthsList');
    strengthsList.innerHTML = insights.strengths
        .map(item => `<li>${item}</li>`)
        .join('');
    
    // Weaknesses
    const weaknessesList = document.getElementById('weaknessesList');
    weaknessesList.innerHTML = insights.weaknesses
        .map(item => `<li>${item}</li>`)
        .join('');
    
    // Suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = insights.suggestions
        .map(item => `<div class="suggestion-item">${item}</div>`)
        .join('');
}

/**
 * Update ATS report
 */
function updateATSReport(atsData) {
    const atsScore = document.getElementById('atsScoreValue');
    const atsIssues = document.getElementById('atsIssues');
    const atsRecommendations = document.getElementById('atsRecommendations');
    
    // Score
    animateValue(atsScore, 0, atsData.score, 1500);
    
    // Issues
    atsIssues.innerHTML = atsData.issues
        .map(issue => `<li>${issue}</li>`)
        .join('');
    
    // Recommendations
    atsRecommendations.innerHTML = atsData.recommendations
        .map(rec => `<li>${rec}</li>`)
        .join('');
    
    // Color badge based on score
    const badge = document.getElementById('atsScoreBadge');
    if (atsData.score >= 80) {
        badge.style.background = 'linear-gradient(135deg, var(--success-color), #059669)';
    } else if (atsData.score >= 60) {
        badge.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
    } else {
        badge.style.background = 'linear-gradient(135deg, var(--danger-color), #dc2626)';
    }
}

/**
 * Animate number value
 */
function animateValue(element, start, end, duration, suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if ((increment > 0 && current >= end) || (increment < 0 && current <= end)) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current) + suffix;
    }, 16);
}

/**
 * Show error message
 */
function showError(message) {
    hideSection('uploadSection');
    hideSection('loadingSection');
    hideSection('resultsSection');
    showSection('errorSection');
    
    document.getElementById('errorMessage').textContent = message;
    document.getElementById('errorSection').scrollIntoView({ behavior: 'smooth' });
}

/**
 * Show section
 */
function showSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.remove('hidden');
    }
}

/**
 * Hide section
 */
function hideSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('hidden');
    }
}

/**
 * Test API connection
 */
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            console.log('✅ API connection successful');
            return true;
        }
    } catch (error) {
        console.error('❌ API connection failed:', error);
        showError('Cannot connect to the API server. Please ensure the backend is running on http://localhost:8000');
        return false;
    }
}

// Test API connection on load
window.addEventListener('load', testAPIConnection);
