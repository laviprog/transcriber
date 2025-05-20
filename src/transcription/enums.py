from src.enums import BaseEnum


class Language(BaseEnum):
    RUSSIAN = "ru"
    ENGLISH = "en"


class Model(BaseEnum):
    SMALL = "small"
    MEDIUM = "medium"
    TURBO = "turbo"
    LARGE_V3 = "large-v3"
    LARGE_V3_TURBO = "large-v3-turbo"


class ResultFormat(BaseEnum):
    TEXT = "text"
    SRT = "srt"
