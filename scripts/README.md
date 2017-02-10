## UI 汉化

### 流程

```txt
.lua -> _translate.txt -> .xls
.xls -> _translate.txt
.lua + str_header.txt + _translate.txt -> .str
```

### 脚本使用说明

#### convert_lua_to_txt.py
>.lua -> _translate.txt

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

#### convert_txt_to_xls.py
>_translate.txt -> .xls

从 `translation/zh_translate.txt` 中提取翻译文本，
转换成翻译、校对使用的 xls 文件。

#### export_uixls_to_txt.py
>.xls -> _translate.txt

将文本从翻译后的 xls 文件导出到 `translation/zh_translate.txt` 中。

#### convert_txt_to_str.py
>.lua + str_header.txt + _translate.txt -> .str

从 `translation/zh_translate.txt` 中提取翻译文本，
从 `translation/str_header.txt` 中读取文件头，
再根据 `translation/zh_pregame.lua`, `translation/zh_client.lua`
生成 `AddOns/esoui/lang/zh_pregame.str`, `AddOns/esoui/lang/zh_client.str`。

可以通过 `-m` 参数选择 origin, translation, both 三种模式之一。


## lang 汉化

### 流程

```txt
.lang <--> .lang.csv -> .id.lang.csv -> .name.lang.csv -> .name.lang.xls
.lang.csv + .*.xls -> .lang.csv
```

### 脚本使用说明

#### split_lang_csv_by_id.py
>.lang.csv -> .id.lang.csv

以 `translation/lang/en.lang.csv` 中的 id 项为 file_id，用来分割文件。

#### prepare_lang.py
>.id.lang.csv -> .name.lang.csv

从特定的分割好的 `translation/lang/en.id.lang.csv` 中提取文本，
合并、转换成翻译、校对使用的 csv 文件，
用于生成 xls 文件。

#### export_langxls_to_csv.py
>.lang.csv + .*.xls -> .lang.csv

从 `translation/lang/translated/` 中的 `*.xls` 里提取翻译， 
仿照 `translation/lang/en.lang.csv` 和 `translation/lang/jp.lang.csv`
的结构生成 `translation/lang/translated/zh.lang.csv`。


## 其他

#### merge_uixls.py
按要求合并两个 UI 汉化的 xls 文件。

#### merge_langxls.py
按要求合并两个 xls 文件。

#### merge_langxls_dir.py
按要求合并两个目录中的 xls 文件。
对目录1中的每个文件，都去目录2里找它的同类文件，向目录1中的文件导数据。

#### merge_diff_files.py
合并目录中的表示冲突项的 xls 文件。
合并的同时去重、去空（未翻译）、排序，
得到校对用的翻译冲突列表。

#### export_rawxls_to_csv.py
`prepare_lang` 的逆，合并所有导出的 xls 文件，得到去重的 `.lang.csv`。

#### lang_def.py
`.lang.csv` 文件中 id 项的说明。

#### check_xls.py
检查翻译后的 xlsx 文件是否符合语法规范。
```bash
# ./check_xls.py file_name column_id [src_column_id]
python check_xls.py ui.xlsx 3
```

#### apply_xls_format.py
给指定的 xls 文件套用模板中的格式。

#### utils.py

#### xlsutils.py
