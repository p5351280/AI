#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 01:58:13 2017

@author: Shuo-En
"""

import numpy as np
import pandas
from sklearn import preprocessing, tree
from sklearn.ensemble import AdaBoostClassifier, RandomForestClassifier

TRAIN = pandas.read_csv('TraData.csv', dtype={'click': np.float64}).as_matrix()
train_num = TRAIN.shape[0]
TEST = pandas.read_csv('input.csv').as_matrix()
test_num = TEST.shape[0]
all_num = train_num+test_num

DATA = np.zeros((all_num, 13), dtype=object)
DATA[0:train_num, :] = TRAIN
DATA[train_num:all_num, 0:12] = TEST

for i in range(0, 12):  
    if i==5 or i==9:
        DATA[:, i]=0
        continue
    label_encoder = preprocessing.LabelEncoder()
    encode = label_encoder.fit_transform(DATA[:, i].astype(str))
    DATA[:, i] = encode

DATA = np.array(DATA, dtype='float')
TRAIN = DATA[0:train_num, :]
TEST = DATA[train_num:all_num, :]

train = TRAIN[:, 0:12]
train_ans = TRAIN[:, 12:13]

clf = AdaBoostClassifier(
        RandomForestClassifier(class_weight = {0:1, 1:10}, max_features=None, 
                               n_jobs=-1),
        n_estimators = 40, learning_rate = 0.05)
clf.fit(train, train_ans.ravel())

test = TEST[:, 0:12]

print("\n\n\n")
pre_ans = clf.predict(test)
np.savetxt('output.csv', pre_ans, delimiter=',', fmt='%d')
print("Finish!")