@echo off
if exist stop_manage.bat goto nofile
goto start

:nofile
stop_manage.bat
echo "kill web"

:start
start start_hidden.vbs
echo "open web"
pause