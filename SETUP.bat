@echo off
python --version | find "Python 3"
if %errorlevel% == 0 (
   echo found right python version
   GOTO INSTALLS
) ELSE (
   echo wrong python version - install Python 3.6 or greater
   GOTO :EOF
)
:INSTALLS
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
pause