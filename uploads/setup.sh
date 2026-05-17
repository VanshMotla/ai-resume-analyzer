#!/bin/bash

echo "=================================================="
echo "🎯 AI Resume Analyzer - Quick Setup Script"
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Navigate to backend directory
echo "📦 Installing backend dependencies..."
cd backend

# Install requirements
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Backend dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Download NLTK data
echo ""
echo "📥 Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"

if [ $? -eq 0 ]; then
    echo "✅ NLTK data downloaded successfully"
else
    echo "❌ Failed to download NLTK data"
    exit 1
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "To start the application:"
echo ""
echo "1️⃣  Start Backend Server:"
echo "   cd backend"
echo "   python3 app.py"
echo ""
echo "2️⃣  Open Frontend:"
echo "   cd frontend"
echo "   python3 -m http.server 3000"
echo ""
echo "3️⃣  Open browser and go to:"
echo "   http://localhost:3000"
echo ""
echo "=================================================="
