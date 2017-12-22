#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 19:35:56 2017

@author: Shuo-En
"""

import numpy as np
import pandas
from sklearn import svm, model_selection, preprocessing, metrics

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

clf = svm.SVC(kernel='rbf', C = 100, random_state=0, gamma = 'auto')
clf.fit(train, train_ans.ravel())

pre_ans = clf.predict(test)

pre_cnt = 0
true_cnt = 0
get_cnt = 0
    
for i in range(0, len(test_ans)):
    if(test_ans[i]==1 and pre_ans[i]==1):
        get_cnt += 1
    if(test_ans[i]==1):
        true_cnt += 1
    if(pre_ans[i] == 1):
        pre_cnt += 1

accuracy = metrics.accuracy_score(test_ans, pre_ans)
print(accuracy)

print("pre:{}%  recall:{}%".format(int(get_cnt/pre_cnt*100), 
                                   int(get_cnt/true_cnt*100)))
