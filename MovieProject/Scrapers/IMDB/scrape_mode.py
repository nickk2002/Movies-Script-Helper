import enum


class IMDBScrapeMode(enum.Enum):
    FullScrape = 1
    ID = 2
    ID_DURATION = 3
    CHECK_EXISTS = 4