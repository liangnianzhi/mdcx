"""
刮削过程的一般工具函数
依赖:
    此模块不应依赖 models.core 中除 flags 外的任何其他模块
"""

import json
import os
import re
import shutil
import subprocess
import traceback
import unicodedata
from typing import Optional

try:
    import cv2

    has_opencv = True
except ImportError:
    has_opencv = False
from models.base.file import read_link, split_path
from models.base.path import get_main_path, get_path
from models.base.utils import convert_path, get_used_time
from models.config.config import config
from models.core.json_data import LogBuffer
from models.signals import signal

has_ffprobe = True if shutil.which("ffprobe") else False


def _get_video_metadata_opencv(file_path: str) -> tuple[int, str]:
    cap = cv2.VideoCapture(file_path)
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    ##使用opencv获取编码器格式
    codec = int(cap.get(cv2.CAP_PROP_FOURCC))
    codec_fourcc = chr(codec & 0xFF) + chr((codec >> 8) & 0xFF) + chr((codec >> 16) & 0xFF) + chr((codec >> 24) & 0xFF)
    return height, codec_fourcc


def _get_video_metadata_ffmpeg(file_path: str) -> tuple[int, str]:
    if not has_ffprobe:
        raise RuntimeError("当前版本无 opencv. 若想获取视频分辨率请请安装 ffprobe 或改用带 opencv 版本.")
    # Use ffprobe to get video information
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", file_path]

    # macOS and Linux use default flags
    creationflags = 0
    # Windows use CREATE_NO_WINDOW to suppress the console window
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW

    result = subprocess.run(cmd, capture_output=True, text=True, creationflags=creationflags)

    data = json.loads(result.stdout)

    # Find video stream
    video_stream = next((stream for stream in data["streams"] if stream["codec_type"] == "video"), None)

    if video_stream:
        height = int(video_stream["height"])
        codec_fourcc = video_stream["codec_name"].upper()
    else:
        height = 0
        codec_fourcc = ""
    return height, codec_fourcc


_get_video_metadata = _get_video_metadata_opencv if has_opencv else _get_video_metadata_ffmpeg


def get_video_size(raw_tag: str, file_path: str) -> tuple[str, str, str]:
    """return: (definition, d_4K, tag)"""
    # 获取本地分辨率 同时获取视频编码格式
    definition = ""
    height = 0
    hd_get = config.hd_get
    if os.path.islink(file_path):
        if "symlink_definition" in config.no_escape:
            file_path = read_link(file_path)
        else:
            hd_get = "path"
    if hd_get == "video":
        try:
            height, codec_fourcc = _get_video_metadata(file_path)
        except Exception as e:
            signal.show_log_text(f" 🔴 无法获取视频分辨率! 文件地址: {file_path}  错误信息: {e}")
    elif hd_get == "path":
        file_path_temp = file_path.upper()
        if "8K" in file_path_temp:
            height = 4000
        elif "4K" in file_path_temp or "UHD" in file_path_temp:
            height = 2000
        elif "1440P" in file_path_temp or "QHD" in file_path_temp:
            height = 1440
        elif "1080P" in file_path_temp or "FHD" in file_path_temp:
            height = 1080
        elif "960P" in file_path_temp:
            height = 960
        elif "720P" in file_path_temp or "HD" in file_path_temp:
            height = 720

    hd_name = config.hd_name
    if not height:
        pass
    elif height >= 4000:
        definition = "8K" if hd_name == "height" else "UHD8"
    elif height >= 2000:
        definition = "4K" if hd_name == "height" else "UHD"
    elif height >= 1400:
        definition = "1440P" if hd_name == "height" else "QHD"
    elif height >= 1000:
        definition = "1080P" if hd_name == "height" else "FHD"
    elif height >= 900:
        definition = "960P" if hd_name == "height" else "HD"
    elif height >= 700:
        definition = "720P" if hd_name == "height" else "HD"
    elif height >= 500:
        definition = "540P" if hd_name == "height" else "qHD"
    elif height >= 400:
        definition = "480P"
    elif height >= 300:
        definition = "360P"
    elif height >= 100:
        definition = "144P"

    d_4K = ""
    if definition in ["4K", "8K", "UHD", "UHD8"]:
        d_4K = "-" + definition

    # 去除标签中的分辨率率，使用本地读取的实际分辨率
    remove_key = ["144P", "360P", "480P", "540P", "720P", "960P", "1080P", "1440P", "2160P", "4K", "8K"]
    tag = raw_tag
    for each_key in remove_key:
        tag = tag.replace(each_key, "").replace(each_key.lower(), "")
    tag_list = re.split(r"[,，]", tag)
    new_tag_list = []
    [new_tag_list.append(i) for i in tag_list if i]
    if definition and "definition" in config.tag_include:
        new_tag_list.insert(0, definition)
        if hd_get == "video":
            new_tag_list.insert(0, codec_fourcc.upper())  # 插入编码格式
    tag = "，".join(new_tag_list)
    return definition, d_4K, tag


def show_data_result(title: str, fields_info: str, start_time: float) -> bool:
    if title == "":
        LogBuffer.log().write(
            f"\n 🌐 [website] {LogBuffer.req().get().strip('-> ')}"
            f"\n{LogBuffer.info().get().strip()}"
            f"\n 🔴 Data failed!({get_used_time(start_time)}s)"
        )
        return False
    else:
        if config.show_web_log == "on":  # 字段刮削过程
            LogBuffer.log().write(f"\n 🌐 [website] {LogBuffer.req().get().strip('-> ')}")
        try:
            LogBuffer.log().write("\n" + LogBuffer.info().get().strip(" ").strip("\n"))
        except:
            signal.show_log_text(traceback.format_exc())
        if config.show_from_log == "on":  # 字段来源信息
            if fields_info:
                LogBuffer.log().write("\n" + fields_info.strip(" ").strip("\n"))
        LogBuffer.log().write(f"\n 🍀 Data done!({get_used_time(start_time)}s)")
        return True


def deal_url(url: str) -> tuple[Optional[str], str]:
    if "://" not in url:
        url = "https://" + url
    url = url.strip()
    for key, vlaue in config.web_dic.items():
        if key.lower() in url.lower():
            return vlaue, url

    # 自定义的网址
    for web_name in config.SUPPORTED_WEBSITES:
        if hasattr(config, web_name + "_website"):
            web_url = getattr(config, web_name + "_website")
            if web_url in url:
                return web_name, url

    return None, url


def convert_half(string: str) -> str:
    # 替换敏感词
    for key, value in config.special_word.items():
        string = string.replace(key, value)
    # 替换全角为半角
    for each in config.full_half_char:
        string = string.replace(each[0], each[1])
    # 去除空格等符号
    return re.sub(r"[\W_]", "", string).upper()


def get_new_release(release: str) -> str:
    release_rule = config.release_rule
    if not release:
        release = "0000-00-00"
    if release_rule == "YYYY-MM-DD":
        return release
    year, month, day = re.findall(r"(\d{4})-(\d{2})-(\d{2})", release)[0]
    return release_rule.replace("YYYY", year).replace("YY", year[-2:]).replace("MM", month).replace("DD", day)


def nfd2c(path: str) -> str:
    # 转换 NFC(mac nfc和nfd都能访问到文件，但是显示的是nfd，这里统一使用nfc，避免各种问题。
    # 日文浊音转换（mac的坑，osx10.12以下使用nfd，以上兼容nfc和nfd，只是显示成了nfd）
    if config.is_nfc:
        new_path = unicodedata.normalize("NFC", path)  # Mac 会拆成两个字符，即 NFD，windwos是 NFC
    else:
        new_path = unicodedata.normalize("NFD", path)  # Mac 会拆成两个字符，即 NFD，windwos是 NFC
    return new_path


def get_movie_path_setting(file_path="") -> tuple[str, str, str, list[str], str, str]:
    # 先把'\'转成'/'以便判断是路径还是目录
    movie_path = config.media_path.replace("\\", "/")  # 用户设置的扫描媒体路径
    if movie_path == "":  # 未设置为空时，使用主程序目录
        movie_path = get_main_path()
    movie_path = nfd2c(movie_path)
    end_folder_name = split_path(movie_path)[1]
    # 用户设置的软链接输出目录
    softlink_path = config.softlink_path.replace("\\", "/").replace("end_folder_name", end_folder_name)
    # 用户设置的成功输出目录
    success_folder = config.success_output_folder.replace("\\", "/").replace("end_folder_name", end_folder_name)
    # 用户设置的失败输出目录
    failed_folder = config.failed_output_folder.replace("\\", "/").replace("end_folder_name", end_folder_name)
    # 用户设置的排除目录
    escape_folder_list = (
        config.folders.replace("\\", "/").replace("end_folder_name", end_folder_name).replace("，", ",").split(",")
    )
    # 用户设置的剧照副本目录
    extrafanart_folder = config.extrafanart_folder.replace("\\", "/")

    # 获取路径
    softlink_path = convert_path(get_path(movie_path, softlink_path))
    success_folder = convert_path(get_path(movie_path, success_folder))
    failed_folder = convert_path(get_path(movie_path, failed_folder))
    softlink_path = nfd2c(softlink_path)
    success_folder = nfd2c(success_folder)
    failed_folder = nfd2c(failed_folder)
    extrafanart_folder = nfd2c(extrafanart_folder)

    # 获取排除目录完整路径（尾巴添加/）
    escape_folder_new_list = []
    for es in escape_folder_list:  # 排除目录可以多个，以，,分割
        es = es.strip(" ")
        if es:
            es = get_path(movie_path, es).replace("\\", "/")
            if es[-1] != "/":  # 路径尾部添加“/”，方便后面move_list查找时匹配路径
                es += "/"
            es = nfd2c(es)
            escape_folder_new_list.append(es)

    if file_path:
        temp_path = movie_path
        if config.scrape_softlink_path:
            temp_path = softlink_path
        if "first_folder_name" in success_folder or "first_folder_name" in failed_folder:
            first_folder_name = re.findall(r"^/?([^/]+)/", file_path[len(temp_path) :].replace("\\", "/"))
            first_folder_name = first_folder_name[0] if first_folder_name else ""
            success_folder = success_folder.replace("first_folder_name", first_folder_name)
            failed_folder = failed_folder.replace("first_folder_name", first_folder_name)

    return (
        convert_path(movie_path),
        success_folder,
        failed_folder,
        escape_folder_new_list,
        extrafanart_folder,
        softlink_path,
    )
