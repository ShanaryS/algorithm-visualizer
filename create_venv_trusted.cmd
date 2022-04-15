python -m venv venv

for /F "tokens=*" %%A in (requirements.txt) do venv\Scripts\pip.exe install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org %%A

@echo off
echo.
pause