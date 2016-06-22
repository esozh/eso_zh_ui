#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang_skills.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 提取技能名、技能描述，放到同一个文件中
# 


import os
import sys
from utils import load_lang_csv


def load_index_and_text_from_csv(file_path):
    """从 csv 中读取文本，并用 index 当作其索引"""
    data = load_lang_csv(file_path, skip_header=False)
    data_dict_by_index = {}
    for _id, unknown, index, offset, text in data:
        index = int(index)
        if index in data_dict_by_index:     # 如果 index 没有重复，将来就可以只用 index 来反查
            raise RuntimeError('duplicate index')
        data_dict_by_index[index] = text
    return data_dict_by_index


def main():
    skill_name_file_id = '198758357'
    skill_desc_file_id = '132143172'

    cd = sys.path[0]
    translation_path = os.path.join(cd, '../translation/lang')
    dest_path = translation_path

    # load
    skill_name_file = os.path.join(translation_path, 'en.%s.lang.csv' % skill_name_file_id)
    skill_name_dict = load_index_and_text_from_csv(skill_name_file)
    skill_desc_file = os.path.join(translation_path, 'en.%s.lang.csv' % skill_desc_file_id)
    skill_desc_dict = load_index_and_text_from_csv(skill_desc_file)

    # match name and desc
    name_desc = []
    for index, desc in sorted(skill_desc_dict.items()):
        if index in skill_name_dict.keys():
            name_desc.append([index, skill_name_dict[index], desc])

    # save
    dest_file_name = os.path.join(dest_path, 'en.skills.lang.csv')
    with open(dest_file_name, 'wt', encoding='utf-8') as fp:
        header = '编号\t英文技能名\t中文技能名\t英文描述\t中文描述\t初翻人员\t校对\t润色\t备注\n'
        fp.write(header)
        for index, name, desc in name_desc:
            line = 'skill-%05d\t%s\t\t%s\t\t\t\t\t\n' % (index, name, desc)
            fp.write(line)


if __name__ == '__main__':
    main()
