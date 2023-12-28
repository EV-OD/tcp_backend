@echo off

:: Start Django server
start "Django Server" cmd /k "python manage.py runserver"

:: Start Flask server
start "Flask Server" cmd /k "cd python && python flask_api.py"

:: Start another Python script
start "Python Script" cmd /k "cd python && python flagged_ip_alert.py"

:: Start another Python script
start "Python Script" cmd /k "cd python && python -m http.server 8080"

:: You can add more commands as needed

:: Keep the command prompt window open
cmd /k
