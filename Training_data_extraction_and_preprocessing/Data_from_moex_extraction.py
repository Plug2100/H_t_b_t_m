import requests
import apimoex
import pandas as pd
from typing import List, Optional
from datetime import datetime, timedelta
from abc import ABC, abstractmethod


class price_info_abs(ABC):
    @abstractmethod
    def extract_price_info(self):
        pass


# Realisation example
class price_info(price_info_abs):

    def extract_price_info(self, securities: List[str], start: Optional[str] = None, end: Optional[str] = None, frequency: Optional[int] = None):
        if start is None:
            start = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        if end is None:
            end = datetime.today().strftime('%Y-%m-%d')
        if frequency  is None:
            frequency = 2

        vec_of_the_prices = []

        for i in securities:
            with requests.Session() as session:
                data = apimoex.get_board_history(session, i, start, end, (('BOARDID', 'TRADEDATE', 'OPEN', 'CLOSE', 'HIGH', 'LOW')))

                open = [entry['OPEN'] for j, entry in enumerate(data) if j % frequency == 0]
                close = [entry['CLOSE'] for j, entry in enumerate(data) if j % frequency == 0]
                high = [entry['HIGH'] for j, entry in enumerate(data) if j % frequency == 0]
                low = [entry['LOW'] for j, entry in enumerate(data) if j % frequency == 0]

                vec_of_the_prices.append([open, close, high, low])
        
        return(vec_of_the_prices)
               
                
# Example
print(price_info().extract_price_info(['SNGSP', 'OZON']))