@echo off
echo [INFO] Створення віртуального середовища...
python -m venv venv

echo [INFO] Активація середовища...
call venv\Scripts\activate

echo [INFO] Встановлення залежностей...
pip install --upgrade pip
pip install -r requirements.txt

echo [INFO] Готово!
pause