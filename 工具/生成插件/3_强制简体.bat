@echo off

python main.py 3

if %ERRORLEVEL% == 0 (
cd ..\..\输出\生成简体插件
explorer .
echo 完成
) else (
echo ### 操作失败
)

pause