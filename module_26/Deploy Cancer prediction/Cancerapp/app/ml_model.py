from joblib import load
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


def model_prediction(rm, tm, cm, cnm, cpm, sm, ts, ps, rw, tw, cw, cpw, sw):
    cols = ['radius_mean', 'texture_mean', 'compactness_mean', 'concavity_mean',
            'concave points_mean', 'symmetry_mean', 'texture_se', 'perimeter_se',
            'radius_worst', 'texture_worst', 'concavity_worst',
            'concave points_worst', 'symmetry_worst']

    model = load('/Users/fadee/PycharmProjects/Cancerapp/app/static/model_c.joblib')

    encoder = LabelEncoder()
    encoder.classes_ = np.load('/Users/fadee/PycharmProjects/Cancerapp/app/static/classes_c.npy', allow_pickle=True)

    df = pd.DataFrame([[rm, tm, cm, cnm, cpm, sm, ts, ps, rw, tw, cw, cpw, sw]], columns=cols)

    if model.predict(df)[0] == 0:
        return 'Benign'
    else:
        return 'Malignant'

