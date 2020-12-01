cd /D "%~dp0" 
set FLASK_APP=DTMT.py
start firefox.exe 127.0.0.1:5000
flask run
exit