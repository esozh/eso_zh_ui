@echo off

REM 老滚安装路径
set ESO_PATH=F:\Program Files (x86)\SteamLibrary\steamapps\common\Zenimax Online\The Elder Scrolls Online

python main.py 1 %ESO_PATH%

if %ERRORLEVEL% == 0 (
cd ..\..\输出\更新翻译
explorer .
echo 完成，请把旧的文件拷贝到 4_old\ 中
) else (
echo ### 操作失败
)

pause