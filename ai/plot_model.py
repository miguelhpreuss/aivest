import pandas as pd
import pickle
import pathlib
import tensorflow as tf
from acoes import get_data
import numpy as np
import matplotlib.pyplot as plt


def custom_ts_univariate_data_prep(dataset, start, end, window, horizon):
  X = []
  y = []
  start = start + window
  if end is None:
    end = len(dataset) - horizon
  for i in range(start, end):
    indicesx = range(i-window, i)
    X.append(np.reshape(dataset[indicesx], (window, 1)))
    indicesy = range(i,i+horizon)
    y.append(dataset[indicesy])
  return np.array(X), np.array(y)


if __name__ == "__main__":
    parent_path = pathlib.Path(__file__).parents[1]
    min_max_scaler_path = pathlib.Path(parent_path, "datasets", "01_raw", "min_max_scaler.pkl")
    lstm_model_path = pathlib.Path(parent_path, "lstm_encoder_decoder_model")
    min_max_scaler = pickle.load(open(min_max_scaler_path, "rb"))
    lstm = tf.keras.models.load_model(lstm_model_path)

    df = get_data('ITUB4.SA', period="max")
    df = df["Close"]
    df.dropna(inplace=True)
    feature_array = min_max_scaler.transform(df.to_numpy().reshape(-1,1))
    x_test_2, y_test_2 = custom_ts_univariate_data_prep(feature_array, 5520, len(feature_array)-5, 60, 5)
    predicted = lstm.predict(x_test_2)


    fig, ax = plt.subplots()
    x_test_2 = x_test_2[-1].reshape(1, -1)
    y_test_2 = y_test_2[-1].reshape(1, -1)
    predicted = predicted[-1].reshape(1, -1)
   
    print(y_test_2)
    print(x_test_2)
    print(predicted)
    x_test_2 = min_max_scaler.inverse_transform(x_test_2)[0]
    preds = min_max_scaler.inverse_transform(predicted)[0]
    y_test_2 = min_max_scaler.inverse_transform(y_test_2)[0]
    
    print(x_test_2)
    print(y_test_2)
    print(preds)

    x_test_2 = x_test_2.tolist()
    preds = preds.tolist()
    y_test_2 = y_test_2.tolist()

    
    data = x_test_2 + y_test_2
    preds_data = x_test_2 + preds
    print(preds)
    ax.plot(preds_data, label="predicted")
    ax.plot(data, label="true")
    ax.legend()
    plt.show()    
