@echo off
REM Download and install wkhtmltopdf
powershell Invoke-WebRequest -Uri "https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.msvc2015-win64.exe" -OutFile "wkhtmltopdf_installer.exe"
wkhtmltopdf_installer.exe /S
del wkhtmltopdf_installer.exe

echo Installation completed!
pause

