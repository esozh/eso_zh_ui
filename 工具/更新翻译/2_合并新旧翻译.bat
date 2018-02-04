@echo off

echo ### 正在合并
cd ../../scripts/
python merge_xls_dir.py ../输出/更新翻译/1_new/ ../输出/更新翻译/4_old/ ../输出/更新翻译/2_diff/

echo ### 正在设置格式
python apply_xls_format.py ../输出/更新翻译/1_new/ ../输出/更新翻译/2_diff/
pause
