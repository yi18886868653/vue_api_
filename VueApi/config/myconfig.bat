@echo off&setlocal ENABLEDELAYEDEXPANSION
call :���� config.ini
call :��ȡ DRIVER driver
call :�޸� DRIVER driver %1
call :��� >d:\vue_api\VueApi\config\config.ini
goto :eof
 
 
:���� [����#1=ini�ļ�·��]
set "op="
for /f " usebackq tokens=1* delims==" %%a in ("%~1") do (
    if "%%b"=="" (
        set "op=%%a"
    ) else (
        set "##!op!#%%a=%%b"
    )
)
goto :eof

 
:��ȡ [����#1=Option] [����#2=Key]
echo,Option=%~1,Key=%~2,Value=!##[%~1]#%~2!
goto :eof
 

:�޸� [����#1=Option] [����#2=Key] [����#3=value��û�в���3��ɾ����������]
set "##[%~1]#%~2 = %~3"
goto :eof
 


:��� [>��ini�ļ�·��]
set "op="
for /f "tokens=1-3 delims=#=" %%a in ('set ##') do (
    if "%%a"=="!op!" (
        echo,%%b=%%c
    ) else (
        echo,%%a
        set "op=%%a"
        echo,%%b=%%c
    )
)

