@echo off
color f0

setlocal EnableDelayedExpansion

set local=%cd%
if "%local:~0,3%" == "X:\" (
    subst > %TEMP%\virtual_disk_list.txt
    set /P VDLIST=<%TEMP%\virtual_disk_list.txt
    echo !VDLIST!
    set local=!VDLIST:~8!!cd:~2!
)

set cloud="%local:D:\OneDrive\统计部=Z:%"
explorer "%cloud%"
