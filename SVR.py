import csv,pandas,re
from sklearn.datasets import load_boston
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np

# 0 读取数据
oridata = []
with open('a.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        oridata.append(row)
# print(oridata)

# 1 处理数据
data = []
Street = {}
Community = {}
Heading = {'East':'1','South':'1.1','West':'1.2','North':'1.3','east':'1','south':'1.1','west':'1.2','north':'1.3'}
countStreet = 0
countCommunity = 0
countHeading = 0
for i in range(len(oridata)-1):
    item = oridata[i+1]
    line = ['']*16
    data.append(line)

    if item[1] in Street.keys():
        data[i][0] = Street[item[1]]
    else:
        data[i][0] = countStreet
        Street[item[1]] = countStreet
        countStreet = countStreet + 1
    
    if item[2] in Community.keys():
        data[i][1] = Community[item[2]]
    else:
        data[i][1] = countCommunity
        Community[item[2]] = countCommunity
        countCommunity = countCommunity + 1
    
    headscore = 0
    for head in Heading.keys():
        if head in item[9]:
            headscore = headscore + float(Heading[head])
    if headscore > 2:
        headscore = headscore /2
    data[i][8] = int((headscore - 1)*20)


    data[i][11] = re.findall('(.*?)㎡',(item[12][:-1]),re.S)[0]

    if 'Yes' in item[14]:
        data[i][13] = 1
    else:
        data[i][13] = 0


    if 'Fine' in item[16]:
        data[i][15] = 1
    else:
        data[i][15] = 0

    if 'High' in  item[15]:
        data[i][14] = 2
    elif 'Mid' in item[15]:
        data[i][14] = 1
    else:
        data[i][14] = 0

    for j in [3,4,5,6,7,8,10,11,13]:
        data[i][j-1] = float(item[j])

xx = []
yy = []
for i in range(len(data)):
    yy.append(data[i][2])
    xx.append([])
    for j in [0,1,3,4,5,6,7,8,9,10,11,12,13,14,15]:
        xx[i].append(data[i][j])
x = np.array(xx)
y = np.array(yy)
# print(len(x),len(y))

# 2 分割训练数据和测试数据
# 随机采样25%作为测试 75%作为训练
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, random_state=33)


# 3 训练数据和测试数据进行标准化处理
ss_x = StandardScaler()
x_train = ss_x.fit_transform(x_train)
x_test = ss_x.transform(x_test)

ss_y = StandardScaler()
y_train = ss_y.fit_transform(y_train.reshape(-1, 1))
y_test = ss_y.transform(y_test.reshape(-1, 1))

# 4.1 支持向量机模型进行学习和预测
# 线性核函数配置支持向量机
linear_svr = SVR(kernel="linear")
# 训练
linear_svr.fit(x_train, y_train)
# 预测 保存预测结果
linear_svr_y_predict = linear_svr.predict(x_test)

# 多项式核函数配置支持向量机
poly_svr = SVR(kernel="poly")
# 训练
poly_svr.fit(x_train, y_train)
# 预测 保存预测结果
poly_svr_y_predict = linear_svr.predict(x_test)
print(poly_svr_y_predict)

# 5 模型评估
# 线性核函数 模型评估
print("线性核函数支持向量机的默认评估值为：", linear_svr.score(x_test, y_test))
print("线性核函数支持向量机的R_squared值为：", r2_score(y_test, linear_svr_y_predict))
print("线性核函数支持向量机的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),
                                              ss_y.inverse_transform(linear_svr_y_predict)))
print("线性核函数支持向量机的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),
                                                 ss_y.inverse_transform(linear_svr_y_predict)))
# 对多项式核函数模型评估
print("对多项式核函数的默认评估值为：", poly_svr.score(x_test, y_test))
print("对多项式核函数的R_squared值为：", r2_score(y_test, poly_svr_y_predict))
print("对多项式核函数的均方误差为:", mean_squared_error(ss_y.inverse_transform(y_test),
                                           ss_y.inverse_transform(poly_svr_y_predict)))
print("对多项式核函数的平均绝对误差为:", mean_absolute_error(ss_y.inverse_transform(y_test),
                                              ss_y.inverse_transform(poly_svr_y_predict)))


# 最后输出结果
'''
线性核函数支持向量机的默认评估值为： 0.977350828793
线性核函数支持向量机的R_squared值为： 0.977350828793
线性核函数支持向量机的均方误差为: 0.0648269681575
线性核函数支持向量机的平均绝对误差为: 0.181794726472
对多项式核函数的默认评估值为： -0.335772572852
对多项式核函数的R_squared值为： 0.977350828793
对多项式核函数的均方误差为: 0.0648269681575
对多项式核函数的平均绝对误差为: 0.181794726472
'''