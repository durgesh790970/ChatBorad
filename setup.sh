#!/bin/bash
# Quick Start Script for ChatBoard

echo "=========================================="
echo "  ChatBoard - Chat Application Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1)
echo "Found: $python_version"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser
echo ""
echo "Create a superuser account (admin):"
python manage.py createsuperuser

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Print success message
echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Access the application at:"
echo "  http://localhost:8000"
echo ""
echo "Admin panel:"
echo "  http://localhost:8000/admin"
echo ""
echo "For WebSocket support, install and run Redis:"
echo "  redis-server"
echo ""
echo "Happy Chatting! 💬"
