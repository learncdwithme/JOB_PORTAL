@echo off
SETLOCAL ENABLEDELAYEDEXPANSION

:: Base directory
set BASEDIR=jobs

:: Create base directory
if not exist %BASEDIR% (
    mkdir %BASEDIR%
)
mkdir "assets"

:: Define job roles (these will become category folders)
set ROLES="Java Developer","PHP Developer","Android Developer","Content Writer","Business Development Manager","Software Engineer","Graphic Designer","Business Analyst","Data Engineer","Project Manager","Sales Manager","Sales Executive","HR Manager","Data Scientist","Civil Engineer","Senior Consultant"

:: Loop through roles and create folder structure
for %%A in (%ROLES%) do (
    set role=%%~A
    set role=!role:"=!
    set category=!role: =-!
    set category=!category:--=-!

 :: Call PowerShell to convert to lowercase and assign to category
    for /f "usebackq delims=" %%B in (`powershell -NoProfile -Command "[string]'!category!'.ToLower()"`) do (
        set "category=%%B"
    )

    echo Creating category: !category!
    mkdir "%BASEDIR%\!category!" 2>nul
)

:: Create data folder and jobs.json if not exists
if not exist data (
    mkdir data
)

if not exist data\jobs.json (
    echo [] > data\jobs.json
    echo Created: data\jobs.json
)

echo.
echo ✅ Initialization complete.
pause
