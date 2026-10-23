@echo off
setlocal
set "APP=%~dp0setup-note.html"
if not exist "%APP%" goto missing
if exist "%ProgramFiles%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles%\Google\Chrome\Application\chrome.exe" --new-window "%APP%"
  exit /b 0
)
if exist "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" (
  start "" "%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe" --new-window "%APP%"
  exit /b 0
)
if exist "%LocalAppData%\Google\Chrome\Application\chrome.exe" (
  start "" "%LocalAppData%\Google\Chrome\Application\chrome.exe" --new-window "%APP%"
  exit /b 0
)
echo Chrome was not found in standard locations.
echo Opening Setup Note in your default browser.
start "" "%APP%"
exit /b 0
:missing
echo setup-note.html is missing.
echo Extract ALL files from the ZIP before running this launcher.
pause
exit /b 1
