import matplotlib.pyplot as plt

# 定义数据点
points = [(0,0), (0,3), (4,0), (1,2), (4,3), (5,2)]

# 解压数据点
x_values, y_values = zip(*points)

# 创建散点图
plt.scatter(x_values, y_values)

# 设置图表标题和坐标轴标签
plt.title('数据点可视化')
plt.xlabel('X轴')
plt.ylabel('Y轴')

# 显示图表
plt.show()