from src.engines.yahoo_engine import YahooEngine


engine = YahooEngine()


stock_code = "AAPL"

print(engine.get_real_time_quote(stock_code))