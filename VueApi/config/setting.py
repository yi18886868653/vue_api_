#!/usr/bin/env python
# _*_ coding:utf-8 _*_
__author__ = 'Administrator'

import os,sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)


# 配置文件
CONFIG_DIR = os.path.join(BASE_DIR, "config", "config.ini")

# 元素控件
TEST_Element_YAML = os.path.join(BASE_DIR,"testyaml")

#CSV文件
EXCEL_DIR_CSV = os.path.join(BASE_DIR, "config", "case.csv")

#Excel文件
EXCEL_DIR = os.path.join(BASE_DIR, "config", "case.xlsx")


#yaml文件
YAML_DIR = os.path.join(BASE_DIR,"myconfig","login.yaml")

