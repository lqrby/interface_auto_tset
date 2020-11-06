# !/usr/bin/python3.6
# -*- coding: UTF-8 -*-
# author: lucien
# 基础包： locust趋势图生成包
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import dates

hex_colors = [
    '#FF7500',
    '#9400D3',
    '#ADFF2F',
    '#FF0000',
    '#000000',
    '#0000FF',
    '#00FF00',
    '#696969',
    '#7FFF00',
    '#F00056',
    '#0EB83A',
    '#00BC12',
    '#1BD1A5',
    '#0C8918',
    '#0AA344',
    '#2ADD9C',
    '#3DE1AD',
    
    
    
]


class data_analyse():
    def __init__(self, filename):
        self.filename = filename
        self.xfmt = dates.DateFormatter('%m/%d %H:%M')
        self._init_graph()  # 初始化趋势图大小
        self._set_graph()  # 初始化趋势图样式

        # headers = ['time', 'label', 'loglevel', 'method', 'name', 'response_time', 'size']  # 命名字段标题
        headers = ['time', 'label', 'loglevel', 'method', 'name', 'response_time', 'size']  # 命名字段标题
        self.data = pd.read_csv(filename, sep='|', names=headers, skiprows=1, encoding="gbk")  # 从文件获取内容为DATAFRAME格式
        # data=pd.read_csv('F:/myTestFile/TestObject/YouTime/report/example_requests.csv',encoding='unicode_escape')#导入csv文件
        for col in headers[-2:]:  # 转换response_time和size为int型
            self.data[col] = self.data[col].apply(lambda x: int(x))
        for col in headers[0:-2]:  # 取消掉所有非int型的空格
            self.data[col] = self.data[col].apply(lambda x: x.strip())
        self.data['time'] = self.data['time'].apply(
            lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S,%f'))  # time转化为时间格式
        self.sorted_data = self.data.sort_values(by=['time', 'name'], ascending=[True, True])  # 对数据按照time和name进行降序排列
        self.grouped_data = self.sorted_data.groupby('name')  # 对降序排列的数据，按名称分组
        self.requests_counts = np.array([[key, len(group)] for key, group in self.grouped_data])  # 构建请求名和请求次数数组

    def _init_graph(self):  # 设定趋势图大小
        left, width = 0.1, 0.8
        bottom, height = 0.1, 0.8
        self.trend_scatter = [left, bottom, width, height]

    def _set_graph(self):  # 生成基本趋势图样式
        plt.clf()  # 清除figure中所有axes
        self.ax_plot = plt.axes(self.trend_scatter)  # 套用axes大小
        self.ax_plot.grid(True)  # 打开网格
        self.ax_plot.set_ylabel('Response Time(ms)')  # 纵坐标标题
        self.ax_plot.set_xlabel('time')  # 横坐标标题
        self.ax_plot.figure.set_size_inches(15, 8)  # 画板大小
        self.ax_plot.xaxis.set_major_locator(dates.MinuteLocator(interval=5))  # 设定横坐标日期格式为5min间隔
        self.ax_plot.xaxis.set_major_formatter(self.xfmt)  # 设定横坐标格式

    def generate_trend(self):  # 生成趋势图
        start_index = 0
        legend_list = []
        for index, request in enumerate(self.requests_counts):  # 为数组添加index标签
            name, count = request[0], int(request[1])  # 获取请求名和请求次数
            end_index = start_index + count
            x = self.grouped_data.get_group(name)['time'][start_index: end_index]  # 设置x轴数据
            y = self.grouped_data.get_group(name)['response_time'][start_index:end_index]  # 设置y轴数据
            self.ax_plot.plot(x, y, '-', color=hex_colors[index + 1])  # 画图
            legend_list.append(name)  # 添加请求名到legend中
        plt.legend(legend_list)  # 打印legend
        # plt.show()  # 打印趋势图
        plt.title(self.filename)
        plt.savefig(fname='.'.join([self.filename, 'png']), dpi=300, bbox_inches='tight')  # 保存趋势图


if __name__ == "__main__":
    filename = 'F:/myTestFile/TestObject/YouTime/report/locust_log.txt'
    data = data_analyse(filename)
    data.generate_trend()
    