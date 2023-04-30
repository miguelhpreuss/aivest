import yfinance as yf
import json

# define o ticker da Petrobras
ticker = "ABEV3.SA"

# extrai o histórico de preços
petrobras = yf.download(ticker, period="max")

# converte o DataFrame em um dicionário com a estrutura desejada
data = []
for index, row in petrobras.iterrows():
    item = {
        "date": index.strftime("%Y-%m-%d"),
        "open": round(row["Open"], 2),
        "high": round(row["High"], 2),
        "low": round(row["Low"], 2),
        "close": round(row["Close"], 2),
        "volume_ltc": round(row["Volume"] / 1000, 2),
        "volume_brl": round(row["Volume"] * row["Close"], 2),
    }
    data.append(item)

# converte o dicionário em um JSON e exibe na tela
json_data = json.dumps(data)
with open(ticker + ".json", "w") as f:
    f.write(json_data)
