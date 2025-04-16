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
# class Other(TypedDict):  # 3
#     fields_info: str  # #meta
#     actor_photo: str  # #movie
#     all_actor_photo: dict  # #movie


# core/web.py 使用的字段
class ImageData(TypedDict):  # 25
    # cd_part: str  # #meta
    cover_size: tuple[int, int]
    poster_big: bool
    poster_marked: bool
    thumb_marked: bool
    fanart_marked: bool
    # cover_list: list[tuple[str, str]]  # #meta
    poster_path: str
    thumb_path: str
    fanart_path: str
    # cover: str  # #movie
    # poster: str  # #movie
    # trailer: str  # #movie
    # extrafanart: list[str]  # #movie
    # cover_from: str  # #meta
    # poster_from: str  # #meta
    # trailer_from: str  # #meta
    # number: str  # #movie
    # letters: str  # #meta
    # image_download: bool  # #meta #movie
    poster_size: tuple[int, int]
    # mosaic: str  # #movie
    # originaltitle_amazon: str  # #meta
    # actor_amazon: list[str]  # #meta
    # amazon_orginaltitle_actor: str  # #meta


# core/nfo.py 使用的字段
class NFOData(TypedDict):  # 43
    nfo_can_translate: bool
    # c_word: str  # #meta
    # cd_part: str  # #meta
    # originaltitle: str  # #movie
    # originalplot: str  # #movie
    # title: str  # #movie
    # studio: str  # #movie
    # publisher: str  # #movie
    # year: str  # #movie
    # outline: str  # #movie
    # outline_from: str  # #meta
    # country: str  # #movie
    # runtime: str  # #movie
    # director: str  # #movie
    # actor: str  # #movie
    # all_actor: str  # #movie
    # release: str  # #movie
    # tag: str  # #movie
    tag_only: str
    # number: str  # #movie
    # cover: str  # #movie
    # poster: str  # #movie
    # website: str  # #movie
    # series: str  # #movie
    # mosaic: str  # #movie
    definition: str
    # trailer: str  # #movie
    # letters: str  # #meta
    # wanted: str  # #movie
    # score: str  # #movie
    # originaltitle_amazon: str  # #meta
    # actor_amazon: list[str]  # #meta
    # source: str  # #movie
    # poster_from: str  # #meta
    # cover_from: str  # #meta
    # extrafanart_from: str  # #meta
    # trailer_from: str  # #meta
    # appoint_number: str  # #meta
    javdbid: str
    # cover_list: list[tuple[str, str]]  # #meta
    poster_path: str
    thumb_path: str
    fanart_path: str


# core/translate.py 使用的字段
class TranslateData(TypedDict):  # 17
    # title: str  # #movie
    # outline: str  # #movie
    # file_path: str  # #meta
    # cd_part: str  # #meta
    # tag: str  # #movie
    # actor: str  # #movie
    # all_actor: str  # #movie
    # letters: str  # #meta
    # number: str  # #movie
    # has_sub: bool  # #meta
    # mosaic: str  # #movie
    # series: str  # #movie
    # studio: str  # #movie
    # publisher: str  # #movie
    # director: str  # #movie
    # outline_from: str  # #meta
    actor_href: str


# 主界面展示使用的字段
class ShowData(TypedDict):  # 34
    # file_path: str  # #meta
    # number: str  # #movie
    # actor: str  # #movie
    # all_actor: str  # #movie
    # source: str  # #movie
    # website: str  # #movie
    # title: str  # #movie
    # outline: str  # #movie
    # tag: str  # #movie
    # release: str  # #movie
    # year: str  # #movie
    # runtime: str  # #movie
    # director: str  # #movie
    # series: str  # #movie
    # studio: str  # #movie
    # publisher: str  # #movie
    poster_path: str
    thumb_path: str
    fanart_path: str
    # has_sub: bool  # #meta
    # c_word: str  # #meta
    # leak: str  # #meta
    # cd_part: str  # #meta
    # mosaic: str  # #movie
    # destroyed: str  # #meta
    actor_href: str
    definition: str
    # cover_from: str  # #meta
    # poster_from: str  # #meta
    # extrafanart_from: str  # #meta
    # trailer_from: str  # #meta
    show_name: str
    img_path: str
    # country: str  # #movie


class FileInfo(TypedDict):  # 30
    # version: int  # #meta
    # number: str  # #movie
    # letters: str  # #meta
    # has_sub: bool  # #meta
    # c_word: str  # #meta
    # cd_part: str  # #meta
    # destroyed: str  # #meta
    # leak: str  # #meta
    # wuma: str  # #meta
    # youma: str  # #meta
    # mosaic: str  # #movie
    _4K: str
    # tag: str  # #movie
    actor_href: str
    # all_actor: str  # #movie
    definition: str
    # file_path: str  # #meta
    # appoint_number: str  # #meta
    # appoint_url: str  # #meta
    # website_name: str  # #meta
    # short_number: str  # #meta
    poster_marked: bool
    thumb_marked: bool
    fanart_marked: bool
    poster_path: str
    thumb_path: str
    fanart_path: str
    # title: str  # #movie
    dont_move_movie: bool
    del_file_path: bool


# get_output_name/_get_folder_path/_generate_file_name 使用的字段
class PathInfo(TypedDict):  # 24
    # destroyed: str  # #meta
    # leak: str  # #meta
    # wuma: str  # #meta
    # youma: str  # #meta
    # c_word: str  # #meta
    # title: str  # #movie
    # originaltitle: str  # #movie
    # studio: str  # #movie
    # publisher: str  # #movie
    # year: str  # #movie
    # outline: str  # #movie
    # runtime: str  # #movie
    # director: str  # #movie
    # actor: str  # #movie
    # release: str  # #movie
    # number: str  # #movie
    # series: str  # #movie
    # mosaic: str  # #movie
    definition: str
    # letters: str  # #meta
    # cd_part: str  # #meta
    # all_actor: str  # #movie
    # score: str  # #movie
    # wanted: str  # #movie


class InputInfo(TypedDict):
    release: str  # #movie
    number: str  # #movie
    short_number: str  # #meta
    source: str  # #movie
    file_path: str  # #meta
    appoint_number: str  # #meta
    appoint_url: str  # #meta
    has_sub: bool  # #meta
    c_word: str  # #meta
    leak: str  # #meta
    wuma: str  # #meta
    youma: str  # #meta
    cd_part: str  # #meta
    destroyed: str  # #meta
    mosaic: str  # #movie
    version: int  # #meta
    actor_amazon: list[str]  # #meta
    originaltitle_amazon: str  # #meta
    website_name: str  # #meta
    title: str  # #movie
    all_actor: str  # #movie
    all_actor_photo: dict  # #movie


class JsonData(ImageData, NFOData, TranslateData, ShowData, FileInfo, PathInfo, InputInfo):  # 71
    pass


# fmt: off
def new_json_data() -> JsonData:
    return {
        "_4K": "",                              # FileInfo
        "actor_amazon": [],                     # ImageData, NFOData
        "actor_href": "",                       # FileInfo, ShowData, TranslateData
        "all_actor_photo": {},                  # Other
        "all_actor": "",                        # FileInfo, PathInfo, ShowData, TranslateData
        "appoint_number": "",                   # NFOData, FileInfo
        "appoint_url": "",                      # FileInfo
        "c_word": "",                           # NFOData, PathInfo, FileInfo, ShowData
        "cd_part": "",                          # ImageData, NFOData, PathInfo, FileInfo, TranslateData, ShowData
        "cover_size": (0, 0),                   # ImageData
        "definition": "",                       # NFOData, PathInfo, ShowData
        "del_file_path": False,                 # FileInfo
        "destroyed": "",                        # FileInfo, PathInfo, ShowData
        "dont_move_movie": False,               # FileInfo
        "fanart_marked": True,                  # FileInfo, ImageData
        "fanart_path": "",                      # FileInfo, ImageData, NFOData, ShowData
        "file_path": "",                        # FileInfo, ShowData, TranslateData
        "has_sub": False,                       # FileInfo, TranslateData, ShowData
        "img_path": "",                         # ShowData
        "javdbid": "",                          # NFOData
        "leak": "",                             # FileInfo, PathInfo, ShowData
        "mosaic": "",                           # ImageData, NFOData, PathInfo, FileInfo, TranslateData, ShowData
        "nfo_can_translate": False,             # NFOData
        "number": "",                           # NFOData, PathInfo, ShowData, FileInfo, TranslateData
        "originaltitle_amazon": "",             # ImageData, NFOData
        "poster_big": False,                    # ImageData
        "poster_marked": True,                  # FileInfo, ImageData
        "poster_path": "",                      # FileInfo, ImageData, NFOData, ShowData
        "poster_size": (0, 0),                  # ImageData
        "release": "",                          # NFOData, PathInfo, ShowData
        "short_number": "",                     # FileInfo
        "show_name": "",                        # ShowData
        "source": "",                           # NFOData, ShowData
        "tag_only": "",                         # NFOData
        "thumb_marked": True,                   # FileInfo, ImageData
        "thumb_path": "",                       # FileInfo, ImageData, NFOData, ShowData
        "title": "",                            # NFOData, PathInfo, ShowData, TranslateData
        "version": 0,                           # FileInfo
        "website_name": "",                     # FileInfo
        "wuma": "",                             # FileInfo, PathInfo
        "youma": "",                            # FileInfo, PathInfo
        # "actor_photo": "",                      # Other
        # "actor": "",                            # NFOData, PathInfo, TranslateData, ShowData
        # "amazon_orginaltitle_actor": "",        # ImageData
        # "country": "",                          # NFOData, ShowData
        # "cover_from": "",                       # ImageData, NFOData, ShowData
        # "cover_list": [],                       # ImageData, NFOData
        # "cover": "",                            # ImageData, NFOData
        # "director": "",                         # NFOData, PathInfo, ShowData, TranslateData
        # "extrafanart_from": "",                 # NFOData, ShowData
        # "extrafanart": [],                      # ImageData
        # "fields_info": "",                      # Other
        # "image_download": False,                # ImageData
        # "letters": "",                          # NFOData, PathInfo, FileInfo, TranslateData
        # "originalplot": "",                     # NFOData
        # "originaltitle": "",                    # NFOData, PathInfo
        # "outline_from": "",                     # NFOData, TranslateData
        # "outline": "",                          # NFOData, PathInfo, ShowData, TranslateData
        # "poster_from": "",                      # ImageData, NFOData, ShowData
        # "poster": "",                           # ImageData, NFOData
        # "publisher": "",                        # NFOData, PathInfo, ShowData, TranslateData
        # "runtime": "",                          # NFOData, PathInfo, ShowData
        # "score": "0.0",                         # NFOData, PathInfo
        # "series": "",                           # NFOData, PathInfo, ShowData, TranslateData
        # "studio": "",                           # NFOData, PathInfo, ShowData, TranslateData
        # "tag": "",                              # NFOData, TranslateData, FileInfo, ShowData
        # "trailer_from": "",                     # ImageData, NFOData, ShowData
        # "trailer": "",                          # ImageData, NFOData
        # "wanted": "",                           # NFOData, PathInfo
        # "website": "",                          # NFOData, ShowData
        # "year": "",                             # NFOData, PathInfo, ShowData
    }
