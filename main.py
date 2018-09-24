# -*- coding: UTF-8 -*-

import io

from sklearn import svm
import numpy as np
from skimage import io as skio

from keras.models import Model
from keras import layers

from helper_function import img_reader, attribute_reader, VGG19, get_cls

# 用来保存85个二分类支持向量机
svm_85 = []

################################################################################

# 首先是数据处理
# 先取得一个测试用的小数据集
# 图片：(num_examples, num_pixles)
# 标签：(num_examples, binary_feature)

# 训练用图片
train_img = img_reader(dataset_name='AWA', data_type='train')
# 训练图片对应的属性向量
train_attributes = attribute_reader('train')
# 训练图片的标签 这里标签和图片关系的对应有问题
train_label = get_cls('train')

# 将训练用的图片提取图片特征
train_img_feature = VGG19(train_img)



################################################################################

# 对每一个图片级别的属性训练一个支持向量机
# 将图片的属性分割
feature = {}

for value in range(0, 84):
    feature[value] = np.vsplit(train_img_feature, 85)
    svm_85[value] = svm.SVC(kernel='linear')
    svm_85[value].fit(feature[value], train_label)


# 实现从‘图片-属性’层的操作：进来一张新的图片，判断它包含哪些属性
img_feature_list = []
for value in range(0, 84):
    predect_value = svm_85[value].predict(feature[value])
    if predect_value > 0:
        img_feature_list.append(1)
    else:
        img_feature_list.append(0)




################################################################################

# 上面得到了从图片到属性的判断
# 本质上应该还需要一个从类别到属性的预测
# 但AWA数据集中用来测试的类别已经直接给出了属性标签

################################################################################

# 最后用贝叶斯定理来实现对图像类别的预测