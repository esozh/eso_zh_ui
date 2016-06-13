#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : convert_lua_to_str.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 将从 mnf 中解出的， esoui 文件夹下的 en_client.lua 等转换为 .str 文件
# 


import sys


def usage():
    print('usage:')
    print('python convert_lua_to_str.py en_client.lua')


def main():
    if len(sys.argv) != 2:
        usage()
        return

    src_path = sys.argv[1].strip()
    if not src_path.endswith('.lua'):
        usage()
        return

    name_values = []
    with open(src_path, 'rt', encoding='utf-8') as fp:
        for line in fp.readlines():
            line = line.strip()
            if line.startswith('SafeAddString'):
                name = line.split('(', 1)[1].split(',', 1)[0].strip()
                value = line.split(',', 1)[1].split(',', -1)[0].strip().strip('"')
                name_values.append((name, value))

    dest_path = src_path[:-3] + 'str'
    print(dest_path)
    with open(dest_path, 'wt', encoding='utf-8') as fp:
        for name, value in name_values:
            fp.write('[%s] = "%s"\n' % (name, value))


if __name__ == '__main__':
    main()
