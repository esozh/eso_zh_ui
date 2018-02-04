@echo off

python main.py 1

if %ERRORLEVEL% == 0 (
cd ..\..\输出\搜索工具
explorer .
echo 完成
) else (
echo ### 操作失败
)

pause