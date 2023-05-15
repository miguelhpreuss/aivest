import pandas as pd
import pathlib
import pandasgui
from acoes import Stock
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from matplotlib import pyplot as plt

def find_number_of_industries_in_each_sector(df: pd.DataFrame) -> list:
    sectors = df['industry'].unique()
    num_of_industries_in_sector = [(sector, len(df[df["industry"] == sector])) for sector in sectors]
    return num_of_industries_in_sector


def get_companies_in_sector(df: pd.DataFrame, sector: str) -> list:
    companies_in_sector = df[df["industry"] == sector]
    return companies_in_sector['symbol'].to_list()


def get_data_from_companies(companies: list[str]) -> list[Stock]:
    stocks = []
    for company in companies:
        stock = Stock(company)
        stock.get_data(period='max', interval='1d')
        stocks.append(stock)
    return stocks


def add_indicators_to_stocks(stocks: list[Stock]) -> list[Stock]:
    for stock in stocks:
        data = stock.get_data
        stock.data["SMA_14"] = stock.SMA(period=14)
        stock.data["SMA_26"] = stock.SMA(period=26)
        stock.data["EMA_14"] = stock.EMA(period=14)
        stock.data["EMA_26"] = stock.EMA(period=26)
        stock.data["MACD"] = stock.MACD()[0]
        stock.data["RSI_14"] = stock.RSI()
        stock.data["RSI_26"] = stock.RSI(period=26)
    indicator_name_list = ['SMA_14', 'SMA_26', 'EMA_14', 'EMA_26',
                                'MACD', 'RSI_14', 'RSI_26']
    return stocks, indicator_name_list


# def remove_outliers(stocks: list[Stock], indicator_name_list: list[str]) -> list[Stock]:
#     for stock in stocks:
#         for indicator in indicator_name_list:
#             stock.data.loc[:,indicator] = stats.winsorize(stock.data.loc[:,indicator], limits = [0.1,0.1])
#     return stocks
        
        
def create_stocks_dataset(stocks: list[Stock], column="Close", observing_times=26, prediction_times=5):
    for stock in stocks:
        for observation in range(1, observing_times, 1):
            stock.data[f"{column}_-{observation}"] = stock.data[column].shift(periods= observation, axis=0)
        for prediction in range(1, prediction_times, 1):
            stock.data[f"{column}_{prediction}"] = stock.data[column].shift(periods= -abs(prediction), axis=0)
    return stocks

def join_dataset(stocks):
    dfs = [stock.data for stock in stocks]
    df = pd.concat(dfs)
    return df

    




            
            

if __name__ == "__main__":
    stock = Stock("PETR4.SA")
    stock.get_data(period="max")
    stocks = [stock]
    stocks, indicator_names_list = add_indicators_to_stocks(stocks)
    stocks = create_stocks_dataset(stocks)
    df = join_dataset(stocks)
    df = df.dropna()
    targets = ["Close_1", "Close_2", "Close_3", "Close_4"]
    y = df[targets]
    x = df.drop(targets, axis=1)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    rf = RandomForestRegressor()
    rf.fit(x_train, y_train)
    predictions = rf.predict(x_test)
    plt.plot(predictions[0])
    plt.plot(y_test.values[0])

    plt.show()



