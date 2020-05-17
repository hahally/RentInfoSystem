# -*- coding: utf-8 -*-
from pyecharts import Bar


def draw_bar(all_list):
    print("开始绘图")
    attr = ['天心区','芙蓉区','开福区','岳麓区','雨花区','望城']
    v0 = all_list[0]
    v1 = all_list[1]
    v2 = all_list[2]
    v3 = all_list[3]

    bar = Bar("长沙市租房租金概况")
    bar.add("最小值", attr, v0, is_stack=True)
    bar.add("最大值", attr, v1, is_stack=True)
    bar.add("平均值", attr, v2, is_stack=True)
    bar.add("中位数", attr, v3, is_stack=True)
    bar.render('./templates/result.html')
    print("结束绘图")
