import os
import pickle
import pandas as pd

def review_alert(id, feat_num):
    res = []
    models = ['KNN', 'DT', 'RF', 'NB', 'LR', 'SVC']
    columns = ['Session 2', 'Session 3', 'Session 4', 'Session 5', 'Session 6']
    for model_name in models:
        row = [0] * 5
        for session in range(2, 7):           
            data = 'session_' + str(session) + '_featnum_' + str(feat_num)
            data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_prep', 'pickles', 'features_and_outcome', data)
            df = pickle.load(open(data_path, 'rb'))
            features = df.loc[df['ID'] == int(id)].drop(columns=['Y', 'ID'])
            if len(features) == 0:
                continue

            model = str(model_name) + '_session_' + str(session) + '_featnum_' + str(feat_num)
            model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_prep', 'pickles', 'trained_models', model)
            loaded_model = pickle.load(open(model_path, 'rb'))
            row[session-2] = loaded_model.predict(features)[0]
        res.append(row)

    df = pd.DataFrame(res,
                      index=['K-Nearest Neighbors', 'Decision Tree', 'Random Forest', 'Baive Bayes', 'Log Regression', 'Support Vector Classfier'], 
                      columns=columns)
    return df