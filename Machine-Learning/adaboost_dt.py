#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 02:22:07 2017

@author: Shuo-En
"""

import numpy as np
import pandas
from sklearn import preprocessing, metrics, model_selection, tree
from sklearn.svm import SVC
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.grid_search import GridSearchCV

DATA = pandas.read_csv('TraData.csv', dtype={'click': np.float64}).as_matrix()

for i in range(0, 12):  
    if i==5 or i==9:
        DATA[:, i]=0
        continue
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
'''
parameter_candidates = [
  {'criterion': ['gini', 'entropy'], 'max_depth': [1, 3, 5, 7, 9, None], 
   'max_features': ['auto', 'log2', None], 
   'min_samples_leaf': [1, 3, 5], 'min_samples_split': [2, 5, 8],
   'bootstrap': [True, False]}
]

clf = GridSearchCV(estimator=RandomForestClassifier(), 
                   param_grid=parameter_candidates, n_jobs=-1, scoring='f1', cv=5)
clf.fit(train, train_ans.ravel())

# Print out the results 
print('Best score for training data:', clf.best_score_)
print('Best `criterion`:',clf.best_estimator_.criterion)
print('Best `max_depth`:',clf.best_estimator_.max_depth)
print('Best max_features:',clf.best_estimator_.max_features)
print('Best `min_samples_leaf`:',clf.best_estimator_.min_samples_leaf)
print('Best `min_samples_split`:',clf.best_estimator_.min_samples_split)
print('Best `bootstrap`:',clf.best_estimator_.bootstrap)

'''
clf = AdaBoostClassifier(
        tree.DecisionTreeClassifier(class_weight = {0:1, 1:10}, min_samples_split=10, 
                                    ),
        n_estimators = 40, learning_rate = 0.05)

clf.fit(train, train_ans.ravel())
pre_ans = clf.predict(test)


accuracy = metrics.accuracy_score(test_ans, pre_ans)
print(accuracy)

print(metrics.classification_report(test_ans, pre_ans))