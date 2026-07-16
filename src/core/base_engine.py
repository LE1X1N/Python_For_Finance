from abc import ABC, abstractmethod


class BaseStockEngine(ABC):
    
    def __init__(self):
        super().__init__()
    
    @abstractmethod
    def get_real_time_quote(self, stock_code):
        pass