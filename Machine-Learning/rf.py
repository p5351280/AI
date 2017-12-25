#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 02:22:07 2017

@author: Shuo-En
"""

import numpy as np
import pandas
from sklearn import preprocessing, metrics, model_selection
from sklearn.ensemble import RandomForestClassifier

DATA = pandas.read_csv('TraData.csv', dtype={'click': np.float64}).as_matrix()

for i in range(0, 12):  
    label_encoder = preprocessing.LabelEncoder()
    encode = label_encoder.fit_transform(DATA[:, i].astype(str))
    for j in range(0, len(encode)):
        encode[j] = float(encode[j])
    DATA[:, i] = encode

DATA = np.array(DATA, dtype='float')
DATA_X = DATA[:, 0:12]
DATA_Y = DATA[:, 12:13]

train, test, train_ans, test_ans = model_selection.train_test_split(
                                    DATA_X, DATA_Y, test_size = 0.2)
'''
train = DATA[0:861457 , 0:12]
train_ans = DATA[0:861457, 12:13]
test = DATA[861457:961457, 0:12]
test_ans = DATA[861457:961457, 12:13]
'''

clf = RandomForestClassifier(random_state=0, n_estimators=10,)
clf.fit(train, train_ans.ravel())
pre_ans = clf.predict(test)


accuracy = metrics.accuracy_score(test_ans, pre_ans)
print(accuracy)

print(metrics.classification_report(test_ans, pre_ans))