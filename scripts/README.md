## 脚本使用说明

### convert_lua_to_txt.py
从 `translation/zh_pregame.lua`, `translation/zh_client.lua` 中提取待翻译文本，
并写入 `translation/zh_translate.txt` 中。

`zh_translate.txt` 由 `.lua` 文件中 `SafeAddString` 开头的行合并而成，
每行 `SafeAddString` 之后可以加一行翻译文本，也可以不写。
例如：

```
SafeAddString(SI_GAME_MENU_LOGOUT, "Log Out", 0)
登出
SafeAddString(SI_GAME_MENU_QUIT, "Quit", 0)
退出
SafeAddString(SI_GAME_MENU_RESUME, "Resume", 0)
SafeAddString(SI_GAME_MENU_SETTINGS, "Settings", 0)
```

### convert_txt_to_str.py
从 `translation/zh_translate.txt` 中提取翻译文本，
从 `translation/str_header.txt` 中读取文件头，
再根据 `translation/zh_pregame.lua`, `translation/zh_client.lua`
生成 `AddOns/esoui/lang/zh_pregame.str`, `AddOns/esoui/lang/zh_client.str`。

### convert_txt_to_xls.py
从 `translation/zh_translate.txt` 中提取翻译文本，
转换成翻译、校对使用的 csv 文件，
用于生成 xlsx 文件。

### check_xls.py
检查翻译后的 xls 文件是否符合语法规范。
```bash
# ./check_xls.py file_name column_id [src_column_id]
python check_xls.py ui.xlsx 3
```

### convert_translate_to_lang.py
从 `translation/lang/zh.lang.translate.csv` 中提取原文及翻译文本，
生成 `translation/lang/zh.lang.csv`
