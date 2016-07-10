## 常见问题

#### 汉化不生效

- 请检查是否按照安装顺序正确安装
- 检查 "文档\Elder Scrolls Online\live\UserSettings.txt" 中是否设置了 `SET Language.2 "zh"`

#### 与其他插件冲突报错

1. 寻找导致报错的插件
2. 到插件所在路径，检查是否有和本地化相关的文件，例如`en.lua`，`fr.lua`，`de.lua`，`Data-en.lua`
3. 复制一份该文件，并把文件名中的 "en" 改成 "zh"

#### 弹框提示 UI ERROR

Lua is reaching its memory limit.
You should consider disabling some addons and reloading the UI.

说明 LUA 可用内存不足。
可以修改 "文档\Elder Scrolls Online\live\UserSettings.txt"
中的 `SET LuaMemoryLimitMB "64"`，
把数字改大，例如改成256.
