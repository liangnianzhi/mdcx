import os
import re
import time
import traceback

import langid
from lxml import etree

from models.base.file import delete_file, split_path
from models.base.number import deal_actor_more, get_number_first_letter, get_number_letters
from models.base.utils import convert_path, get_used_time
from models.config.config import config
from models.core.json_data import LogBuffer, ShowData
from models.core.utils import get_new_release
from models.signals import signal


def write_nfo(
    data: ShowData,
    nfo_new_path: str,
    folder_new_path: str,
    file_path: str,
    edit_mode=False,
) -> bool:
    start_time = time.time()
    download_files = config.download_files
    keep_files = config.keep_files
    outline_show = config.outline_show

    if not edit_mode:
        # 读取模式，有nfo，并且没有勾选更新 nfo 信息
        if not data.nfo_can_translate:
            LogBuffer.log().write(f"\n 🍀 Nfo done! (old)({get_used_time(start_time)}s)")
            return True

        # 不下载，不保留时
        if "nfo" not in download_files:
            if "nfo" not in keep_files and os.path.exists(nfo_new_path):
                delete_file(nfo_new_path)
            return True

        # 保留时，返回
        if "nfo" in keep_files and os.path.exists(nfo_new_path):
            LogBuffer.log().write(f"\n 🍀 Nfo done! (old)({get_used_time(start_time)}s)")
            return True

    # 字符转义，避免emby无法解析
    # todo 需进一步处理
    key_word = [
        "title",
        "originaltitle",
        "outline",
        "originalplot",
        "actor",
        "series",
        "director",
        "studio",
        "publisher",
        "tag",
        "website",
        "cover",
        "poster",
        "trailer",
    ]
    rep_word = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&apos;": "'",
        "&quot;": '"',
        "&lsquo;": "「",
        "&rsquo;": "」",
        "&hellip;": "…",
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "'": "&apos;",
        '"': "&quot;",
    }
    for key, value in rep_word.items():
        for each in key_word:
            # 由于使用的是数据类，需要通过setattr设置属性
            setattr(data, each, str(getattr(data, each)).replace(key, value))

    # 获取字段
    nfo_include_new = config.nfo_include_new
    cd_part = data.cd_part
    originaltitle = data.originaltitle
    originalplot = data.originalplot
    title = data.title
    studio = data.studio
    publisher = data.publisher
    year = data.year
    outline = data.outline
    runtime = data.runtime
    director = data.director
    actor = data.actor
    release = data.release
    tag = data.tag
    number = data.number
    cover = data.cover
    poster = data.poster
    website = data.website
    series = data.series
    definition = data.definition
    trailer = data.trailer
    temp_release = get_new_release(release)
    file_full_name = split_path(file_path)[1]
    filename = os.path.splitext(file_full_name)[0]
    temp_4k = ""
    if definition == "8K" or definition == "UHD8" or definition == "4K" or definition == "UHD":
        temp_4k = definition.replace("UHD8", "UHD")

    # 获取在媒体文件中显示的规则，不需要过滤Windows异常字符
    # 国产使用title作为number会出现重复，此处去除title，避免重复(需要注意titile繁体情况)
    nfo_title = config.naming_media
    if not number:
        number = title
    # 默认emby视频标题配置为 [number title]，国产重复时需去掉一个，去重需注意空格也应一起去掉，否则国产的nfo标题中会多一个空格
    # 读取nfo title信息会去掉前面的number和空格以保留title展示出来，同时number和标题一致时，去掉number的逻辑变成去掉整个标题导致读取失败，见426行
    if number == title and "number" in nfo_title and "title" in nfo_title:
        nfo_title = nfo_title.replace("originaltitle", "").replace("title", "").strip()
    first_letter = get_number_first_letter(number)

    # 处理演员
    first_actor = actor.split(",").pop(0)
    temp_all_actor = deal_actor_more(data.all_actor)
    temp_actor = deal_actor_more(actor)

    repl_list = [
        ["4K", temp_4k],
        ["originaltitle", originaltitle],
        ["title", title],
        ["outline", outline],
        ["number", number],
        ["first_actor", first_actor],
        ["all_actor", temp_all_actor],
        ["actor", temp_actor],
        ["release", temp_release],
        ["year", year],
        ["runtime", runtime],
        ["director", director],
        ["series", series],
        ["studio", studio],
        ["publisher", publisher],
        ["mosaic", data.mosaic],
        ["definition", definition.replace("UHD8", "UHD")],
        ["cnword", data.c_word],
        ["first_letter", first_letter],
        ["letters", data.letters],
        ["filename", filename],
        ["wanted", data.wanted],
    ]
    for each_key in repl_list:
        nfo_title = nfo_title.replace(each_key[0], each_key[1])

    tag = re.split(r"[,，]", tag)  # tag str转list

    try:
        if not os.path.exists(folder_new_path):
            os.makedirs(folder_new_path)
        delete_file(nfo_new_path)  # 避免115出现重复文件
        with open(nfo_new_path, "w", encoding="UTF-8") as code:
            print('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>', file=code)
            print("<movie>", file=code)

            # 输出剧情简介
            if outline:
                outline = outline.replace("\n", "<br>")
                if originalplot and originalplot != outline:
                    if "show_zh_jp" in outline_show:
                        outline += f"<br>  <br>{originalplot}"
                    elif "show_jp_zh" in outline_show:
                        outline = f"{originalplot}<br>  <br>{outline}"
                    outline_from = data.outline_from.capitalize().replace("Youdao", "有道")
                    if "show_from" in outline_show and outline_from:
                        outline += f"<br>  <br>由 {outline_from} 提供翻译"
                if "outline_no_cdata," in nfo_include_new:
                    temp_outline = outline.replace("<br>", "")
                    if "plot_," in nfo_include_new:
                        print(f"  <plot>{temp_outline}</plot>", file=code)
                    if "outline," in nfo_include_new:
                        print(f"  <outline>{temp_outline}</outline>", file=code)
                else:
                    if "plot_," in nfo_include_new:
                        print("  <plot><![CDATA[" + outline + "]]></plot>", file=code)
                    if "outline," in nfo_include_new:
                        print("  <outline><![CDATA[" + outline + "]]></outline>", file=code)

            # 输出日文剧情简介
            if originalplot and "originalplot," in nfo_include_new:
                originalplot = originalplot.replace("\n", "<br>")
                if "outline_no_cdata," in nfo_include_new:
                    temp_originalplot = originalplot.replace("<br>", "")
                    print(f"  <originalplot>{temp_originalplot}</originalplot>", file=code)
                else:
                    print("  <originalplot><![CDATA[" + originalplot + "]]></originalplot>", file=code)

            # 输出发行日期
            if release:
                nfo_tagline = config.nfo_tagline.replace("release", release)
                if nfo_tagline:
                    print("  <tagline>" + nfo_tagline + "</tagline>", file=code)
                if "premiered," in nfo_include_new:
                    print("  <premiered>" + release + "</premiered>", file=code)
                if "releasedate," in nfo_include_new:
                    print("  <releasedate>" + release + "</releasedate>", file=code)
                if "release_," in nfo_include_new:
                    print("  <release>" + release + "</release>", file=code)

            # 输出番号
            print("  <num>" + number + "</num>", file=code)

            # 输出标题
            if cd_part and "title_cd," in nfo_include_new:
                nfo_title += " " + cd_part[1:].upper()
            print("  <title>" + nfo_title + "</title>", file=code)

            # 输出原标题
            if "originaltitle," in nfo_include_new:
                if number != title:
                    print("  <originaltitle>" + number + " " + originaltitle + "</originaltitle>", file=code)
                else:
                    print("  <originaltitle>" + originaltitle + "</originaltitle>", file=code)

            # 输出类标题
            if "sorttitle," in nfo_include_new:
                if cd_part:
                    originaltitle += " " + cd_part[1:].upper()
                if number != title:
                    print("  <sorttitle>" + number + " " + originaltitle + "</sorttitle>", file=code)
                else:
                    print("  <sorttitle>" + number + "</sorttitle>", file=code)

            # 输出国家和分级
            try:
                country = data.country
            except:
                if re.findall(r"\.\d{2}\.\d{2}\.\d{2}", number):
                    country = "US"
                else:
                    country = "JP"

            # 输出家长分级
            if "mpaa," in nfo_include_new:
                if country == "JP":
                    print("  <mpaa>JP-18+</mpaa>", file=code)
                else:
                    print("  <mpaa>NC-17</mpaa>", file=code)

            # 输出自定义分级
            if "customrating," in nfo_include_new:
                if country == "JP":
                    print("  <customrating>JP-18+</customrating>", file=code)
                else:
                    print("  <customrating>NC-17</customrating>", file=code)

            # 输出国家
            if "country," in nfo_include_new:
                print(f"  <countrycode>{country}</countrycode>", file=code)

            # 初始化 actor_list
            actor_list = []
            # 输出男女演员
            if "actor_all," in nfo_include_new:
                actor = data.all_actor
            # 有演员时输出演员
            if "actor," in nfo_include_new:
                if not actor:
                    actor = config.actor_no_name
                actor_list = actor.split(",")  # 字符串转列表
                actor_list = [actor.strip() for actor in actor_list if actor.strip()]  # 去除空白
            if actor_list:
                for each in actor_list:
                    print("  <actor>", file=code)
                    print("    <name>" + each + "</name>", file=code)
                    print("    <type>Actor</type>", file=code)
                    print("  </actor>", file=code)

            # 输出导演
            if director and "director," in nfo_include_new:
                print("  <director>" + director + "</director>", file=code)

            # 输出公众评分、影评人评分
            try:
                if data.score:
                    score = float(data.score)
                    if "score," in nfo_include_new:
                        print("  <rating>" + str(score) + "</rating>", file=code)
                    if "criticrating," in nfo_include_new:
                        print("  <criticrating>" + str(int(score * 10)) + "</criticrating>", file=code)
            except:
                print(traceback.format_exc())

            # 输出我想看人数
            try:
                if data.wanted and "wanted," in nfo_include_new:
                    print("  <votes>" + data.wanted + "</votes>", file=code)
            except:
                pass

            # 输出年代
            if str(year) and "year," in nfo_include_new:
                print("  <year>" + str(year) + "</year>", file=code)

            # 输出时长
            if str(runtime) and "runtime," in nfo_include_new:
                print("  <runtime>" + str(runtime).replace(" ", "") + "</runtime>", file=code)

            # 输出合集(使用演员)
            if "actor_set," in nfo_include_new and actor and actor != "未知演员" and actor != "未知演員":
                actor_list = actor.split(",")  # 字符串转列表
                actor_list = [actor.strip() for actor in actor_list if actor.strip()]  # 去除空白
                if actor_list:
                    for each in actor_list:
                        print("  <set>", file=code)
                        print("    <name>" + each + "</name>", file=code)
                        print("  </set>", file=code)

            # 输出合集(使用系列)
            if "series_set," in nfo_include_new and series:
                print("  <set>", file=code)
                print("    <name>" + series + "</name>", file=code)
                print("  </set>", file=code)

            # 输出系列
            if series:
                if "series," in nfo_include_new:
                    print("  <series>" + series + "</series>", file=code)

            # 输出片商/制作商
            if studio:
                if "studio," in nfo_include_new:
                    print("  <studio>" + studio + "</studio>", file=code)
                if "maker," in nfo_include_new:
                    print("  <maker>" + studio + "</maker>", file=code)

            # 输出发行商 label（厂牌/唱片公司） publisher（发行商）
            if publisher:
                if "publisher," in nfo_include_new:
                    print("  <publisher>" + publisher + "</publisher>", file=code)
                if "label," in nfo_include_new:
                    print("  <label>" + publisher + "</label>", file=code)

            # 输出 tag
            if tag and "tag," in nfo_include_new:
                try:
                    for i in tag:
                        if i:
                            print("  <tag>" + i + "</tag>", file=code)
                except:
                    signal.show_log_text(traceback.format_exc())

            # 输出 genre
            if tag and "genre," in nfo_include_new:
                try:
                    for i in tag:
                        if i:
                            print("  <genre>" + i + "</genre>", file=code)
                except:
                    signal.show_log_text(traceback.format_exc())

            # 输出封面地址
            if poster and "poster," in nfo_include_new:
                print("  <poster>" + poster + "</poster>", file=code)

            # 输出背景地址
            if cover and "cover," in nfo_include_new:
                print("  <cover>" + cover + "</cover>", file=code)

            # 输出预告片
            if trailer and "trailer," in nfo_include_new:
                print("  <trailer>" + trailer + "</trailer>", file=code)

            # 输出网页地址
            if website and "website," in nfo_include_new:
                print("  <website>" + website + "</website>", file=code)

            # javdb id 输出, 没有时使用番号搜索页
            if "国产" not in data.mosaic and "國產" not in data.mosaic:
                if data.javdbid:
                    print("  <javdbid>" + data.javdbid + "</javdbid>", file=code)
                else:
                    print("  <javdbsearchid>" + number + "</javdbsearchid>", file=code)
            print("</movie>", file=code)
            LogBuffer.log().write(f"\n 🍀 Nfo done! (new)({get_used_time(start_time)}s)")
            return True
    except Exception as e:
        LogBuffer.log().write(f"\n 🔴 Nfo failed! \n     {str(e)}")
        signal.show_traceback_log(traceback.format_exc())
        signal.show_log_text(traceback.format_exc())
        return False


def get_nfo_data(appoint_number: str, file_path: str, movie_number: str) -> tuple[bool, ShowData]:
    nfo_data = ShowData()  # 使用新的数据类创建函数
    local_nfo_path = os.path.splitext(file_path)[0] + ".nfo"
    local_nfo_name = split_path(local_nfo_path)[1]
    file_folder = split_path(file_path)[0]
    nfo_data.source = "nfo"
    LogBuffer.req().write(local_nfo_path)
    nfo_data.poster_from = "local"
    nfo_data.cover_from = "local"
    nfo_data.extrafanart_from = "local"
    nfo_data.trailer_from = "local"

    if not os.path.exists(local_nfo_path):
        LogBuffer.error().write("nfo文件不存在")
        LogBuffer.req().write("do_not_update_json_data_dic")
        nfo_data.outline = split_path(file_path)[1]
        nfo_data.tag = file_path
        return False, nfo_data

    with open(local_nfo_path, encoding="utf-8") as f:
        content = f.read().replace("<![CDATA[", "").replace("]]>", "")

    parser = etree.HTMLParser(encoding="utf-8")
    xml_nfo = etree.HTML(content.encode("utf-8"), parser)

    title = "".join(xml_nfo.xpath("//title/text()"))
    # 获取不到标题，表示xml错误，重新刮削
    if not title:
        LogBuffer.error().write("nfo文件损坏")
        LogBuffer.req().write("do_not_update_json_data_dic")
        nfo_data.outline = split_path(file_path)[1]
        nfo_data.tag = file_path
        return False, nfo_data
    title = re.sub(r" (CD)?\d{1}$", "", title)

    # 获取其他数据
    originaltitle = "".join(xml_nfo.xpath("//originaltitle/text()"))
    if appoint_number:
        number = appoint_number
    else:
        number = "".join(xml_nfo.xpath("//num/text()"))
        if not number:
            number = movie_number
    nfo_data.letters = get_number_letters(number)
    title = title.replace(number + " ", "").strip()
    originaltitle = originaltitle.replace(number + " ", "").strip()
    originaltitle_amazon = originaltitle
    if originaltitle:
        for key, value in config.special_word.items():
            originaltitle_amazon = originaltitle_amazon.replace(value, key)
    nfo_data.actor = ",".join(xml_nfo.xpath("//actor/name/text()"))
    originalplot = "".join(xml_nfo.xpath("//originalplot/text()"))
    outline = ""
    temp_outline = re.findall(r"<plot>(.+)</plot>", content)
    if not temp_outline:
        temp_outline = re.findall(r"<outline>(.+)</outline>", content)
    if temp_outline:
        outline = temp_outline[0]
        if "<br>  <br>" in outline:
            temp_from = re.findall(r"<br>  <br>由 .+ 提供翻译", outline)
            if temp_from:
                outline = outline.replace(temp_from[0], "")
                nfo_data.outline_from = temp_from[0].replace("<br>  <br>由 ", "").replace(" 提供翻译", "")
            outline = outline.replace(originalplot, "").replace("<br>  <br>", "")
    tag = ",".join(xml_nfo.xpath("//tag/text()"))
    release = "".join(xml_nfo.xpath("//release/text()"))
    if not release:
        release = "".join(xml_nfo.xpath("//releasedate/text()"))
    if not release:
        release = "".join(xml_nfo.xpath("//premiered/text()"))
    if release:
        release = release.replace("/", "-").strip(". ")
        if len(release) < 10:
            release_list = re.findall(r"(\d{4})-(\d{1,2})-(\d{1,2})", release)
            if release_list:
                r_year, r_month, r_day = release_list[0]
                r_month = "0" + r_month if len(r_month) == 1 else r_month
                r_day = "0" + r_day if len(r_day) == 1 else r_day
                release = r_year + "-" + r_month + "-" + r_day
    nfo_data.release = release
    nfo_data.year = "".join(xml_nfo.xpath("//year/text()"))
    nfo_data.runtime = "".join(xml_nfo.xpath("//runtime/text()"))
    score = "".join(xml_nfo.xpath("//rating/text()"))
    if not score:
        score = "".join(xml_nfo.xpath("//rating/text()"))
        if score:
            score = str(int(score) / 10)
    nfo_data.series = "".join(xml_nfo.xpath("//series/text()"))
    nfo_data.director = "".join(xml_nfo.xpath("//director/text()"))
    studio = "".join(xml_nfo.xpath("//studio/text()"))
    if not studio:
        studio = "".join(xml_nfo.xpath("//maker/text()"))
    publisher = "".join(xml_nfo.xpath("//publisher/text()"))
    if not publisher:
        publisher = "".join(xml_nfo.xpath("//label/text()"))
    nfo_data.cover = "".join(xml_nfo.xpath("//cover/text()")).replace("&amp;", "&")
    nfo_data.poster = "".join(xml_nfo.xpath("//poster/text()")).replace("&amp;", "&")
    nfo_data.trailer = "".join(xml_nfo.xpath("//trailer/text()")).replace("&amp;", "&")
    nfo_data.website = "".join(xml_nfo.xpath("//website/text()")).replace("&amp;", "&")
    nfo_data.wanted = "".join(xml_nfo.xpath("//votes/text()"))

    # 判断马赛克
    if "国产" in tag or "國產" in tag:
        nfo_data.mosaic = "国产"
    elif "破解" in tag:
        nfo_data.mosaic = "无码破解"
    elif "有码" in tag or "有碼" in tag:
        nfo_data.mosaic = "有码"
    elif "流出" in tag:
        nfo_data.mosaic = "流出"
    elif "无码" in tag or "無碼" in tag or "無修正" in tag:
        nfo_data.mosaic = "无码"
    elif "里番" in tag or "裏番" in tag:
        nfo_data.mosaic = "里番"
    elif "动漫" in tag or "動漫" in tag:
        nfo_data.mosaic = "动漫"

    # 获取只有标签的标签（因为启用字段翻译后，会再次重复添加字幕、演员、发行、系列等字段）
    replace_keys = set(filter(None, ["：", ":"] + re.split(r"[,，]", nfo_data.actor)))
    temp_tag_list = list(filter(None, re.split(r"[,，]", tag.replace("中文字幕", ""))))
    only_tag_list = temp_tag_list.copy()
    for each_tag in temp_tag_list:
        for each_key in replace_keys:
            if each_key in each_tag:
                only_tag_list.remove(each_tag)
                break
    nfo_data.tag_only = ",".join(only_tag_list)

    # 获取本地图片路径
    poster_path_1 = convert_path(os.path.splitext(file_path)[0] + "-poster.jpg")
    poster_path_2 = convert_path(os.path.join(file_folder, "poster.jpg"))
    thumb_path_1 = convert_path(os.path.splitext(file_path)[0] + "-thumb.jpg")
    thumb_path_2 = convert_path(os.path.join(file_folder, "thumb.jpg"))
    fanart_path_1 = convert_path(os.path.splitext(file_path)[0] + "-fanart.jpg")
    fanart_path_2 = convert_path(os.path.join(file_folder, "fanart.jpg"))
    if os.path.isfile(poster_path_1):
        poster_path = poster_path_1
    elif os.path.isfile(poster_path_2):
        poster_path = poster_path_2
    else:
        poster_path = ""
    if os.path.isfile(thumb_path_1):
        thumb_path = thumb_path_1
    elif os.path.isfile(thumb_path_2):
        thumb_path = thumb_path_2
    else:
        thumb_path = ""
    if os.path.isfile(fanart_path_1):
        fanart_path = fanart_path_1
    elif os.path.isfile(fanart_path_2):
        fanart_path = fanart_path_2
    else:
        fanart_path = ""

    # 返回数据
    nfo_data.title = title
    if config.title_language == "jp" and "read_translate_again" in config.read_mode and originaltitle:
        nfo_data.title = originaltitle
    nfo_data.originaltitle = originaltitle
    if originaltitle and langid.classify(originaltitle)[0] == "ja":
        nfo_data.originaltitle_amazon = originaltitle
        if nfo_data.actor:
            nfo_data.actor_amazon = nfo_data.actor.split(",")
    nfo_data.number = number
    nfo_data.all_actor = nfo_data.actor
    nfo_data.outline = outline
    if config.outline_language == "jp" and "read_translate_again" in config.read_mode and originalplot:
        nfo_data.outline = originalplot
    nfo_data.originalplot = originalplot
    nfo_data.tag = tag
    nfo_data.score = score
    nfo_data.studio = studio
    nfo_data.publisher = publisher
    if nfo_data.cover:
        nfo_data.cover_list.append(("local", nfo_data.cover))
    nfo_data.poster_path = poster_path
    nfo_data.thumb_path = thumb_path
    nfo_data.fanart_path = fanart_path
    LogBuffer.log().write(f"\n 📄 [NFO] {local_nfo_name}")
    signal.show_traceback_log(f"{number} {nfo_data.mosaic}")
    return True, nfo_data
