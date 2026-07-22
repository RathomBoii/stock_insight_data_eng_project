from datetime import datetime, timedelta

"""
data freshness formula = ingestion timestamp - event (trade) timestamp
"""


def calculate_data_freshness(now: datetime, trade_date: datetime) -> timedelta:
    return now - trade_date
