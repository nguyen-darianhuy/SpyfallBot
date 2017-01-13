@ECHO off
IF EXIST %SYSTEMROOT%\py.exe (
    CMD /k py.exe -3 main.py
    EXIT
)