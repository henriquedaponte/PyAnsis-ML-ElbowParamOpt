echo off
set LOCALHOST=%COMPUTERNAME%
set KILL_CMD="C:\PROGRA~1\ANSYS Inc\ANSYS Student\v231\fluent/ntbin/win64/winkill.exe"

"C:\PROGRA~1\ANSYS Inc\ANSYS Student\v231\fluent\ntbin\win64\tell.exe" DESKTOP-U26BJ62 65496 CLEANUP_EXITING
if /i "%LOCALHOST%"=="DESKTOP-U26BJ62" (%KILL_CMD% 15872) 
if /i "%LOCALHOST%"=="DESKTOP-U26BJ62" (%KILL_CMD% 5868) 
if /i "%LOCALHOST%"=="DESKTOP-U26BJ62" (%KILL_CMD% 20032) 
if /i "%LOCALHOST%"=="DESKTOP-U26BJ62" (%KILL_CMD% 18928)
del "C:\Users\Ique\Documents\Internship\Femto\ElbowOpt\Code\git\cleanup-fluent-DESKTOP-U26BJ62-20032.bat"
