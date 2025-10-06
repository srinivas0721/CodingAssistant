@echo off
echo Starting CP Assistant Backend...

if not exist .env (
    echo Error: .env file not found!
    echo Please copy .env.example to .env and add your GOOGLE_API_KEY
    exit /b 1
)

for /f "delims=" %%i in ('type .env ^| findstr /b "GOOGLE_API_KEY="') do set %%i

if "%GOOGLE_API_KEY%"=="" (
    echo Error: GOOGLE_API_KEY not set in .env file
    exit /b 1
)

cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
