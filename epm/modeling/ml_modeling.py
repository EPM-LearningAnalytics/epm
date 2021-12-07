def getting_important_features(datasets, num_of_features):
    """
    parameters:
    datasets: dataframe with 
    num_of_features
    """
    # packages
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import ExtraTreesClassifier
    import pandas as pd

    # 
    important_features = []
    
    for i, session in enumerate(datasets):
        X = session.drop(columns=['ID', 'Y'])
        y = session['Y']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)
        clf = ExtraTreesClassifier(n_estimators=50)
        clf = clf.fit(X, y)
        feat_importances = (pd.Series(clf.feature_importances_, index=X.columns))
        important_features.append(pd.DataFrame(feat_importances.nlargest(num_of_features).index[0:num_of_features], columns = ['imp_features'+str(i)]))
        important_features[i].loc[num_of_features] = ['ID']

    # merge features and outcome (only top certain significant predictors)
    for i, features in enumerate(datasets):
        features = features[important_features[i]['imp_features' + str(i)]]
        datasets[i] = features.merge(outcome2[['ID', 'RES' + str(i+2)]], how='inner', on='ID')
        datasets[i] = datasets[i].rename(columns={'RES' + str(i+2): 'Y'})
    