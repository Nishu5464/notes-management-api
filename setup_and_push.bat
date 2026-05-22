@echo off
echo ===================================================
echo   Notes REST API Upgrader - Setup & Push Tool
echo ===================================================
echo.

echo [1/4] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Python/pip installation failed.
    echo Please ensure Python is installed and added to your System PATH variables.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/4] Running Django Database Migrations...
python manage.py makemigrations
python manage.py migrate
if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] Django migrations failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [3/4] Staging and Committing files to Git...
git add .
git commit -m "Upgrade Notes REST API: Add Token Auth, MySQL toggle, and Redis Caching"
if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Git commit failed. Make sure Git is installed and configured.
)

echo.
echo [4/4] Pushing changes to GitHub...
git push
if %ERRORLEVEL% neq 0 (
    echo.
    echo [WARNING] Git push failed. You may need to verify your GitHub auth or remote URL.
)

echo.
echo ===================================================
echo   Setup & Push complete!
echo ===================================================
pause
