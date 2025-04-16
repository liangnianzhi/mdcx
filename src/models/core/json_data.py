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
class Other(TypedDict):  # 4
    fields_info: str
    failed_folder: str
    actor_photo: str
    all_actor_photo: dict


# core/web.py 使用的字段
class ImageData(TypedDict):  # 25
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
class NFOData(TypedDict):  # 43
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
class TranslateData(TypedDict):  # 17
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
class ShowData(TypedDict):  # 34
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
    show_name: str
    img_path: str
    country: str


class FileInfo(TypedDict):  # 30
    version: int
    number: str
    letters: str
    has_sub: bool
    c_word: str
    cd_part: str
    destroyed: str
    leak: str
    wuma: str
    youma: str
    mosaic: str
    _4K: str
    tag: str
    actor_href: str
    all_actor: str
    definition: str
    file_path: str
    appoint_number: str
    appoint_url: str
    website_name: str
    short_number: str
    poster_marked: bool
    thumb_marked: bool
    fanart_marked: bool
    poster_path: str
    thumb_path: str
    fanart_path: str
    title: str
    dont_move_movie: bool
    del_file_path: bool


# get_output_name/_get_folder_path/_generate_file_name 使用的字段
class PathInfo(TypedDict):  # 24
    destroyed: str
    leak: str
    wuma: str
    youma: str
    c_word: str
    title: str
    originaltitle: str
    studio: str
    publisher: str
    year: str
    outline: str
    runtime: str
    director: str
    actor: str
    release: str
    number: str
    series: str
    mosaic: str
    definition: str
    letters: str
    cd_part: str
    all_actor: str
    score: str
    wanted: str


class InputInfo(TypedDict):
    release: str
    number: str
    short_number: str
    source: str
    file_path: str
    appoint_number: str
    appoint_url: str
    has_sub: bool
    c_word: str
    leak: str
    wuma: str
    youma: str
    cd_part: str
    destroyed: str
    mosaic: str
    version: int
    actor_amazon: list[str]
    originaltitle_amazon: str
    website_name: str
    title: str
    all_actor: str
    all_actor_photo: dict


class JsonData(ImageData, NFOData, TranslateData, ShowData, FileInfo, PathInfo, InputInfo, Other):  # 72
    pass


# fmt: off
def new_json_data() -> JsonData:
    return {
        "show_name": "",                        # ShowData
        "img_path": "",                         # ShowData
        "tag_only": "",                         # NFOData
        "definition": "",                       # NFOData, PathInfo, ShowData
        "actor": "",                            # NFOData, PathInfo, TranslateData, ShowData
        "cover_size": (0, 0),                   # ImageData
        "poster_size": (0, 0),                  # ImageData
        "poster_big": False,                    # ImageData
        "poster_marked": True,                  # FileInfo, ImageData
        "thumb_marked": True,                   # FileInfo, ImageData
        "fanart_marked": True,                  # FileInfo, ImageData
        "cover_list": [],                       # ImageData, NFOData
        "poster_path": "",                      # FileInfo, ImageData, NFOData, ShowData
        "thumb_path": "",                       # FileInfo, ImageData, NFOData, ShowData
        "fanart_path": "",                      # FileInfo, ImageData, NFOData, ShowData
        "cover": "",                            # ImageData, NFOData
        "poster": "",                           # ImageData, NFOData
        "extrafanart": [],                      # ImageData
        "actor_amazon": [],                     # ImageData, NFOData
        "actor_href": "",                       # FileInfo, ShowData, TranslateData
        "all_actor": "",                        # FileInfo, PathInfo, ShowData, TranslateData
        "actor_photo": "",                      # Other
        "all_actor_photo": {},                  # Other
        "amazon_orginaltitle_actor": "",        # ImageData
        "file_path": "",                        # FileInfo, ShowData, TranslateData
        "del_file_path": False,                 # FileInfo
        "dont_move_movie": False,               # FileInfo
        "nfo_can_translate": False,             # NFOData
        "title": "",                            # NFOData, PathInfo, ShowData, TranslateData
        "outline": "",                          # NFOData, PathInfo, ShowData, TranslateData
        "failed_folder": "",                    # Other
        "version": 0,                           # FileInfo
        "image_download": False,                # ImageData
        "outline_from": "",                     # NFOData, TranslateData
        "cover_from": "",                       # ImageData, NFOData, ShowData
        "poster_from": "",                      # ImageData, NFOData, ShowData
        "extrafanart_from": "",                 # NFOData, ShowData
        "trailer_from": "",                     # ImageData, NFOData, ShowData
        "short_number": "",                     # FileInfo
        "appoint_number": "",                   # NFOData, FileInfo
        "appoint_url": "",                      # FileInfo
        "website_name": "",                     # FileInfo
        "fields_info": "",                      # Other
        "number": "",                           # NFOData, PathInfo, ShowData, FileInfo, TranslateData
        "letters": "",                          # NFOData, PathInfo, FileInfo, TranslateData
        "has_sub": False,                       # FileInfo, TranslateData, ShowData
        "c_word": "",                           # NFOData, PathInfo, FileInfo, ShowData
        "cd_part": "",                          # ImageData, NFOData, PathInfo, FileInfo, TranslateData, ShowData
        "destroyed": "",                        # FileInfo, PathInfo, ShowData
        "leak": "",                             # FileInfo, PathInfo, ShowData
        "wuma": "",                             # FileInfo, PathInfo
        "youma": "",                            # FileInfo, PathInfo
        "mosaic": "",                           # ImageData, NFOData, PathInfo, FileInfo, TranslateData, ShowData
        "tag": "",                              # NFOData, TranslateData, FileInfo, ShowData
        "_4K": "",                              # FileInfo
        "source": "",                           # NFOData, ShowData
        "release": "",                          # NFOData, PathInfo, ShowData
        "year": "",                             # NFOData, PathInfo, ShowData
        "javdbid": "",                          # NFOData
        "score": "0.0",                         # NFOData, PathInfo
        "originaltitle": "",                    # NFOData, PathInfo
        "studio": "",                           # NFOData, PathInfo, ShowData, TranslateData
        "publisher": "",                        # NFOData, PathInfo, ShowData, TranslateData
        "runtime": "",                          # NFOData, PathInfo, ShowData
        "director": "",                         # NFOData, PathInfo, ShowData, TranslateData
        "website": "",                          # NFOData, ShowData
        "series": "",                           # NFOData, PathInfo, ShowData, TranslateData
        "trailer": "",                          # ImageData, NFOData
        "originaltitle_amazon": "",             # ImageData, NFOData
        "originalplot": "",                     # NFOData
        "wanted": "",                           # NFOData, PathInfo
        "country": "",                          # NFOData, ShowData
    }
