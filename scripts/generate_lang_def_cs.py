#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : generate_lang_def_cs.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 为 lang_finder 生成 LangDef.cs 的后半部分
# 


from utils.lang_def import *


def main():
    print('        private void InitPairSet()')
    print('        {')
    print('            pairs = new HashSet<string>();')
    print('')
    for k, v in sorted(file_id_of_pair.items()):
        print('            pairs.Add("%s");' % v[0])
        print('            pairs.Add("%s");' % v[1])
    print('        }')
    print('')
    print('        private void InitCategoryToName()')
    print('        {')
    print('            categoryToName = new Dictionary<string, string>();')
    print('')
    for k, v in sorted(category_names.items()):
        print('            categoryToName.Add("%s", "%s");' % (k, v))
    print('        }')
    print('')
    print('        private void InitFileidToCategory()')
    print('        {')
    print('            fileidToCategory = new Dictionary<string, string>();')
    print('')
    print('            fileidToCategory.Add("UI", "UI");')
    for k, v in sorted(list(file_id_of_list.items()) + list(file_id_of_array.items()) + list(file_id_of_pair.items())):
        for _id in v:
            print('            fileidToCategory.Add("%s", "%s");' % (_id, k))
    print('        }')
    print('    }')
    print('}')


if __name__ == '__main__':
    main()
