# -*- coding: utf-8 -*-

import numpy as np
import pandas
from sklearn import preprocessing, metrics
from sklearn.neural_network import MLPClassifier

DATA = pandas.read_csv('TraData.csv', dtype={'click': np.float64}).as_matrix()

for i in range(0, 12):  
    label_encoder = preprocessing.LabelEncoder()
    encode = label_encoder.fit_transform(DATA[:, i].astype(str))
    for j in range(0, len(encode)):
        encode[j] = float(encode[j])
    DATA[:, i] = encode

DATA = np.array(DATA, dtype='float')

train = DATA[0:861457 , 0:12]
train_ans = DATA[0:861457, 12:13]
test = DATA[861457:961457, 0:12]
test_ans = DATA[861457:961457, 12:13]

clf = MLPClassifier(solver='adam', alpha=1e-5,
                    hidden_layer_sizes=(4, 2), random_state=2, activation='relu')
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

accuracy = metrics.accuracy_score(test_ans, pre_ans)
print(accuracy)

print("pre:{}%  recall:{}%".format(int(get_cnt/pre_cnt*100), 
                                   int(get_cnt/true_cnt*100)))