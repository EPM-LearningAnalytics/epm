import os
import pickle

def review_alert(id):
    res = [0]*7
    for num in [2, 3, 4, 5, 6]:
        data = 'data_session_' + str(num)
        data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_prep', 'pickles', data)
        df = pickle.load(open(data_path, 'rb'))
        features = df.loc[df['ID'] == int(id)].drop(columns=['Y', 'ID'])
        if len(features) == 0:
            continue
        
        model = 'log_regression_' + str(num)
        model_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'data_prep', 'pickles', model)
        loaded_model = pickle.load(open(model_path, 'rb'))
        res[num] = loaded_model.predict(features)[0]
    return res