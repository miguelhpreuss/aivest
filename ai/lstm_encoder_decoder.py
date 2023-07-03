
from keras.layers import Input
from keras.layers import LSTM
from acoes import get_data
import numpy as np
from keras.models import Sequential
import tensorflow as tf
from keras import layers
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import pandas as pd
from keras import backend as K
import pickle
from pathlib import Path


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
    K.set_value(enco_deco.optimizer.learning_rate, 0.00001)
    return enco_deco

if __name__ == "__main__":
    banks = ['BBDC4.SA', 'ITUB4.SA', 'BBDC3.SA', 'BBAS3.SA', 'BRIV4.SA', 'BAZA3.SA',
            'ABCB4.SA', 'BRIV3.SA', 
            'BGIP4.SA', 'BPAN4.SA', 'SANB11.SA', 'BRSR5.SA', 'BRSR6.SA', 'BNBR3.SA',
            'BMIN4.SA', 'BEES4.SA', 'PINE4.SA', 'MERC4.SA',
            'ITUB3.SA', 'USBC34.SA', 'BEES3.SA', 'BMEB3.SA']
     
    for idx, bank in enumerate(banks):
        df = get_data(bank, period="max")
        df = df["Close"]
        print(f"""{bank} & {round(df.min(),1)} & {round(df.max(),1)} \\\\ \\hline""")
        if idx == 0:
           min_max_scaler_array = df
        else:
           min_max_scaler_array = pd.concat([min_max_scaler_array, df], axis=0)

    print(min_max_scaler_array.max(), min_max_scaler_array.min())
    min_max_scaler_array.dropna(inplace=True)
    min_max_scaler = MinMaxScaler()
    min_max_scaler.fit(min_max_scaler_array.to_numpy().reshape(-1,1))
    path = Path("datasets", "01_raw", "min_max_scaler.pkl")
    pickle.dump(min_max_scaler, open(path, "wb"))

    
    for idx, bank in enumerate(banks):
        df = get_data(bank, period="max")
        df = df["Close"]
        df.dropna(inplace=True)
        feature_array = min_max_scaler.transform(df.to_numpy().reshape(-1,1))
        x_train_bank, y_train_bank = custom_ts_univariate_data_prep(feature_array, 0, int(len(feature_array)*0.8), 60, 5)
        x_test_bank, y_test_bank = custom_ts_univariate_data_prep(feature_array, int(len(feature_array)*0.8), len(feature_array)-5, 60, 5)
        if idx==0:
           x_train = x_train_bank
           y_train = y_train_bank
           x_test = x_test_bank
           y_test = y_test_bank

        
        x_train = np.append(x_train, x_train_bank, axis=0)
        y_train = np.append(y_train, y_train_bank, axis=0)
        x_test = np.append(x_test, x_test_bank, axis=0)
        y_test = np.append(y_test, y_test_bank, axis=0)



    BATCH_SIZE = 256
    BUFFER_SIZE = 150
    print(x_train.shape)
    print(x_test.shape)
    train_univariate = tf.data.Dataset.from_tensor_slices((x_train, y_train))
    train_univariate = train_univariate.cache().shuffle(BUFFER_SIZE).batch(BATCH_SIZE).repeat()
    val_univariate = tf.data.Dataset.from_tensor_slices((x_test, y_test))
    val_univariate = val_univariate.batch(BATCH_SIZE).repeat()


    lstm = create_model(x_train, y_train)
    lstm.fit(x_train, y_train, epochs=300,steps_per_epoch=100,validation_data=val_univariate, validation_steps=50,verbose =1)
    lstm.save("lstm_encoder_decoder_model")

    x_test_2, y_test_2 = custom_ts_univariate_data_prep(feature_array, 5500, 5531, 60, 5)
    predicted = lstm.predict(x_test_2)
    fig, ax = plt.subplots()
    
    x_test_2 = min_max_scaler.inverse_transform(x_test_2.reshape(1,-1)[0].reshape(-1,1))
    preds = min_max_scaler.inverse_transform(predicted.reshape(1, -1)[0].reshape(-1,1))
    y_test_2 = min_max_scaler.inverse_transform(y_test_2.reshape(1, -1)[0].reshape(-1,1))

    print(x_test_2)
    data = x_test_2.extend(y_test_2)
    ax.plot(preds, label="predicted")
    ax.plot(data, label="true")
    ax.legend()
    plt.show()
