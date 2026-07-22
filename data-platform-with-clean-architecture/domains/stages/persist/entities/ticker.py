
class TickerInput:
    symbol: str
    name: str
    industry: str
    country: str
    delisted: bool

class Ticker: 
    def __init__(self, props: TickerInput):
        self._symbol = props.symbol
        self._name = props.name
        self._industry = props.industry
        self._country = props.country
        self._delisted = props.delisted
        
    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def name(self) -> str:
        return self._name

    @property
    def industry(self) -> str:
        return self._industry

    @property
    def country(self) -> str:
        return self._country

    @property
    def delisted(self) -> bool:
        return self._delisted
    