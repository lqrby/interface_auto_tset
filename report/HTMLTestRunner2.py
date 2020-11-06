import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
csv_data = np.loadtxt(open('F:/myTestFile/TestObject/YouTime/report/example_requests.csv',"rb"),delimiter=",",skiprows=0)
np.argsort(csv_data, axis=0)#排序
a,b=csv_data.shape
print(a,b)
# plt.xlabel('x')
# plt.ylabel('y')
# plt.title('Data')
# plt.legend()
# tidu=1000
# qq=a/tidu
# for j in range(0,int(qq)):
#     x, y = csv_data[tidu*j:tidu*j+tidu, 0], csv_data[tidu*j:tidu*j+tidu, 1]
#     #plt.scatter(x, y, s=0.01, c="#0000ff", marker='o')
#     plt.plot(x, y, '*', label='Data', color='black')
#     plt.show()

#绘制散点图
x, y = csv_data[:, 0], csv_data[:, 1]
plt.legend()
plt.plot(x, y, '*', label='Data', color='black')
# plt.scatter(x, y, s=0.01, c="#0000ff", marker='o')
plt.tick_params(axis='both',which='major',labelsize=1)
plt.savefig('./test2.png')
plt.show()
