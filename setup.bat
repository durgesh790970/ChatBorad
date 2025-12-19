@echo off
REM Quick Start Script for ChatBoard (Windows)

echo.
echo ==========================================
echo   ChatBoard - Chat Application Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Run migrations
echo Running database migrations...
python manage.py migrate
echo.

REM Create superuser
echo Create a superuser account (admin):
python manage.py createsuperuser
echo.

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
echo.

REM Print success message
echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Access the application at:
echo   http://localhost:8000
echo.
echo Admin panel:
echo   http://localhost:8000/admin
echo.
echo For WebSocket support, install and run Redis:
echo   https://github.com/microsoftarchive/redis/releases
echo.
echo Happy Chatting! 💬
echo.
pause
