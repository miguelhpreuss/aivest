
from keras.layers import Input
from keras.layers import LSTM
from acoes import Stock
import numpy as np
from keras.models import Sequential
import tensorflow as tf
from keras import layers
from sklearn.preprocessing import MinMaxScaler
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


def create_model(x_train_uni, y_train_uni):
    enco_deco = Sequential()

    # Encoder
    enco_deco.add(LSTM(100, input_shape=x_train_uni.shape[-2:], return_sequences=True))
    enco_deco.add(LSTM(units=50,return_sequences=True))
    enco_deco.add(LSTM(units=15))

    #feature vector
    enco_deco.add(layers.RepeatVector(y_train_uni.shape[1]))

    #decoder
    enco_deco.add(LSTM(units=100,return_sequences=True))
    enco_deco.add(LSTM(units=50,return_sequences=True))
    enco_deco.add(layers.TimeDistributed(tf.keras.layers.Dense(units=1)))
    enco_deco.compile(optimizer='adam', loss='mse')
    return enco_deco

if __name__ == "__main__":

    stock = Stock("PETR4.SA")
    df = stock.get_data(period="1mo", interval="1d",
                start=None, end=None, prepost=False, actions=True,
                auto_adjust=True, back_adjust=False, repair=False, keepna=False,
                proxy=None, rounding=False, timeout=10,
                debug=True, raise_errors=False)
    print(df)
    # df = df["Close"]
    # print(len(df.index))
    # min_max_scaler = MinMaxScaler()
    # feature_array = min_max_scaler.fit_transform(df.to_numpy().reshape(-1,1))
    # print(len(feature_array))
    
    # x_train, y_train = custom_ts_univariate_data_prep(feature_array, 0, 5000, 30, 5)
    # x_test, y_test = custom_ts_univariate_data_prep(feature_array, 5000, 5500, 30, 5)

    # BATCH_SIZE = 256
    # BUFFER_SIZE = 150

    # train_univariate = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    # train_univariate = train_univariate.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()
    # val_univariate = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    # val_univariate = val_univariate.batch(BATCH_SIZE).repeat()


    # # lstm = create_model(x_train, y_train)
    # # lstm.fit(x_train, y_train, epochs=150,steps_per_epoch=100,validation_data=val_univariate, validation_steps=50,verbose =1)

    # x_test_2, y_test_2 = custom_ts_univariate_data_prep(feature_array, 5500, 5531, 30, 5)
    # # predicted = lstm.predict(x_test_2)
    # plt.plot(predicted)
    # plt.plot(y_test_2)
    # plt.show()
