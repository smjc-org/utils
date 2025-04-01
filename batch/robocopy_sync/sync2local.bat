@echo off
color f0

setlocal EnableDelayedExpansion

echo [31m同步至本地，默认不删除本地多余的文件，按任意键继续，按CTRL+C键中止[30m
echo.

set local=%cd%
if "%local:~0,3%" == "X:\" (
    subst > %TEMP%\virtual_disk_list.txt
    set /P VDLIST=<%TEMP%\virtual_disk_list.txt
    echo !VDLIST!
    set local=!VDLIST:~8!!cd:~2!
)
set cloud=%local:D:\OneDrive\统计部=Z:%
echo 本地路径：[31m%local%[30m
echo 服务器路径：[31m%cloud%[30m
echo.
echo.

set /p input=是否删除本地磁盘中多余的文件？（[31mY/N[30m）
if "%input%"=="Y" (
goto delete_rep
)else if "%input%"=="y" (
goto delete_rep
)else if "%input%"=="N" (
goto not_delete_rep
)else if "%input%"=="n" (
goto not_delete_rep
)else (
echo 输入有误，将保留服务器中多余的文件！
goto not_delete_rep
)

:delete_rep
robocopy "%cloud%" "%local%" /E /XO /COPY:DAT /DCOPY:DAT /W:3 /R:10 /TEE /XA:H /XF ~$* upload.log download.log compare.log /XD .ruff_cache .venv __pycache__ /UNILOG+:download.log /UNICODE /PURGE
exit

:not_delete_rep
robocopy "%cloud%" "%local%" /E /XO /COPY:DAT /DCOPY:DAT /W:3 /R:10 /TEE /XA:H /XF ~$* upload.log download.log compare.log /XD .ruff_cache .venv __pycache__ /UNILOG+:download.log /UNICODE
exit
