#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 19:35:56 2017

@author: Shuo-En
"""

import numpy as np
import pandas
from sklearn import svm, cross_validation, preprocessing

DATA = pandas.read_csv('TraData.csv', dtype={'click': np.float64}).as_matrix()


for i in range(0, 12):  
    label_encoder = preprocessing.LabelEncoder()
    encode = label_encoder.fit_transform(DATA[:, i].astype(str))
    for j in range(0, len(encode)):
        encode[j] = float(encode[j])
    DATA[:, i] = encode

DATA = np.array(DATA, dtype='float')

test = DATA[861457:961457, 0:12]
test_ans = DATA[861457:961457, 12:13]


for j in range(700000, 961457):
    train = DATA[0:j, 0:12]
    train_ans = DATA[0:j, 12:13]
    clf = svm.SVC(kernel='rbf', C = 100, random_state=0, gamma = 'auto')
    clf.fit(train, train_ans.ravel())

    pre_ans = clf.predict(test)

    pre_cnt = 0
    true_cnt = 0
    get_cnt = 0
    
    for i in range(100000):
        if(test_ans[i]==1 and pre_ans[i]==1):
            get_cnt += 1
        if(test_ans[i]==1):
            true_cnt += 1
        if(pre_ans[i] == 1):
            pre_cnt += 1

    print("{}: pre:{}%  recall:{}%".format(j, int(get_cnt/pre_cnt*100), 
                                              int(get_cnt/true_cnt*100)))
