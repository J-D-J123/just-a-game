@echo off 
color 0a
title Just-A-Game

setlocal enabledelayedexpansion 

:menu
cls
echo ">      ____.         ________                 ____.____________  ________  
echo ">     |    |         \______ \               |    /_   \_____  \ \_____  \ 
echo ">     |    |  ______  |    |  \   ______     |    ||   |/  ____/   _(__  <
echo "> /\__|    | /_____/  |    \`   \ /_____ /\__|    ||   /       \  /       \
echo "> \________|         /_______  /         \________||___\_______ \/______  /
echo ">                            \/                                \/       \/ 

echo ">
echo "> Press(1) for Flappy Bird    Press(2) for the Unknown    Press(3) for Block Break 
echo "> (Py must be installed)       (Py must be installed)      (Py must be installed)
echo ">
echo ">Press(4) to exit
echo ">
echo ">

set /p ans=":> Enter Number: "   

if %ans%==1 goto FlappyBird
if %ans%==2 goto Unknown
if %ans%==3 goto exit

:FlappyBird
cls
echo Checking for Python installation . . . 
:: Check if Python is installed
py --version > temp.txt 2>&1
set "pythonFound=0"

:: Read the temp file to check for the word "Python"
for /f "tokens=*" %%A in (temp.txt) do (
    echo %%A | find /i "Python" >nul
    if !errorlevel! == 0 (
        set "pythonFound=1"
    )
)

:: Remove the temp file 
del temp.txt

:: proceed to start FlappyBird 
if %pythonFound%==1 (
    echo Starting FlappyBird . . .
    FB\start.py
    pause
    goto menu
) else (
    echo Python is not installed. Please install Python and try again.
)

:Unknown
cls
echo Starting Unknown . . .

:: start up the .vbs script in the back
cscript //nologo Unknown\run.vbs
cls
pause
goto menu

:exit 
cls
echo Exiting the program. 
pause
goto menu
