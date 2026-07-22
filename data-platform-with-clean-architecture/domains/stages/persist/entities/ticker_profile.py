import datetime

class TickerProfileInput:
    symbol: str
    snapshot_date: datetime.datetime          # fundamentals change daily — this stamps "as of when"
    ingestion_timestamp: datetime.datetime

    # Profile
    long_name: str | None
    sector: str | None
    industry: str | None
    country: str | None
    currency: str | None

    # Valuation
    market_cap: float | None
    trailing_pe: float | None
    forward_pe: float | None
    price_to_book: float | None
    enterprise_value: float | None

    # Growth & margins
    revenue_growth: float | None
    gross_margins: float | None
    operating_margins: float | None
    profit_margins: float | None
    total_revenue: float | None
    ebitda: float | None

    # Risk
    beta: float | None
    fifty_two_week_high: float | None
    fifty_two_week_low: float | None

    # Analyst view
    recommendation_key: str | None
    target_mean_price: float | None
    number_of_analyst_opinions: int | None

class TickerProfile:
    def __init__(self, props: TickerProfileInput):
        self._symbol = props.symbol
        self._snapshot_date = props.snapshot_date
        self._ingestion_timestamp = props.ingestion_timestamp

        # Profile
        self._long_name = props.long_name
        self._sector = props.sector
        self._industry = props.industry
        self._country = props.country
        self._currency = props.currency

        # Valuation
        self._market_cap = props.market_cap
        self._trailing_pe = props.trailing_pe
        self._forward_pe = props.forward_pe
        self._price_to_book = props.price_to_book
        self._enterprise_value = props.enterprise_value

        # Growth & margins
        self._revenue_growth = props.revenue_growth
        self._gross_margins = props.gross_margins
        self._operating_margins = props.operating_margins
        self._profit_margins = props.profit_margins
        self._total_revenue = props.total_revenue
        self._ebitda = props.ebitda

        # Risk
        self._beta = props.beta
        self._fifty_two_week_high = props.fifty_two_week_high
        self._fifty_two_week_low = props.fifty_two_week_low

        # Analyst view
        self._recommendation_key = props.recommendation_key
        self._target_mean_price = props.target_mean_price
        self._number_of_analyst_opinions = props.number_of_analyst_opinions

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def snapshot_date(self) -> datetime.datetime:
        return self._snapshot_date

    @property
    def ingestion_timestamp(self) -> datetime.datetime:
        return self._ingestion_timestamp

    # Profile
    @property
    def long_name(self) -> str | None:
        return self._long_name

    @property
    def sector(self) -> str | None:
        return self._sector

    @property
    def industry(self) -> str | None:
        return self._industry

    @property
    def country(self) -> str | None:
        return self._country

    @property
    def currency(self) -> str | None:
        return self._currency

    # Valuation
    @property
    def market_cap(self) -> float | None:
        return self._market_cap

    @property
    def trailing_pe(self) -> float | None:
        return self._trailing_pe

    @property
    def forward_pe(self) -> float | None:
        return self._forward_pe

    @property
    def price_to_book(self) -> float | None:
        return self._price_to_book

    @property
    def enterprise_value(self) -> float | None:
        return self._enterprise_value

    # Growth & margins
    @property
    def revenue_growth(self) -> float | None:
        return self._revenue_growth

    @property
    def gross_margins(self) -> float | None:
        return self._gross_margins

    @property
    def operating_margins(self) -> float | None:
        return self._operating_margins

    @property
    def profit_margins(self) -> float | None:
        return self._profit_margins

    @property
    def total_revenue(self) -> float | None:
        return self._total_revenue

    @property
    def ebitda(self) -> float | None:
        return self._ebitda

    # Risk
    @property
    def beta(self) -> float | None:
        return self._beta

    @property
    def fifty_two_week_high(self) -> float | None:
        return self._fifty_two_week_high

    @property
    def fifty_two_week_low(self) -> float | None:
        return self._fifty_two_week_low

    # Analyst view
    @property
    def recommendation_key(self) -> str | None:
        return self._recommendation_key

    @property
    def target_mean_price(self) -> float | None:
        return self._target_mean_price

    @property
    def number_of_analyst_opinions(self) -> int | None:
        return self._number_of_analyst_opinions
