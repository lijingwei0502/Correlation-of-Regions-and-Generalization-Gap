import matplotlib.pyplot as plt
import numpy as np
import os


nets = ['resnet18','resnet34', 'resnet50', 'VGG19', 'ResNeXt29_2x64d', 'MobileNet', 'DPN92', 'SENet18', 'ShuffleNetV2', 'EfficientNetB0', 'RegNetX_200MF', 'SimpleDLA']
# 读取数据

for net in nets:
    root = 'final/' + str(net) + '.txt'
    data = np.genfromtxt(root)

    # 打印原始数据的行数
    print("原始数据的行数:", data.shape[0])

    # 定义 structured array 的 dtype
    dtype = [('col' + str(i), float) for i in range(data.shape[1])]

    # 将数据转换为 structured array
    structured_data = np.core.records.fromarrays(data.T, dtype=dtype)

    # 根据最后三列排序
    sorted_data = np.sort(structured_data, order=['col23', 'col24', 'col25'])

    # 使用 numpy 的 split 函数根据最后三列分组
    unique_keys, indices = np.unique(sorted_data[['col23', 'col24', 'col25']], return_index=True, axis=0)
    grouped_data = np.split(sorted_data, indices[1:])

    # 对每个组进行平均
    averaged_data = []
    for group in grouped_data:
        # 将每个分组转换为普通的 NumPy 数组
        group_array = np.array(group.tolist())
        averaged_data.append(group_array.mean(axis=0))

    averaged_data = np.array(averaged_data)
    # 打印处理后数据的行数
    print("处理后数据的行数:", averaged_data.shape[0])

    indexs = [1,5,10,15,20]
    # 为每个 epoch 值绘制并保存一张散点图
    for index in indexs:
        # 过滤出当前 epoch 的数据
        x_current = averaged_data[:, index]
        y_current = averaged_data[:, 21]-averaged_data[:, 22]

        correlation = np.corrcoef(x_current, y_current)[0, 1]  # 计算相关系数

        # 绘制散点图
        plt.scatter(x_current, y_current)
        plt.xlabel('Number of Regions')
        plt.ylabel('Generalization Gap')
        plt.title(f'Correlation: {correlation:.2f}')
        if os.path.exists('result_corr') == False:
            os.mkdir('result_corr')
        plt.savefig(f'result_corr/correlation_epoch_{index*10}.png')  # 保存图像
        plt.clf()  # 清除当前图像
        if index == 20:
            f = open('final/' + 'correlation.txt', 'a')
            f.write(str(net) + ' ' + str(correlation) + '\n')


