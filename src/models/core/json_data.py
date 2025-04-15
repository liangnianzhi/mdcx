import threading
from typing import TypedDict


class LogBuffer:
    all_buffers = {}
    global_buffer = None

    @staticmethod
    def _global_buffer() -> "LogBuffer":
        if LogBuffer.global_buffer is None:
            LogBuffer.global_buffer = LogBuffer()
        return LogBuffer.global_buffer

    @staticmethod
    def _get_buffer(category: str) -> "LogBuffer":
        pid = threading.current_thread().ident
        if pid is None:
            return LogBuffer._global_buffer()
        if pid not in LogBuffer.all_buffers:
            LogBuffer.all_buffers[pid] = {}
        if category not in LogBuffer.all_buffers[pid]:
            LogBuffer.all_buffers[pid][category] = LogBuffer()
        return LogBuffer.all_buffers[pid][category]

    @staticmethod
    def log() -> "LogBuffer":
        return LogBuffer._get_buffer("log")

    @staticmethod
    def info() -> "LogBuffer":
        return LogBuffer._get_buffer("info")

    @staticmethod
    def error() -> "LogBuffer":
        return LogBuffer._get_buffer("error")

    @staticmethod
    def req() -> "LogBuffer":
        return LogBuffer._get_buffer("req")

    def __init__(self):
        self.buffer = []

    def write(self, message):
        self.buffer.append(message)

    def get(self):
        return "".join(self.buffer)

    def last(self):
        if len(self.buffer) == 0:
            return ""
        return self.buffer[-1]

    def clear(self):
        self.buffer.clear()


# 尚未处理的字段
class Other(TypedDict):
    short_number: str
    appoint_url: str
    website_name: str
    fields_info: str
    wuma: str
    youma: str
    _4K: str
    failed_folder: str
    version: int
    actor_photo: str
    all_actor_photo: dict
    dont_move_movie: bool
    del_file_path: bool


# core/web.py 使用的字段
class ImageData(TypedDict):
    cd_part: str

    cover_size: tuple[int, int]
    poster_big: bool
    poster_marked: bool
    thumb_marked: bool
    fanart_marked: bool
    cover_list: list[tuple[str, str]]
    poster_path: str
    thumb_path: str
    fanart_path: str
    cover: str
    poster: str
    trailer: str
    extrafanart: list[str]
    cover_from: str
    poster_from: str
    trailer_from: str

    number: str
    letters: str
    image_download: bool
    poster_size: tuple[int, int]
    mosaic: str
    originaltitle_amazon: str
    actor_amazon: list[str]
    amazon_orginaltitle_actor: str


# core/nfo.py 使用的字段
class NFOData(TypedDict):
    nfo_can_translate: bool
    c_word: str
    cd_part: str
    originaltitle: str
    originalplot: str
    title: str
    studio: str
    publisher: str
    year: str
    outline: str
    outline_from: str
    country: str
    runtime: str
    director: str
    actor: str
    all_actor: str
    release: str
    tag: str
    tag_only: str
    number: str
    cover: str
    poster: str
    website: str
    series: str
    mosaic: str
    definition: str
    trailer: str
    letters: str
    wanted: str
    score: str
    originaltitle_amazon: str
    actor_amazon: list[str]
    source: str
    poster_from: str
    cover_from: str
    extrafanart_from: str
    trailer_from: str
    appoint_number: str
    javdbid: str
    cover_list: list[tuple[str, str]]
    poster_path: str
    thumb_path: str
    fanart_path: str


# core/translate.py 使用的字段
class TranslateData(TypedDict):
    title: str
    outline: str
    file_path: str
    cd_part: str
    tag: str
    actor: str
    all_actor: str
    letters: str
    number: str
    has_sub: bool
    mosaic: str
    series: str
    studio: str
    publisher: str
    director: str
    outline_from: str
    actor_href: str


# 主界面展示使用的字段
class ShowData(TypedDict):
    file_path: str
    number: str
    actor: str
    all_actor: str
    source: str
    website: str
    title: str
    outline: str
    tag: str
    release: str
    year: str
    runtime: str
    director: str
    series: str
    studio: str
    publisher: str
    poster_path: str
    thumb_path: str
    fanart_path: str
    has_sub: bool
    c_word: str
    leak: str
    cd_part: str
    mosaic: str
    destroyed: str
    actor_href: str
    definition: str
    cover_from: str
    poster_from: str
    extrafanart_from: str
    trailer_from: str
    file_path: str
    show_name: str
    img_path: str
    country: str


class JsonData(ImageData, NFOData, TranslateData, ShowData, Other):
    pass


def new_json_data() -> JsonData:
    return {
        "show_name": "",
        "img_path": "",
        "tag_only": "",
        "definition": "",
        "actor": "",
        "cover_size": (0, 0),
        "poster_size": (0, 0),
        "poster_big": False,
        "poster_marked": True,
        "thumb_marked": True,
        "fanart_marked": True,
        "cover_list": [],
        "poster_path": "",
        "thumb_path": "",
        "fanart_path": "",
        "cover": "",
        "poster": "",
        "extrafanart": [],
        "actor_amazon": [],
        "actor_href": "",
        "all_actor": "",
        "actor_photo": "",
        "all_actor_photo": {},
        "amazon_orginaltitle_actor": "",
        "file_path": "",
        "del_file_path": False,
        "dont_move_movie": False,
        "nfo_can_translate": False,
        "title": "",
        "outline": "",
        "failed_folder": "",
        "version": 0,
        "image_download": False,
        "outline_from": "",
        "cover_from": "",
        "poster_from": "",
        "extrafanart_from": "",
        "trailer_from": "",
        "short_number": "",
        "appoint_number": "",
        "appoint_url": "",
        "website_name": "",
        "fields_info": "",
        "number": "",
        "letters": "",
        "has_sub": False,
        "c_word": "",
        "cd_part": "",
        "destroyed": "",
        "leak": "",
        "wuma": "",
        "youma": "",
        "mosaic": "",
        "tag": "",
        "_4K": "",
        "source": "",
        "release": "",
        "year": "",
        "javdbid": "",
        "score": "0.0",
        "originaltitle": "",
        "studio": "",
        "publisher": "",
        "runtime": "",
        "director": "",
        "website": "",
        "series": "",
        "trailer": "",
        "originaltitle_amazon": "",
        "originalplot": "",
        "wanted": "",
        "country": "",
    }
