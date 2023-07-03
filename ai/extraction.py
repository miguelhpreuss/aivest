import pandas as pd
import pathlib

def find_number_of_industries_in_each_sector(df: pd.DataFrame) -> list:
    sectors = df['industry'].unique()
    num_of_industries_in_sector = [(sector, len(df[df["industry"] == sector])) for sector in sectors]
    return num_of_industries_in_sector


def get_companies_in_sector(df: pd.DataFrame, sector: str) -> list:
    companies_in_sector = df[df["industry"] == sector]
    return companies_in_sector['symbol'].to_list()



def add_indicators_to_stocks(stocks):
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
        
def join_dataset(stocks):
    dfs = [stock.data for stock in stocks]
    df = pd.concat(dfs)
    return df

    
if __name__ == "__main__":
    parent = pathlib.Path(__file__).parents[1]
    file = pathlib.Path(parent, "datasets", "01_raw", "all_stocks_info3.csv")
    df = pd.read_csv(file)
    sector = find_number_of_industries_in_each_sector(df)
    res = get_companies_in_sector(df, 'Banks—Regional')
    print(res)



