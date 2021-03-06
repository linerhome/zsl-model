# -*- coding: UTF-8 -*-

import io
import os

import numpy as np
import tensorflow as tf

from sklearn import svm, naive_bayes
from sklearn.calibration import CalibratedClassifierCV

from dap.utils import class_name_of_split, reader

def train_single_svm_clf(train_data, train_attr):
    """Train a svm classifier for an attribute.

    Args:
        train_data: image features used to train svm classifier, of shape (num of examples, feature dimension)
        train_attr: the binary indicating value of attribute, of shape (num of examples, 1) 

    Returns:
        calibrated_svm_clf: svm classifier for current attribute
    """
    # 卡方核的计算不能存在负值，需要进行对特征进行处理才能使用
    # 先采用线性核计算
    # features = features_with_chi2_kernel(train_data, 3)

    svm_clf = svm.LinearSVC()
    calibrated_svm_clf = CalibratedClassifierCV(svm_clf, method='sigmoid', cv=5)
    calibrated_svm_clf.fit(train_data, train_attr)

    return calibrated_svm_clf

def train_svm_clfs(train_data, train_label):
    """Train 85 svm for each attribute.
    
    According to the paper, we should use 40 classes for train, 10 classes for test. Thus, the file we should use to extract features for training svm is named 'trainvalidfeatures.npy'.

    Args:
        train_data: features used to training, of shape (num of examples, 512)
        train_label: attributes used to training, of shape (num of examples, num of attributes)

    Returns:
        smv_clfs: all 85 support vector machine corresponding to 85 attributes
    """
    svm_clfs = []

    for attr_index in range(0, 85):
        features = train_data
        attr = train_label[:, attr_index]

        print("\n====================")
        print("SVM count: " + str(attr_index+1))
        print("Current svm training begining...\n")
        current_svm = train_single_svm_clf(features, attr)
        print("Training completed!")
        print("====================\n")

        svm_clfs.append(current_svm)

    return svm_clfs

# def train_model(data):
#     """
#     """
#     with tf.Session() as sess:
#         print("\n////////// Training process //////////\n\n")
#         svm_clfs = train_svm_clfs(data['train_data'], data['train_label'])

#         model = 
#         print("\n\n////////// Training completed //////////\n")

#     return model