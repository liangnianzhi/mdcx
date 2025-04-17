import enum
from dataclasses import dataclass, field, fields
from enum import Enum


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
    actor_photo: dict[str, str]  # = field(default_factory=dict)
    mosaic: str
    image_download: bool  # = False
    image_cut: str  # = "right"
    wanted: str

    # 可选字段
    all_actor: str = ""
    all_actor_photo: dict[str, str] = field(default_factory=dict)
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

    # 不重载 __setitem__ 和 __getitem__ 方法, get/set 作为权宜之计以方便查找调用方, 最终要采用安全的方法
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
class ScrapeContext: ...


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


@dataclass
class ShowData:
    file_path: str = ""  # #meta
    number: str = ""  # #movie
    actor: str = ""  # #movie
    all_actor: str = ""  # #movie
    source: str = ""  # #movie
    website: str = ""  # #movie
    title: str = ""  # #movie
    outline: str = ""  # #movie
    tag: str = ""  # #movie
    release: str = ""  # #movie
    year: str = ""  # #movie
    runtime: str = ""  # #movie
    director: str = ""  # #movie
    series: str = ""  # #movie
    studio: str = ""  # #movie
    publisher: str = ""  # #movie
    poster_path: str = ""
    thumb_path: str = ""
    fanart_path: str = ""
    has_sub: bool = False  # #meta
    c_word: str = ""  # #meta
    leak: str = ""  # #meta
    cd_part: str = ""  # #meta
    mosaic: str = ""  # #movie
    destroyed: str = ""  # #meta
    actor_href: str = ""
    definition: str = ""
    cover_from: str = ""  # #meta
    poster_from: str = ""  # #meta
    extrafanart_from: str = ""  # #meta
    trailer_from: str = ""  # #meta
    show_name: str = ""
    img_path: str = ""
    country: str = ""  # #movie

    # used in _show_nfo_info
    originaltitle: str = ""  # #movie
    cover: str = ""  # #movie
    poster: str = ""  # #movie
    trailer: str = ""  # #movie
    originalplot: str = ""  # #movie
    wanted: str = ""  # #movie
    score: str = ""  # #movie

    # compatible with NFOData
    javdbid: str = ""
    letters: str = ""  # #meta
    outline_from: str = ""  # #meta
    tag_only: str = ""
    cover_list: list[tuple[str, str]] = field(default_factory=list)  # #meta
    actor_amazon: list[str] = field(default_factory=list)  # #meta
    originaltitle_amazon: str = ""  # #meta
    nfo_can_translate: bool = False  # todo remove this


@dataclass
class FileInfo:
    number: str = ""  # #movie
    letters: str = ""  # #meta
    has_sub: bool = False  # #meta
    c_word: str = ""  # #meta
    cd_part: str = ""  # #meta
    destroyed: str = ""  # #meta
    leak: str = ""  # #meta
    wuma: str = ""  # #meta
    youma: str = ""  # #meta
    mosaic: str = ""  # #movie
    tag: str = ""  # #movie
    all_actor: str = ""  # #movie
    file_path: str = ""  # #meta
    appoint_number: str = ""  # #meta
    appoint_url: str = ""  # #meta
    website_name: str = ""  # #meta
    short_number: str = ""  # #meta
    title: str = ""  # #movie
    _4K: str = ""
    actor_href: str = ""
    definition: str = ""
    version: int = 0  # #meta
    poster_marked: bool = True
    thumb_marked: bool = True
    fanart_marked: bool = True
    poster_path: str = ""
    thumb_path: str = ""
    fanart_path: str = ""
    dont_move_movie: bool = False
    del_file_path: bool = False

    # 精简 get_file_info return value
    # movie_number = number
    folder_path: str = ""
    file_name_no_ext: str = ""
    file_ext: str = ""
    sub_list: list[str] = field(default_factory=list)
    file_show_name: str = ""
    file_show_path: str = ""


# utils for checking fields info


def field_names(cls) -> set[str]:
    """获取类的所有字段名称"""
    return set(f.name for f in fields(cls))


def _format_fields(s: set[str], sep: str = " | ", asc: bool = True) -> str:
    return sep.join(sorted(s, reverse=not asc))


def compare_dataclasses(cls1, cls2):
    fields1 = field_names(cls1)
    fields2 = field_names(cls2)
    print(f"{'=' * 15} {cls1.__name__} vs {cls2.__name__} {'=' * 15}")
    print(f"In {cls1.__name__} but not in {cls2.__name__}:\n {_format_fields(fields1 - fields2)}\n")
    print(f"In {cls2.__name__} but not in {cls1.__name__}:\n {_format_fields(fields2 - fields1)}\n")
    print(f"Same fields:\n {_format_fields(fields1 & fields2)}\n")


def has_fields(cls, fields: set[str]) -> tuple[bool, set[str]]:
    """检查 dataclass 是否包含指定字段"""
    cls_fields = field_names(cls)
    not_in = fields - cls_fields
    return len(not_in) == 0, not_in


compare_dataclasses(MovieData, ShowData)
compare_dataclasses(Metadata, FileInfo)
