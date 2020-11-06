import matplotlib.pyplot as plt

import pandas as pd

import time


def _init_graph(self):  # 设定趋势图大小
    left, width = 0.1, 0.8
    bottom, height = 0.1, 0.8
    self.trend_scatter = [left, bottom, width, height]
# data=pd.read_csv('F:/myTestFile/TestObject/YouTime/report/example_requests.csv',encoding='unicode_escape')#导入csv文件
data=pd.read_csv('F:/myTestFile/TestObject/YouTime/report/example_requests.csv',encoding='unicode_escape')#导入csv文件
data['number'] = 10
print("*********",data,"******")
y=data['number'].T.values #设置y轴数值 ,.T是转置
print(y)
x=[]
y = []

# array=[0,len(y)]

# for i in array:

#      x[i]=time.mktime(time.strptime(data['tm'][i],"%Y-%m-%d %H:%M:%S")) #将string类型的时间字符串转换为float类型

plt.figure(figsize=(10,6))

plt.plot(x,y,'')

plt.xlabel('date')

plt.ylabel('number')

plt.show()
