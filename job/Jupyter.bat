if not "%~0"=="%~dp0.\%~nx0" (
    start /min cmd /c,"%~dp0.\%~nx0" %*
    exit
)
cd /d F:\
call C:\Users\sakur\anaconda3\Scripts\activate.bat
jupyter lab