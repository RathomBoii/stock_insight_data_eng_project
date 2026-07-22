from domains.stages.persist.entities.raw_ohlc_bar import RawOHLCBar


def is_valid_bar(bar: RawOHLCBar) -> bool:
    """§1.3 sanity: a real bar has low <= open/close <= high, volume >= 0."""
    return (
        bar.low <= bar.open <= bar.high
        and bar.low <= bar.close <= bar.high
        and bar.volume >= 0
    )
