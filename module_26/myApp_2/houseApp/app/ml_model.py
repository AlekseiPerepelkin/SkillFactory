from joblib import load
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


def model_prediction(city, floor, area, rooms):
    model = load('/Users/ymochalova/Desktop/skillfactory/деплой/houseApp/app/static/model.joblib')

    encoder = LabelEncoder()
    encoder.classes_ = np.load('/Users/ymochalova/Desktop/skillfactory/деплой/houseApp/app/static/classes.npy', allow_pickle=True)

    df = pd.DataFrame([[city, floor, area, rooms]], columns=['city', 'floorNumber', 'totalArea', 'rooms'])
    df['floorsTotal'] = 14.75
    df.city = encoder.transform(df.city)

    return round(model.predict(df)[0])

