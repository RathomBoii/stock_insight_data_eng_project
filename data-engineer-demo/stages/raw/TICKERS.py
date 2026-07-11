# Use Final as a static type check before a runtime
from types import MappingProxyType


TICKERS = MappingProxyType({
    "Cloud Provider": {
        "US": {"MSFT": "MSFT", "AMZN": "AMZN", "GOOGL": "GOOGL"},
        "China": {"BABA": "BABA", "TCEHY": "TCEHY", "KC": "KC"},
    },
    "SaaS": {
        "US": {"CRM": "CRM", "NOW": "NOW", "SNOW": "SNOW"},
        "China": {
            "Kingdee": "0268.HK",
            "Chinasoft": "0354.HK",
            "Weimob": "2013.HK",
        },
    },
    "Security": {
        "US": {"CRWD": "CRWD", "PANW": "PANW", "FTNT": "FTNT"},
        "China": {
            "Sangfor": "300454.SZ",
            "Venustech": "002439.SZ",
            "NSFOCUS": "300369.SZ",
        },
    },
})