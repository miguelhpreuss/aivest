import numpy as np

BANKS = ['BBDC4.SA', 'ITUB4.SA', 'BBDC3.SA', 'BBAS3.SA', 'BRIV4.SA', 'BAZA3.SA',
            'ABCB4.SA', 'BRIV3.SA', 
            'BGIP4.SA', 'BPAN4.SA', 'SANB11.SA', 'BRSR5.SA', 'BRSR6.SA', 'BNBR3.SA',
            'BMIN4.SA', 'BEES4.SA', 'PINE4.SA', 'MERC4.SA',
            'ITUB3.SA', 'USBC34.SA', 'BEES3.SA', 'BMEB3.SA']

def prepare_data_for_prediction(dataset, start, end, window):
    X = []
    start = start + window

    if start != end:
        for i in range(start, end):
            print("entrou")
            indicesx = range(i-window, i)
            X.append(np.reshape(dataset[indicesx], (window, 1)))
    else:
        for i in range(1):
            print("entrou")
            indicesx = range(i-window, i)
            X.append(np.reshape(dataset[indicesx], (window, 1)))
    return np.array(X)