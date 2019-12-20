import scikitplot as skplt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.externals import joblib


def cpmp_qwk(a1, a2, max_rat=3) -> float:
    """
    A ultra fast implementation of Quadratic Weighted Kappa (QWK)
    Source: https://www.kaggle.com/c/data-science-bowl-2019/discussion/114133

    :param a1: The ground truth labels
    :param a2: The predicted labels
    :param max_rat: The maximum target value

    return: A floating point number with the QWK score
    """
    assert (len(a1) == len(a2))
    a1 = np.asarray(a1, dtype=int)
    a2 = np.asarray(a2, dtype=int)

    hist1 = np.zeros((max_rat + 1,))
    hist2 = np.zeros((max_rat + 1,))

    o = 0
    for k in range(a1.shape[0]):
        i, j = a1[k], a2[k]
        hist1[i] += 1
        hist2[j] += 1
        o += (i - j) * (i - j)

    e = 0
    for i in range(max_rat + 1):
        for j in range(max_rat + 1):
            e += hist1[i] * hist2[j] * (i - j) * (i - j)

    e = e / a1.shape[0]

    return 1 - o / e


def prediction(model, test_set):
    X_test = test_set.drop(columns='accuracy_group').values
    y_test = test_set['accuracy_group'].values

    y_pred = model.predict(X_test)
    label_pred = [y_pred[i].argmax() for i in range(len(y_pred))]
    score = cpmp_qwk(y_test, label_pred)
    print('Quadratic Kappa Weighted score: {}'.format(score))
    # if kwargs.get("verbose_eval"):
    #             print("\n" + "="*50 + "\n")

    return y_pred, score


def aucplot(test_set, y_pred, folder_name, file_name):
    y_true = test_set['accuracy_group'].values
    y_probas = y_pred
    skplt.metrics.plot_roc_curve(y_true, y_probas)
    full_file_name = 'static/temp/' + folder_name + '/' + file_name + '.png'
    plt.tight_layout()
    plt.savefig(full_file_name)


def featureImportance(model, train_joined):
    featureRank = model.feature_importance()
    featureName = train_joined.columns[:-1]
    featureDict = dict(zip(featureName, featureRank))
    import heapq
    top10 = heapq.nlargest(20, featureDict, key=featureDict.get)
    top10_value = [featureDict[i] for i in top10]
    top10.reverse()
    plt.rcParams.update({'font.size': 12})
    fig = plt.figure(figsize=(12, 10))
    se = pd.Series(data=top10_value).sort_values(ascending=True)
    se.index = top10
    se.plot.barh()
    plt.title("Feature importance")
    plt.xticks(rotation=0)
    plt.show()


def curvePlot(evals_result):
    train_logloss = evals_result['training']['multi_logloss']
    valid_logloss = evals_result['valid_1']['multi_logloss']
    plt.plot(train_logloss)
    plt.plot(valid_logloss)
    plt.legend(['train_logloss', 'valid_logloss'])
    plt.title('Loss curve')
    plt.xlabel('Iteration')
    plt.ylabel('logloss')
    plt.show()


def predict(test_num, model_num, folder_name, name):
    train_joined = pd.read_csv('src/files/train_joined.csv', index_col=0)

    # The test set for model3 (model_fp) is different
    if model_num == 3:
        suffix = '_fp'
    else:
        suffix = ''

    test_name = 'test' + str(test_num) + suffix + '.csv'
    test_set = pd.read_csv('src/files/' + test_name, index_col=0)
    model_name = 'model_v' + str(model_num) + '.model'
    model = joblib.load('src/files/' + model_name)

    # Prediction
    y_pred, score = prediction(model, test_set)

    # AUC plot
    aucplot(test_set, y_pred, folder_name, name)
    return score

    # loss plot
    # curvePlot(evals_result)

    # feature importance
    # featureImportance(model, train_joined, folder_name, name)
