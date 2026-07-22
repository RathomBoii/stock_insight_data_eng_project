from dataclasses import dataclass
import datetime
    
class NewsArticleInput:
    ticker: str
    title: str
    publisher: str
    link: str
    publish_time: datetime.datetime  # UTC-normalized timestamp of when the article was published

class NewsArticle:
    def __init__(self, props: NewsArticleInput):
        self._ticker = props.ticker
        self._title = props.title
        self._publisher = props.publisher
        self._link = props.link
        self._publish_time = props.publish_time

    @property
    def ticker(self) -> str:
        return self._ticker

    @property
    def title(self) -> str:
        return self._title

    @property
    def publisher(self) -> str:
        return self._publisher

    @property
    def link(self) -> str:
        return self._link

    @property
    def publish_time(self) -> datetime.datetime:
        return self._publish_time
