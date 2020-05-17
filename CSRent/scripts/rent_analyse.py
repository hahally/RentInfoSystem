# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType


def spark_analyse(filename):
    print("开始spark分析")
    # 程序主入口
    spark = SparkSession.builder.master("local").appName("rent_analyse").getOrCreate()
    df = spark.read.csv(filename, header=True)

    # max_list存储各个区的最大值，以及min_list,approxQuantile中位数
    # '天心区', '芙蓉区', '开福区', '岳麓区', '雨花区', '望城'
    max_list = [0 for i in range(6)]
    mean_list = [1.2 for i in range(6)]
    min_list = [0 for i in range(6)]
    mid_list = [0 for i in range(6)]
    # 类型转换，十分重要，保证了price列作为int用来比较，否则会用str比较, 同时排除掉一些奇怪的价格，比如写字楼的出租超级贵
    # 或者有人故意标签1元，其实要面议, 还有排除价格标记为面议的


    df = df.filter(df.price != '面议').withColumn("price", df.price.cast(IntegerType()))
    df = df.filter(df.price >= 50).filter(df.price <= 40000)

    # cn_par = ['天心区', '芙蓉区', '开福区', '岳麓区', '雨花区', '望城']
    mean_list[0] = df.filter(df.area == "天心区").agg({"price": "mean"}).first()['avg(price)']
    mean_list[1] = df.filter(df.area == "芙蓉区").agg({"price": "mean"}).first()['avg(price)']
    mean_list[2] = df.filter(df.area == "开福区").agg({"price": "mean"}).first()['avg(price)']
    mean_list[3] = df.filter(df.area == "岳麓区").agg({"price": "mean"}).first()['avg(price)']
    mean_list[4] = df.filter(df.area == "雨花区").agg({"price": "mean"}).first()['avg(price)']
    mean_list[5] = df.filter(df.area == "望城").agg({"price": "mean"}).first()['avg(price)']

    min_list[0] = df.filter(df.area == "天心区").agg({"price": "min"}).first()['min(price)']
    min_list[1] = df.filter(df.area == "芙蓉区").agg({"price": "min"}).first()['min(price)']
    min_list[2] = df.filter(df.area == "开福区").agg({"price": "min"}).first()['min(price)']
    min_list[3] = df.filter(df.area == "岳麓区").agg({"price": "min"}).first()['min(price)']
    min_list[4] = df.filter(df.area == "雨花区").agg({"price": "min"}).first()['min(price)']
    min_list[5] = df.filter(df.area == "望城").agg({"price": "min"}).first()['min(price)']

    max_list[0] = df.filter(df.area == "天心区").agg({"price": "max"}).first()['max(price)']
    max_list[1] = df.filter(df.area == "芙蓉区").agg({"price": "max"}).first()['max(price)']
    max_list[2] = df.filter(df.area == "开福区").agg({"price": "max"}).first()['max(price)']
    max_list[3] = df.filter(df.area == "岳麓区").agg({"price": "max"}).first()['max(price)']
    max_list[4] = df.filter(df.area == "雨花区").agg({"price": "max"}).first()['max(price)']
    max_list[5] = df.filter(df.area == "望城").agg({"price": "max"}).first()['max(price)']

    # 返回值是一个list，所以在最后加一个[0],才能取到里面的数值
    mid_list[0] = df.filter(df.area == "天心区").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[1] = df.filter(df.area == "芙蓉区").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[2] = df.filter(df.area == "开福区").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[3] = df.filter(df.area == "岳麓区").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[4] = df.filter(df.area == "雨花区").approxQuantile("price", [0.5], 0.01)[0]
    mid_list[5] = df.filter(df.area == "望城").approxQuantile("price", [0.5], 0.01)[0]

    all_list = []
    all_list.append(min_list)
    all_list.append(max_list)
    all_list.append(mean_list)
    all_list.append(mid_list)

    print("结束spark分析")
    return all_list
