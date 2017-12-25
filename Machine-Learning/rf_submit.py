#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 01:58:13 2017

@author: Shuo-En
"""

import numpy as np
import pandas
from sklearn import preprocessing, metrics, model_selection
from sklearn.ensemble import RandomForestClassifier

TRAIN = pandas.read_csv('TraData2.csv', dtype={'click': np.float64}).as_matrix()
train_num = TRAIN.shape[0]
TEST = pandas.read_csv('input.csv', dtype={'click': np.float64}).as_matrix()
test_num = TEST.shape[0]
all_num = train_num+test_num

DATA = np.zeros((all_num, 13), dtype=object)
DATA[0:train_num, :] = TRAIN
DATA[train_num:all_num, :] = TEST

for i in range(0, 12):  
    label_encoder = preprocessing.LabelEncoder()
    encode = label_encoder.fit_transform(DATA[:, i].astype(str))
    DATA[:, i] = encode

DATA = np.array(DATA, dtype='float')
TRAIN = DATA[0:train_num, :]
TEST = DATA[train_num:all_num, :]

train = TRAIN[:, 0:12]
train_ans = TRAIN[:, 12:13]

#train, vali, train_ans, vali_ans = model_selection.train_test_split(
#                                    train, train_ans, test_size = 0)

clf = RandomForestClassifier(random_state=0, n_estimators=10,)
clf.fit(train, train_ans.ravel())
'''
pre_ans = clf.predict(vali)
accuracy = metrics.accuracy_score(vali_ans, pre_ans)
print(accuracy)
print(metrics.classification_report(vali_ans, pre_ans))
'''
test = TEST[:, 0:12]
test_ans = TEST[:, 12:13]

print("\n\n\n")
pre_ans = clf.predict(test)
accuracy = metrics.accuracy_score(test_ans, pre_ans)
print(accuracy)
print(metrics.classification_report(test_ans, pre_ans))
