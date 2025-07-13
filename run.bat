@echo off
:: Get the current folder where this script is
set "target_dir=%~dp0"

:: Create a temporary batch file to be executed as Admin
set "temp_script=%temp%\\run_main_temp.bat"
echo cd /d "%target_dir%" > "%temp_script%"
echo echo Running Flask App in Admin Mode... >> "%temp_script%"
echo python main.py >> "%temp_script%"
echo pause >> "%temp_script%"

:: Run the temporary script in elevated CMD
powershell -Command "Start-Process cmd -ArgumentList '/k \"%temp_script%\"' -Verb RunAs"
