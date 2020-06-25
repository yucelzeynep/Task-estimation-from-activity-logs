#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 28 08:35:29 2019

@author: florianpgn


Basically this function runs a classifier multiple times and then outputs the 
average performance. 

"""
import numpy as np
import matplotlib.pyplot as plt
import re
import params

from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.utils.multiclass import unique_labels
#from imblearn.over_sampling import SMOTE
from collections import Counter

le = preprocessing.LabelEncoder()

def runMultiple(clf, datalog, name, n_iter=10):
    """
    This function runs the classifier clf as many times as n_iter and saves the 
    averaged confusion matrix into a txt file
    """

    precisions = []
    confs = 0
    for i in range(n_iter):
        """
        SVM management for the grid search
        
        Note that we GridSearch the hyper-parameters of the SVM only for the 
        first run and then keep the best values for all the other runs. For 
        that reason, I had to also modify 'runClassifierGS' (GS stands 
        for GridSearch). 

        """
        if name == "SVM" and i == 0:
            p, c, labels, gs_params = runClassifierGS(clf, datalog, name)
            clf = SVC(C = gs_params[('C')], gamma = gs_params[('gamma')])
                
        else:
            p, c, labels = runClassifier(clf, datalog, name)
        precisions.append(p)
        if i == 0:
            confs = c
        else:
            confs += c
            
    # careful that it does not overwrite but it appends
    f = open("classifiers_results.txt", "a+") 
    f.write('-----------{}----------- \n'.format(name))
    f.write('Tasks --> {}\n'.format(' - '.join(labels)))
    precision = round(np.sum(precisions)/len(precisions), 4)
    f.write('Score: {}\n'.format(precision))
    
    for i in range(len(confs)):
        for j in range(len(confs[i])):
            f.write(str(confs[i,j])+'\t')
        f.write('\n')
    f.write('\n')
    
    confs = np.array(confs)/np.nansum(confs, axis=1)[:,None]
    for i in range(len(confs)):
        for j in range(len(confs[i])):
            f.write(str(round(confs[i,j],4))+'\t')
        f.write('\n')
    f.write('\n\n')
                
    f.close()

def kNN(datalog, multi=False):
    """
    kNN
    """
    clf = KNeighborsClassifier(3)
    if multi:
        runMultiple(clf, datalog, "kNN")
    else:
        runClassifier(clf, datalog, "kNN")
    
def randomForest(datalog, multi=False):
    """
    RandomForestClassifier
    """
    clf = RandomForestClassifier(max_depth=5, n_estimators=100, max_features=1)
    if multi:
        runMultiple(clf, datalog, "Random Forest")
    else:
        runClassifier(clf, datalog, "Random Forest")
    
def svm(datalog, multi=False):
    """
    SVM classification
    """
    clf = SVC(gamma='scale')

    if multi:
        runMultiple(clf, datalog, "SVM")
    else:
        runClassifierGS(clf, datalog, "SVM")
        
def testAndPrintScores(clfName, clf, X_test, y_test):
    """
    This function first tests the classifier and then reports results by printing 
    them on console and also plotting confusion matrix
    """
    print("------------------------ ", clfName, " ------------------------")
    score = clf.score(X_test, y_test)
    print("Score : ", score)
    y_pred = clf.predict(X_test)

    conf_mat, labels = plotConfusionMatrix(y_test, y_pred)
    return score, conf_mat, labels

def runClassifier(clf, datalog, clfName):
    """
    Use GS version, if you do also the GridSearch
    """
    X_train, X_test, y_train, y_test = getTrainTest(datalog)
    clf.fit(X_train, y_train)  
    
    score, conf_mat, labels = testAndPrintScores(clfName, clf, X_test, y_test)
    return (score, conf_mat, labels)

def runClassifierGS(clf, datalog, clfName):
    """
    Train and test together with grid search
    """
    X_train, X_test, y_train, y_test = getTrainTest(datalog)
    param_grid = {'C':[1,10,100,1000], 'gamma':[1,0.1,0.001,0.0001]}
    grid = GridSearchCV(SVC(), param_grid, refit = True)
    grid.fit(X_train,y_train)
    
    score, conf_mat, labels = testAndPrintScores(clfName, grid, X_test, y_test)
    return (score, conf_mat, labels, grid.best_params_)


def getTrainTest(datalog):
    """
    Retain the descriptors that we are interested in or keep all
    """
    if params.USE_REL_DESC:
        subdict = {k: datalog[k] for k in (params.WINDOW_STR,
               params.EXE_STR)}
        
    else:
        subdict = {k: datalog[k] for k in (params.WINDOW_STR,
               params.EXE_STR,
               params.NB_LCLICK_STR,
               params.NB_RCLICK_STR,
               params.NB_KSTROKES_STR,
               params.DURATION_STR)}
    
    """
    Transform the data into numeric values
    """
    datalog_copy = datalog.copy()
    dataEncoding(datalog_copy, subdict)
    
    """
    Building feature vector and ground_truth vector
    """
    X = []
    y = []
    #For each instance in the database
    for i in range(len(datalog_copy[params.HAND_TASK_STR])):
        y.append(datalog_copy[params.HAND_TASK_STR][i])        
        
        features = []
        for k in subdict.keys():
            features.append(subdict[k][i])
        
        """
        The feature list contains both int and lists. Here, we flatten the list
        We also cast into float
        """
        features = [float(value) for feature in features for value in (feature if isinstance(feature, list) else (feature,))]
        X.append(features)
    
    X_resampled, y_resampled = SMOTE().fit_resample(X, y)
    print(sorted(Counter(y_resampled).items()))
    
    """
    Splitting into train/test
    
    Obviousy, we don't want to test the classifier with the data generated by 
    SMOTE. Therefore, we first take a random subset for the test set. Then for 
    the train set, we take a subset in the resampled set. Thus data crossing is 
    possible between the 2 subsets
    """
    _, X_test, _, y_test =  train_test_split(X, y, test_size=1-params.TRAINSET_SIZE)
    X_train, _, y_train, _ = train_test_split(X_resampled, y_resampled, test_size=1-params.TRAINSET_SIZE)
    return (X_train, X_test, y_train, y_test)
    
def dataEncoding(datalog, subdict):
    """
    Remove .exe extension in application names
    """
    for index, elem in enumerate(subdict[params.EXE_STR]):
        subdict[params.EXE_STR][index] = re.sub(r".exe", "", elem)
    
    """
    Encoding exe names with vectors (i.e. associate a vector with each exe name)
    """
    lb = preprocessing.LabelBinarizer()
    lb.fit(subdict[params.EXE_STR]) 
    subdict[params.EXE_STR] = encodeList(lb, subdict[params.EXE_STR])
    lb = preprocessing.LabelBinarizer()
    lb.fit(subdict[params.WINDOW_STR]) # here, we associate a vector to each exe name   
    subdict[params.WINDOW_STR] = encodeList(lb, subdict[params.WINDOW_STR])
    
    """
    Building a list that contains all the possible annotations
    """
    le.fit(params.TASKS) #Associate an id to each label
    
    """
    Encoding task names
    """
    datalog[params.HAND_TASK_STR] = encodeList(le, datalog[params.HAND_TASK_STR])
    

    
def encodeList(encoder, strings):
    """
    Translate strings into int (Encoder) or int vector (Binarizer)
    """
    return encoder.transform(strings).tolist()


def plotConfusionMatrix(y_true, y_pred, normalize=False, cmap=plt.cm.Blues):
    """
    This function computes the confusion matrix and, if desired, it also 
    normalizes it. Here, by normalize I mean scaling each row to 1.
    
    It also displays it as a figure, not a very crucial objective but it is 
    nevertheless handy, if you do many tests. 
    """
    if normalize:
        title = 'Normalized confusion matrix'
    else:
        title = 'Confusion matrix, without normalization'

    """
    Compute the confusion matrix
    """
    cm = confusion_matrix(y_true, y_pred)
    classe_ids = le.transform(le.classes_) # Only use the labels that appear in the data
    classes = classe_ids[unique_labels(y_true, y_pred)]
    
    """
    Print the confusion matrix on console
    """
    print('Confusion matrix, without normalization')
    print(cm)
    print("Normalized confusion matrix")
    cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    print(cm_norm)
    
    """
    Plot the confusion matrix (quite tedious)
    """
    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()

    #Display the labels associated to each ID
    for n, classe in enumerate(le.classes_):
        print(n,'-->',[classe])
    
    labels = [le.classes_[index] for index in classes]
    plt.show()
    return cm, labels

