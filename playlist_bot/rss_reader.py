from datetime import datetime
from time import mktime, struct_time
from typing import Generator

import feedparser
from pydantic import BaseModel, Json


class FluxFMRSSEntry(BaseModel):
    title: str
    published_time: struct_time

    @property
    def artist(self) -> str:
        artist_track = "".join(self.title.split(",")[1:])
        return artist_track.split("-")[0].strip()

    @property
    def track(self) -> str:
        artist_track = "".join(self.title.split(",")[1:])
        return artist_track.split("-")[1].strip()

    @property
    def datetime(self) -> datetime:
        return datetime.fromtimestamp(mktime(self.published_time))


class FluxFMRSSReader:
    def __init__(self, rss_url: str) -> None:
        """
        A simple RSS Reader class.

        :param rss_url: The RSS feed URL
        """
        self.rss_url = rss_url

    def __get_rss_feed(self) -> Json:
        """
        Fetches and parses the RSS feed.

        :return: The XML feed as a JSON.
        """
        return feedparser.parse(self.rss_url)

    def rss_generator(self) -> Generator[FluxFMRSSEntry, None, None]:
        """
        Returns parsed FluxFMRSSEntry objects.

        :yield: The FLuxFMRSSEntry object
        """
        for item in self.__get_rss_feed():
            yield FluxFMRSSEntry(
                title=item.get("title"),
                published_time=item.get("published_parsed"),
            )
