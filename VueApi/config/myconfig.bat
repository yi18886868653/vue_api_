@echo off&setlocal ENABLEDELAYEDEXPANSION
call :解析 config.ini
call :提取 DRIVER driver
call :修改 DRIVER driver %1
call :输出 >d:\vue_api\VueApi\config\config.ini
goto :eof
 
 
:解析 [参数#1=ini文件路径]
set "op="
for /f " usebackq tokens=1* delims==" %%a in ("%~1") do (
    if "%%b"=="" (
        set "op=%%a"
    ) else (
        set "##!op!#%%a=%%b"
    )
)
goto :eof

 
:提取 [参数#1=Option] [参数#2=Key]
echo,Option=%~1,Key=%~2,Value=!##[%~1]#%~2!
goto :eof
 

:修改 [参数#1=Option] [参数#2=Key] [参数#3=value，没有参数3则删除该配置项]
set "##[%~1]#%~2 = %~3"
goto :eof
 


:输出 [>新ini文件路径]
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

