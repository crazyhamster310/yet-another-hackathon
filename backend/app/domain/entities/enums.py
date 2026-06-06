from enum import StrEnum


class WidgetType(StrEnum):
    NEWS = "news"
    STATIC = "static"
    PARKING = "parking"
    STORAGE = "storage"


class DataSourceType(StrEnum):
    UJIN_API = "ujin_api"
    LOCAL = "local"
    EXTERNAL = "external"
