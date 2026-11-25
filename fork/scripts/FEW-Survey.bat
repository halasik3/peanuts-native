@echo off
rem FORK: Fire Emblem Warriors survey kit. Double-click it. It reads the game files and prod.keys in one folder (C:\FEW by default) and writes
rem FEW-results.zip there: the survey, the provisional profile and the logs, no game data. fork\scripts\few_survey.py does the work.
setlocal
set "KIT=%~dp0"
if exist "%KIT%tools\nximport_cli.exe" set "NX_IMPORTER=%KIT%tools\nximport_cli.exe"
echo.
echo  Fire Emblem Warriors survey
echo  ---------------------------
echo  Put the base game, the 1.5.0 update and prod.keys in one folder.
echo.
set "GAMEDIR=C:\FEW"
set /p "GAMEDIR=Folder with the files [C:\FEW]: "
if not exist "%GAMEDIR%\prod.keys" (
  echo.
  echo  No prod.keys in "%GAMEDIR%". Copy it there and run this again.
  pause
  exit /b 1
)
echo.
echo  The first run sets up its tools (about 400 MB). If it asks for a folder, press Enter.
echo.
call "%KIT%scripts\bananative.bat" python "%KIT%fork\scripts\few_survey.py" "%GAMEDIR%"
set rc=%ERRORLEVEL%
echo.
if %rc%==0 (echo  Finished. Send "%GAMEDIR%\FEW-results.zip".) else (echo  It stopped with an error. Send "%GAMEDIR%\FEW-results.zip" anyway: the logs say why.)
pause
exit /b %rc%
