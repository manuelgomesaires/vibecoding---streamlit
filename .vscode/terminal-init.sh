#!/bin/bash
# VSCode Terminal Initialization Script for macOS/Linux
# This script runs automatically when you open a new terminal in VSCode

# Source the user's shell configuration
if [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc"
elif [ -f "$HOME/.bash_profile" ]; then
    source "$HOME/.bash_profile"
elif [ -f "$HOME/.zshrc" ]; then
    source "$HOME/.zshrc"
fi

# Define helpful aliases for Python virtual environment
# setup-venv calls the setup.sh script to keep logic in one place
alias setup-venv='bash setup.sh && source .venv/bin/activate 2>/dev/null'
alias activate='source .venv/bin/activate && pip install -r requirements.txt 2>/dev/null'
alias install-req='pip install -r requirements.txt'

# Check if virtual environment exists
if [ -d ".venv" ]; then
    # Activate it automatically
    source .venv/bin/activate
    echo "🐍 Virtual environment activated!"
    echo "   Ready to code! Run: python main.py"
else
    # Friendly message for first-time users
    echo "💡 Welcome! No virtual environment found yet."
    echo "   Run this command to set up everything: setup-venv"
fi

echo ""
