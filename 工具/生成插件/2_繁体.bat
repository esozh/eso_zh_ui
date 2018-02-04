@echo off

python main.py 2

if %ERRORLEVEL% == 0 (
cd ..\..\输出\生成繁体插件
explorer .
echo 完成
) else (
echo ### 操作失败
)

pause