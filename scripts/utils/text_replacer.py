#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : text_replacer.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 替换中文文本中不需要的特殊标记
# https://gist.github.com/bgusach/a967e0587d6e01e889fd1d776c5f3729
#


import re


class TextReplacer:
    def __init__(self, replacements=None):
        """构造文本替换类
        
        Args:
            replacements (list[tuple[str]] | None): 原始文本: 替换后文本
        """
        if replacements is not None:
            self.replacements = replacements
        else:
            self.replacements = [
                ('"', '""'),
                ('""""', '""'),
                ('\n', r'\n'),
                ('<<a:1>>', '一个<<1>>'),
                ('<<aC:1>>', '一个<<C:1>>'),
                ('<<az:1>>', '一个<<z:1>>'),
                ('<<ma:1>>', '一些<<1>>'),
                ('<<A:1>>', '<<1>>'),
                ('<<AC:1>>', '<<C:1>>'),
                ('<<ACmz:1>>', '<<Cz:1>>'),
                ('<<Ac:1>>', '<<c:1>>'),
                ('<<Acm:1>>', '<<c:1>>'),
                ('<<Am:1>>', '<<1>>'),
                ('<<Amz:1>>', '<<z:1>>'),
                ('<<At:1>>', '<<t:1>>'),
                ('<<Az:1>>', '<<z:1>>'),
                ('<<Azm:1>>', '<<z:1>>'),
                ('<<CA:1>>', '<<C:1>>'),
                ('<<Cmz:1>>', '<<Cz:1>>'),
                ('<<cm:1>>', '<<c:1>>'),
                ('<<m:1>>', '<<1>>'),
                ('<<mCz:1>>', '<<Cz:1>>'),
                ('<<mc:1>>', '<<c:1>>'),
                ('<<mt:1>>', '<<t:1>>'),
                ('<<mz:1>>', '<<z:1>>'),
                ('<<n:1>>', '<<1>>'),
                ('<<tA:1>>', '<<t:1>>'),
                ('<<tm:1>>', '<<t:1>>'),
                ('<<zm:1>>', '<<z:1>>'),
            ]
            # 增广
            for k_v in self.replacements:
                k, v = k_v[0], k_v[1]
                if '1' in k:
                    for i in range(2, 6):
                        self.replacements.append((k.replace('1', str(i)), v.replace('1', str(i))))

        pattern = [k_v[0] for k_v in self.replacements]
        self.replacements = {k_v[0]: k_v[1] for k_v in self.replacements}
        self.regexp = re.compile('|'.join(map(re.escape, pattern)))

    def replace(self, text):
        """替换文本"""
        new_text = self.regexp.sub(lambda match: self.replacements[match.group(0)], text)
        return new_text
