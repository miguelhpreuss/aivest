import json

def stock(ticker):
    with open("./___data/" + ticker + ".SA.json", "r") as f:
        return json.load(f)    
    
