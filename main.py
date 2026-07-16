from src.engines.yahoo_engine import YahooEngine


engine = YahooEngine()


stock_code = "AAPL"

print(engine.get_price(stock_code))