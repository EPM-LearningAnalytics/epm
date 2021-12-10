#!/usr/bin/env python
# coding: utf-8

"""
This module preprocess the log activity data
"""


# load libraries
import os, sys
sys.path.insert(0, os.path.abspath('../data_prep/'))
import glob
import pandas as pd
import log_prep as lp
import grades_prep as gp


from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score
from sklearn.metrics import accuracy_score

import pandas as pd

def subset_important_features(data_list, num_of_features, option):
    """
    parameters:
    datasets: dataframe with 
    num_of_features
    option:
    """
    if option == 'different':
        important_features = []
        for i, session in enumerate(data_list):
            if i == 0: continue
            X = session.drop(columns=['ID', 'Y'])
            y = session['Y']
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)
            clf = ExtraTreesClassifier(n_estimators=50)
            clf = clf.fit(X, y)
            feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
            features = feat_importances.nlargest(num_of_features).index[0:num_of_features]
            important_features.append(pd.DataFrame(features, columns = ['session'+str(i+1)]))
            important_features[i-1].loc[num_of_features] = ['Y']
            important_features[i-1].loc[num_of_features+1] = ['ID']
            
        for i, session in enumerate(data_list):
            if i == 0: continue
            data_list[i] = session[important_features[i-1]['session'+str(i+1)]] 

        return data_list

    elif option == 'common':
        num = 0
        j = 10
        while num < num_of_features-1:
            important_features = []
            for i, session in enumerate(data_list):
                if i == 0: continue
                X = session.drop(columns=['ID', 'Y'])
                y = session['Y']
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)
                clf = ExtraTreesClassifier(n_estimators=50)
                clf = clf.fit(X, y)
                feat_importances = pd.Series(clf.feature_importances_, index=X.columns)
                features = feat_importances.nlargest(j).index[0:j]
                important_features.append(features)
            common_features = list(set.intersection(*map(set, important_features)))
            num = len(common_features)
            j += 1            
            
        if len(common_features) > num_of_features-1:
            common_features = common_features[0:num_of_features]
            for i, session in enumerate(data_list):
                if i == 0: continue
                common_features.append('ID')
                common_features.append('MID'+str(i+1)) 
                data_list[i] = session[common_features]
                del common_features[-2:]
            
        if len(common_features) == num_of_features-1:
            
            for i, session in enumerate(data_list):
                if i == 0: continue
                common_features.append('ID')
                common_features.append('MID'+str(i+1))
                data_list[i] = session[common_features]
                del common_features[-2:]
        
        return data_list            
            


def machine_learning_model(data_list, ml_model):
    for i, session in enumerate(data_list):
        if i == 0: continue
        X = session.drop(columns=['Y'])
        y = session['Y']
        if ml_model == 'KNN':
            cKNN = KNeighborsClassifier(n_neighbors = 10, metric = 'minkowski', p = 2).fit(X, y)
            predict = cKNN.predict(X)
            session = session.assign(Predicted_Y = predict)
        elif ml_model == 'DT':
            cDT = DecisionTreeClassifier(criterion = 'entropy', random_state = 0).fit(X, y)
            predict = cDT.predict(X)
            session = session.assign(Predicted_Y = predict)
        elif ml_model == 'RF':
            cRF = RandomForestClassifier(n_estimators = 10, criterion ='entropy', random_state = 0).fit(X, y)
            predict = cRF.predict(X)
            session = session.assign(Predicted_Y = predict)
        elif ml_model == 'NB':
            cNB = GaussianNB().fit(X, y)
            predict = cNB.predict(X)
            session = session.assign(Predicted_Y = predict)
        elif ml_model == 'LR':
            cLR = LogisticRegression(solver = 'liblinear', random_state = 0).fit(X, y)
            predict = cLR.predict(X)
            session = session.assign(Predicted_Y = predict)
        elif model == 'SVC':
            cSVM = SVC(kernel = 'rbf', random_state=0).fit(X, y)
            predict = cSVM.predict(X)
            session = session.assign(Predicted_Y = predict)
        data_list[i]=session
    return data_list

# K-Means considering all the previous sessions
Def:
    for i in range(5):
        #data_new =  scaled_var_list[i].drop(columns = 'ID')
        cols = [f'MID{n+2}' for n in range(i+1)]
        cols.append('ID')
        data_new = pd.merge(scaled_var_list[i], grades[cols], how='inner', on=['ID'])
        Mid_cols = [col for col in  data_new.columns.values if col.startswith('MID')]
        data_new['MID_Mean'] = data_new[Mid_cols].mean(axis = 1)
        
        features = ['KS_Deeds','MID_Mean']
        data_new = data_new[features]
        wcss=[]
        for clu_n in range(1,11): 
            kmeans = KMeans(n_clusters=clu_n, init ='k-means++', max_iter=300,  n_init=10,random_state=0 )
            kmeans.fit(data_new)
            #kmeans algorithm fits to the X dataset
            wcss.append(kmeans.inertia_)
        
        plt.figure(figsize=(10, 4))
        plt.subplot(121)
        #kmeans inertia_ attribute is:  Sum of squared distances of samples #to their closest cluster center.
        #4.Plot the elbow graph
        plt.plot(range(1,11),wcss,'rP-')
        plt.title('The Elbow Method Graph')
        plt.xlabel('Number of clusters')
        plt.ylabel('WCSS')
       
def main():
    A = read_file()
    A = feature_manipulation(A)
    save_data(A)
    return 0


if __name__ == '__main__':
    main()