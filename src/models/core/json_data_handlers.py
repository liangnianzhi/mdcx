import re
import traceback

from models.base.number import get_number_letters
from models.config.config import config
from models.config.resources import resources
from models.core.json_data import LogBuffer
from models.data_models import MovieData
from models.signals import signal


def replace_word(movie_data: MovieData):
    # 常见字段替换的字符
    for key, value in config.all_rep_word.items():
        for each in config.all_key_word:  # todo
            # json_data[each] = json_data[each].replace(key, value)
            movie_data.set(each, movie_data.get(each).replace(key, value))

    # 简体时替换的字符
    key_word = []
    if config.title_language == "zh_cn":
        key_word.append("title")
    if config.outline_language == "zh_cn":
        key_word.append("outline")

    for key, value in config.chinese_rep_word.items():
        for each in key_word:  # todo
            # json_data[each] = json_data[each].replace(key, value)
            movie_data.set(each, movie_data.get(each).replace(key, value))

    # 替换标题的上下集信息
    fields_word = ["title", "originaltitle"]
    for field in fields_word:
        for each in config.title_rep:
            # json_data[field] = json_data[field].replace(each, "").strip(":， ").strip()
            movie_data.set(field, movie_data.get(field).replace(each, "").strip(":， ").strip())


def deal_some_field(movie_data: MovieData) -> MovieData:
    fields_rule = config.fields_rule
    actor = movie_data.actor
    title = movie_data.title
    originaltitle = movie_data.originaltitle
    number = movie_data.number

    # 演员处理
    if actor:
        # 去除演员名中的括号
        new_actor_list = []
        actor_list = []
        temp_actor_list = []
        for each_actor in actor.split(","):
            if each_actor and each_actor not in actor_list:
                actor_list.append(each_actor)
                new_actor = re.findall(r"[^\(\)\（\）]+", each_actor)
                if new_actor[0] not in new_actor_list:
                    new_actor_list.append(new_actor[0])
                temp_actor_list.extend(new_actor)
        if "del_char" in fields_rule:
            movie_data.actor = ",".join(new_actor_list)
        else:
            movie_data.actor = ",".join(actor_list)

        # 去除标题后的演员名
        if "del_actor" in fields_rule:
            new_all_actor_name_list = []
            for each_actor in movie_data.actor_amazon + temp_actor_list:
                actor_keyword_list = resources.get_actor_data(each_actor).get(
                    "keyword"
                )  # 获取演员映射表的所有演员别名进行替换
                new_all_actor_name_list.extend(actor_keyword_list)
            for each_actor in set(new_all_actor_name_list):
                try:
                    end_actor = re.compile(rf" {each_actor}$")
                    title = re.sub(end_actor, "", title)
                    originaltitle = re.sub(end_actor, "", originaltitle)
                except:
                    signal.show_traceback_log(traceback.format_exc())
        movie_data.title = title.strip()
        movie_data.originaltitle = originaltitle.strip()

    # 去除标题中的番号
    if number != title and title.startswith(number):
        title = title.replace(number, "").strip()
        movie_data.title = title
    if number != originaltitle and originaltitle.startswith(number):
        originaltitle = originaltitle.replace(number, "").strip()
        movie_data.originaltitle = originaltitle

    # 去除标题中的/
    movie_data.title = movie_data.title.replace("/", "#").strip(" -")
    movie_data.originaltitle = movie_data.originaltitle.replace("/", "#").strip(" -")

    # 去除素人番号前缀数字
    if "del_num" in fields_rule:
        temp_n = re.findall(r"\d{3,}([a-zA-Z]+-\d+)", number)
        if temp_n:
            movie_data.number = temp_n[0]
            movie_data.letters = get_number_letters(movie_data.number)

    if number.endswith("Z"):
        movie_data.number = movie_data.number[:-1] + "z"
    return movie_data


def replace_special_word(movie_data: MovieData):
    # 常见字段替换的字符
    all_key_word = [
        "title",
        "originaltitle",
        "outline",
        "originalplot",
        "series",
        "director",
        "studio",
        "publisher",
        "tag",
    ]
    for key, value in config.special_word.items():
        for each in all_key_word:  # todo
            movie_data.set(each, movie_data.get(each).replace(key, value))


def show_movie_info(movie_data: MovieData):
    if config.show_data_log == "off":  # 调试模式打开时显示详细日志
        return
    for key in config.show_key:
        value = movie_data.get(key)
        if not value:
            continue
        if key == "outline" or key == "originalplot" and len(value) > 100:
            value = str(value)[:98] + "……（略）"
        elif key == "has_sub":
            value = "中文字幕"
        elif key == "actor" and "actor_all," in config.nfo_include_new:
            value = movie_data.all_actor
        LogBuffer.log().write("\n     " + "%-13s" % key + ": " + str(value))
