@echo off
color f0

setlocal EnableDelayedExpansion

echo [31m比较本地与服务器文件的差异，请按任意键继续!!![30m
echo [31m运行后请查看log.txt文件!!![30m

set local=%cd%
if "%local:~0,3%" == "X:\" (
    subst > %TEMP%\virtual_disk_list.txt
    set /P VDLIST=<%TEMP%\virtual_disk_list.txt
    echo !VDLIST!
    set local=!VDLIST:~8!!cd:~2!
)
echo 本地路径：[31m%local%[30m
set cloud=%local:D:\OneDrive\统计部=Z:%
echo 服务器路径：[31m%cloud%[30m
rem pause

robocopy "%local%" "%cloud%" /E /XO /COPY:DAT /DCOPY:DAT /TEE /W:3 /R:10 /XA:H /XF ~$* upload.log download.log compare.log /XD .ruff_cache .venv __pycache__ /UNILOG+:compare.log /UNICODE /L /PURGE

explorer %local%\compare.log

exit
