from src import YahooEngine


engine = YahooEngine()


stock_code = "AAPL"

print(engine.get_real_time_quote(stock_code))