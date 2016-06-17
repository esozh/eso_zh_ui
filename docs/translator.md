## 翻译方法

### 一、文本翻译

##### UI翻译
~~~编辑 `translation/zh_translate.txt`。~~~
~~~直接把译文另起一行写在以 "SafeAddString" 开头的原文后即可。~~~

直接编辑UI汉化的xlsx文件，具体任务分配见翻译群。

##### 对话翻译
修改 `zh.lang.translate.csv` 文件。
文件来源是 `en.lang.csv`。

原文件第一行是说明，
从第二行开始是需要翻译的文本。
直接把译文另起一行写在原文后即可。
例如：

```
"75246404","0","232","8686977","Hm?"
嗯？
"75246404","0","233","11440092","Ah, it's you!"
啊，是你！
```

### 二、生成 .str 文件

运行 `/scripts` 下的 `convert_txt_to_str`

```bash
python convert_txt_to_str.py
```

### 三、生成 zh.lang 文件

#### 1. 将 `zh.lang.translate.csv` 转换成 `zh.lang.csv`
```bash
# todo
```

#### 2. 使用 EsoExtractData 软件，将 `zh.lang.csv` 转换成 `zh.lang`。
```bash
esoextractdata -x zh.lang.csv
```

### 四、打包发布

需要打包以下内容：
- esoui/lang/zh_client.str
- esoui/lang/zh_pregame.str
- fonts, 详见 release
- gamedata/lang/zh.lang, 详见 release
