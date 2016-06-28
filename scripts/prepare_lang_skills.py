#!/usr/bin/env python
# -*- coding:utf-8 -*-
# File          : prepare_lang_skills.py
# Author        : bssthu
# Project       : eso_zh_ui
# Description   : 提取技能名、技能描述，放到同一个文件中
# 


from utils import prepare_lang_name_and_desc, save_lang_name_and_desc


def main():
    skill_name_file_id = '198758357'
    skill_desc_file_id = '132143172'

    # load, match name and desc
    name_desc = prepare_lang_name_and_desc(skill_name_file_id, skill_desc_file_id)
    name_desc_jp = prepare_lang_name_and_desc(skill_name_file_id, skill_desc_file_id, lang='jp')

    # save
    dest_filename = 'en.skills.lang.csv'
    save_lang_name_and_desc(dest_filename, 'skill', '技能名', '描述', name_desc, name_desc_jp)


if __name__ == '__main__':
    main()
