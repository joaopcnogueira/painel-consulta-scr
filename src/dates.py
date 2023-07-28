import pandas as pd
from datetime import datetime

def get_current_data_base():
    now = datetime.now().date()
    previous = now - pd.DateOffset(months=1)
    previous = previous.strftime("%m/%Y")
    month = previous.split("/")[0]
    year = previous.split("/")[1]
    data_base = month + "/" + year
    return data_base