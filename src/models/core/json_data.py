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


# core/translate.py 使用的字段, 此类型已使用 MovieData + MetaData 替换
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
    actor_href: str  # todo
