"""
Flux FM RSS feed reader components
"""
from datetime import datetime
from time import mktime, struct_time
from typing import Generator

import feedparser
from pydantic import BaseModel, Json


class FluxFMRSSEntry(BaseModel):
    """
    A PyDantic model for a Flux FM RSS feed entry.
    """
    title: str
    published_time: struct_time

    @property
    def artist(self) -> str:
        """
        Parses the track artist.

        :return: The track artist.
        """
        artist_track = "".join(self.title.split(",")[1:])
        return artist_track.split("-")[0].strip()

    @property
    def track(self) -> str:
        """
        Parses the track title.

        :return: The track title.
        """
        artist_track = "".join(self.title.split(",")[1:])
        return artist_track.split("-")[1].strip()

    @property
    def datetime(self) -> datetime:
        """
        Parses the published timestamp.

        :return: The timestamp as a python datetime object.
        """
        return datetime.fromtimestamp(mktime(self.published_time))


class FluxFMRSSReader:
    """
    A simple RSS Reader class for Flux FM streams.
    """
    def __init__(self, rss_url: str) -> None:
        """
        :param rss_url: The RSS feed URL
        """
        self.rss_url = rss_url

    def get_rss_feed(self) -> Json:
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
        for item in self.get_rss_feed():
            yield FluxFMRSSEntry(
                title=item.get("title"),
                published_time=item.get("published_parsed"),
            )
