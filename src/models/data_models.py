import enum
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


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
    """刮削器需返回的影片数据"""

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

    @classmethod
    def new_empty(cls) -> "MovieData":
        """
        创建一个新的空的 MovieData. 仅用于特定场景.

        不直接设置字段默认值, 因此要求各刮削器必须显式声明自己不支持的字段.
        """
        return cls(
            number="",
            title="",
            originaltitle="",
            actor="",
            outline="",
            originalplot="",
            tag="",
            release="",
            year="",
            runtime="",
            score="",
            series="",
            director="",
            studio="",
            publisher="",
            source="",
            website="",
            cover="",
            poster="",
            extrafanart=[],
            trailer="",
            actor_photo={},
            mosaic="",
            image_download=False,
            image_cut="",
            wanted="",
        )

    def update(self, other: "MovieData"):
        """更新数据"""
        if not isinstance(other, MovieData):
            raise TypeError("other must be an instance of MovieData")
        self.__dict__.update(other.__dict__)

    def get(self, key: str, default=None):
        """获取数据"""
        return self.__dict__.get(key, default)

    def set(self, key: str, value):
        """设置数据"""
        if key in self.__dict__:
            self.__dict__[key] = value
        else:
            raise KeyError(f"{key} not in MovieData")


class Lang(enum.Enum):
    zh_cn = "zh_cn"
    zh_tw = "zh_tw"
    jp = "jp"


@dataclass
class CrawlerResult:
    site: str
    data: MovieData
    success: bool = True

    @classmethod
    def failed(cls, site: str) -> "CrawlerResult":
        """创建失败的爬虫结果"""
        return cls(site=site, success=False, data=MovieData.new_empty())


@dataclass
class Metadata:
    """刮削过程的中间数据及调试信息等"""

    letters: str = ""
    short_number: str = ""
    file_path: str = ""
    appoint_number: str = ""
    appoint_url: str = ""
    has_sub: bool = False
    c_word: str = ""
    leak: str = ""
    wuma: str = ""
    youma: str = ""
    cd_part: str = ""
    destroyed: str = ""
    version: int = 0
    actor_amazon: list = field(default_factory=list)
    originaltitle_amazon: str = ""
    website_name: str = ""
    fields_info: str = ""
    outline_from: str = ""
    poster_from: str = ""
    cover_from: str = ""
    extrafanart_from: str = ""
    trailer_from: str = ""
    amazon_orginaltitle_actor: str = ""
    cover_list: list = field(default_factory=list)


@dataclass
class FinalResult:
    data: MovieData
    metadata: Metadata

    def update(self, data: "MovieData"):
        """更新数据"""
        if not isinstance(data, MovieData):
            raise TypeError("FinalResult must be updated with MovieData")
        self.data.update(data)

    @classmethod
    def new_empty(cls) -> "FinalResult":
        """创建一个新的空的 FinalResult"""
        return cls(data=MovieData.new_empty(), metadata=Metadata())


class FileMode(Enum):
    Default = 0
    Single = 1
    Again = 2
