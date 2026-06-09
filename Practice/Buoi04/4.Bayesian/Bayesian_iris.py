# chen thu vien
import pandas as pd
import numpy as np
import os

# load du lieu va DT
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.model_selection import train_test_split 

from sklearn.naive_bayes import GaussianNB

# tach nhan va goi mo hinh
X,y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

gnb = GaussianNB() 
gnb.fit(X_train, y_train)

