#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : check_xls.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 检查翻译的 xls 的格式
# 


import os
import re
import sys
from xlsutils import load_xls


def usage():
    print('usage:')
    print('python check_xls.py file_name column_id [origin_column_id]')


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        usage()
        sys.exit(2)

    src_path = sys.argv[1]
    column_id = int(sys.argv[2])    # 待查列
    origin_column_id = None if len(sys.argv) == 3 else int(sys.argv[3])     # 原文列

    # check translation
    check_xls(src_path, column_id, origin_column_id)


def check_xls(src_path, column_id, origin_column_id):
    data = load_xls(src_path)
    for line in data:
        text_is_ok = False
        try:
            text_is_ok = check_string(line[column_id])
            if origin_column_id is not None:
                text_is_ok &= check_string_with_origin(line[column_id], line[origin_column_id])
        except Exception as e:
            print(e)
        if not text_is_ok:
            print('> failed when checking:\n%s\n' % ', '.join(line))


def check_string(text_to_check):
    """检查是否符合规范，输出错误"""
    if text_to_check == '':
        return True

    stack = {'<>': 0, 'c': 0, 't': 0}
    i = 0
    len_text = len(text_to_check)

    while i < len_text:
        curr_char = text_to_check[i]
        # <<>> 的匹配
        if curr_char == '<':
            if i+1 < len_text and text_to_check[i+1] == '<':
                # 可能只是单独的 < 符号
                stack['<>'] += 1
                i += 1
        elif curr_char == '>':
            if i+1 < len_text and text_to_check[i+1] == '>':
                stack['<>'] -= 1
                i += 1
        elif curr_char == '|':
            # 颜色
            if text_to_check[i+1] == 'c':
                search_not_match = re.compile(r'[^0-9a-fA-F]').search
                if search_not_match(text_to_check[i+2:i+2+6]):    # 含有颜色以外的字符
                    return False
                stack['c'] += 1
                i += 7
            # 颜色结束
            elif text_to_check[i+1] == 'r':
                stack['c'] -= 1
                i += 1
            # 调用
            elif text_to_check[i+1] == 't':
                if stack['t'] == 0:
                    stack['t'] += 1
                    i += 1
                else:
                    stack['t'] -= 1
                    i += 1
        elif curr_char == '\\':
            if text_to_check[i+1] not in r'\n"':
                return False
            i += 1
        # <<>> 之间内容检查，暂无
        # 数量检查
        # |c |r 的情况似乎比较灵活
        if stack['<>'] < 0 or stack['<>'] > 1 or stack['c'] < -1 or stack['c'] > 1 or stack['t'] > 1:
            return False
        # iter
        i += 1

    # 最终的匹配检查
    if stack['<>'] != 0 or stack['c'] < -1 or stack['c'] > 1 or stack['t'] != 0:
        return False
    return True


def check_string_with_origin(text_to_check, origin_text):
    """比较翻译前后文本的属性，例如 \n 数量"""
    if text_to_check == '' or origin_text == '':
        return True
    attr_check = count_string_attr(text_to_check)
    attr_origin = count_string_attr(origin_text)
    for key in attr_check.keys():
        if key not in attr_origin or attr_check[key] != attr_origin[key]:
            return False
    return True


def count_string_attr(text_to_check):
    """统计文本的属性，例如 \n 的个数"""
    count = {'<>': 0, 'c': 0, 't': 0, 'bs': 0, 'n': 0, 'q': 0}
    len_text = len(text_to_check)

    for i in range(0, len_text):
        if text_to_check[i] == '<' and i+1 < len_text and text_to_check[i+1] == '<':
            count['<>'] += 1
        elif text_to_check[i] == '>' and i+1 < len_text and text_to_check[i+1] == '>':
            count['<>'] += 1
        elif text_to_check[i] == '|' and text_to_check[i+1] == 'c':
            count['c'] += 1
        elif text_to_check[i] == '|' and text_to_check[i+1] == 't':
            count['t'] += 1
        elif text_to_check[i] == '\\' and text_to_check[i+1] == '\\':
            count['bs'] += 1
        elif text_to_check[i] == '\\' and text_to_check[i+1] == 'n':
            count['n'] += 1
        elif text_to_check[i] == '\\' and text_to_check[i+1] == '"':
            count['q'] += 1
    return count


if __name__ == '__main__':
    if os.name == 'nt':
        sys.stdout = open(1, 'w', encoding='utf-8', closefd=False)  # windows
    main()
