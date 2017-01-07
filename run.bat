@ECHO off
IF EXIST %SYSTEMROOT%\py.exe (
    CMD /k py.exe -3.5 main.py
    EXIT
)