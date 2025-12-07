#!/bin/bash

# Start the FastAPI backend server
echo "🚀 Starting Drug Repurposing Platform Backend..."
echo "📍 Server will run on http://localhost:8000"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Run the server
echo "✅ Starting FastAPI server..."
python main.py

