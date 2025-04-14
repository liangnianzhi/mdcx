import enum
from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class EMbyActressInfo:
    name: str
    server_id: str
    id: str
    birthday: str = "0000-00-00"
    year: str = "0000"
    overview: str = ""
    taglines: list = field(default_factory=list)
    genres: list = field(default_factory=list)
    tags: list = field(default_factory=list)
    provider_ids: dict = field(default_factory=dict)
    taglines_translate: bool = False
    locations: list = field(default_factory=list)

    def dump(self) -> dict:
        # 此处生成的 json 符合 emby/jellyfin 规范
        return {
            "Name": self.name,
            "ServerId": self.server_id,
            "Id": self.id,
            "Genres": self.genres,
            "Tags": self.tags,
            "ProviderIds": self.provider_ids,
            "ProductionLocations": self.locations,
            "PremiereDate": self.birthday,
            "ProductionYear": self.year,
            "Overview": self.overview,
            "Taglines": self.taglines,
        }


@dataclass
class MovieData:
    number: str
    title: str
    originaltitle: str
    actor: str
    outline: str
    originalplot: str
    tag: str
    release: str
    year: str
    runtime: str
    score: str
    series: str
    director: str
    studio: str
    publisher: str
    source: str
    website: str
    cover: str
    poster: str
    extrafanart: list[str]
    trailer: str
    actor_photo: Dict[str, str]  # = field(default_factory=dict)
    mosaic: str
    image_download: bool  # = False
    image_cut: str  # = "right"
    wanted: str

    # 可选字段
    all_actor: str = ""
    all_actor_photo: Dict[str, str] = field(default_factory=dict)
    country: str = ""
    javdb_id: str = ""

    def update(self, other: "MovieData"):
        """更新数据"""
        if not isinstance(other, MovieData):
            raise TypeError("other must be an instance of MovieData")
        self.__dict__.update(other.__dict__)


class Lang(enum.Enum):
    zh_cn = "zh_cn"
    zh_tw = "zh_tw"
    jp = "jp"


@dataclass
class CrawlerResult:
    site: str
    data: Optional[MovieData] = None

    @classmethod
    def failed(cls, site: str) -> "CrawlerResult":
        """创建失败的爬虫结果"""
        return cls(site=site)
