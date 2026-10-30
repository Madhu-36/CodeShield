#!/bin/bash
echo "🚀 Setting up CodeShield Project for Linux/Mac..."

# Create Virtual Environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Virtual Environment..."
    python3 -m venv venv
fi

# Activate and Install
echo "Activating Virtual Environment and installing dependencies..."
source venv/bin/activate
pip install -e .

# Setup .env
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "⚠️ Created .env file. Please open it and add your OPENAI_API_KEY."
else
    echo ".env file already exists."
fi

echo "✅ Setup Complete!"
echo "To start using CodeShield, run:"
echo "source venv/bin/activate"
echo "python cli.py --help"
