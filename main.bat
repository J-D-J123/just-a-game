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
echo "> Press(1) for Flappy Bird    Press(2) for BlockBreak     Press(3) to exit
echo "> (Py must be installed)       (Py must be installed)      
echo ">
echo ">
echo ">

set /p ans=":> Enter Number: "   

if "%ans%"=="1" goto FlappyBird
if "%ans%"=="2" goto BlockBreak
if "%ans%"=="3" goto exit
goto menu

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
if "!pythonFound!"=="1" (
    echo "> What type of song do you want to use?
    echo "> This will play the song in the background. 
    echo ">
    echo "> HipHop(1)
    echo "> Jazz(2)
    echo "> EDM(3)

    set /p songANS=":> Enter a Number: "

    if "%songANS%"=="1" goto FB_HipHop
    if "%songANS%"=="2" goto FB_Jazz
    if "%songANS%"=="3" goto FB_EDM

) else (
    echo Python is not installed. Please install Python and try again.
    pause 
    goto menu
)

:FB_HipHop
cls
echo Starting HipHop version of Flappy Bird...
@REM FB\startHipHop.py
pause
goto menu

:FB_Jazz
cls
echo Starting Jazz version of Flappy Bird...
FB\startJazz.py
pause
goto menu

:FB_EDM
cls
echo Starting EDM version of Flappy Bird...
@REM FB\startEDM.py
there is no current version of a EDM Flappy Bird come back later!
pause
goto menu

:BlockBreak
cls
echo Starting BlockBreak . . .
:: start up the .vbs script in the back
@REM cscript //nologo Unknown\run.vbs
echo no BlockBreak version is made 
echo it will come out soon . . .
pause
goto menu

:exit 
cls
echo Exiting the program. 
pause
exit