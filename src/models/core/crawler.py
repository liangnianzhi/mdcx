"""
爬虫控制, 调用 models.crawlers 中各个网站爬虫
"""

import re
from typing import Any, Callable

import langid

from models.base.number import get_number_letters, is_uncensored
from models.config.config import config
from models.core.flags import Flags
from models.core.json_data import InputInfo, LogBuffer
from models.crawlers import (
    airav,
    airav_cc,
    avsex,
    avsox,
    cableav,
    cnmdb,
    dahlia,
    dmm,
    faleno,
    fantastica,
    fc2,
    fc2club,
    fc2hub,
    freejavbt,
    getchu,
    getchu_dmm,
    giga,
    hdouban,
    hscangku,
    iqqtv_new,
    jav321,
    javbus,
    javday,
    javdb,
    javlibrary_new,
    kin8,
    love6,
    lulubar,
    madouqu,
    mdtv,
    mgstage,
    mmtv,
    mywife,
    official,
    prestige,
    theporndb,
    xcity,
)
from models.data_models import CrawlerResult, FileMode, FinalResult, MovieData


# used by _call_crawlers and _call_specific_crawler
def _call_crawler(
    appoint_number: str,
    appoint_url: str,
    file_path: str,
    website: str,
    language: str,
    file_number: str,
    short_number: str,
    mosaic: str,
    org_language: str,
) -> CrawlerResult:
    """
    获取某个网站数据
    """
    # 259LUXU-1111， mgstage 和 avsex 之外使用 LUXU-1111（素人番号时，short_number有值，不带前缀数字；反之，short_number为空)
    if short_number and website != "mgstage" and website != "avsex":
        file_number = short_number
    _: dict[str, Callable] = {
        "official": official.main,
        "iqqtv": iqqtv_new.main,
        "avsex": avsex.main,
        "airav_cc": airav_cc.main,
        "airav": airav.main,
        "freejavbt": freejavbt.main,
        "javbus": javbus.main,
        "javdb": javdb.main,
        "jav321": jav321.main,
        "dmm": dmm.main,
        "javlibrary": javlibrary_new.main,
        "xcity": xcity.main,
        "avsox": avsox.main,
        "mgstage": mgstage.main,
        "7mmtv": mmtv.main,
        "fc2": fc2.main,
        "fc2hub": fc2hub.main,
        "fc2club": fc2club.main,
        "mdtv": mdtv.main,
        "madouqu": madouqu.main,
        "hscangku": hscangku.main,
        "cableav": cableav.main,
        "getchu": getchu.main,
        "getchu_dmm": getchu_dmm.main,
        "mywife": mywife.main,
        "giga": giga.main,
        "hdouban": hdouban.main,
        "lulubar": lulubar.main,
        "love6": love6.main,
        "cnmdb": cnmdb.main,
        "faleno": faleno.main,
        "fantastica": fantastica.main,
        "theporndb": theporndb.main,
        "dahlia": dahlia.main,
        "prestige": prestige.main,
        "kin8": kin8.main,
        "javday": javday.main,
    }
    if website == "official":
        res = official.main(file_number, appoint_url, language)
    elif website == "iqqtv":
        res = iqqtv_new.main(file_number, appoint_url, language)
    elif website == "avsex":
        res = avsex.main(file_number, appoint_url, language)
    elif website == "airav_cc":
        res = airav_cc.main(file_number, appoint_url, language)
    elif website == "airav":
        res = airav.main(file_number, appoint_url, language)
    elif website == "freejavbt":
        res = freejavbt.main(file_number, appoint_url, language)
    elif website == "javbus":
        res = javbus.main(file_number, appoint_url, language, mosaic)
    elif website == "javdb":
        res = javdb.main(file_number, appoint_url, language, org_language)
    elif website == "jav321":
        res = jav321.main(file_number, appoint_url, language)
    elif website == "dmm":
        res = dmm.main(file_number, appoint_url, language, file_path)
    elif website == "javlibrary":
        res = javlibrary_new.main(file_number, appoint_url, language)
    elif website == "xcity":
        res = xcity.main(file_number, appoint_url, language)
    elif website == "avsox":
        res = avsox.main(file_number, appoint_url, language)
    elif website == "mgstage":
        res = mgstage.main(file_number, appoint_url, language, short_number)
    elif website == "7mmtv":
        res = mmtv.main(file_number, appoint_url, language, file_path)
    elif website == "fc2":
        res = fc2.main(file_number, appoint_url, language)
    elif website == "fc2hub":
        res = fc2hub.main(file_number, appoint_url, language)
    elif website == "fc2club":
        res = fc2club.main(file_number, appoint_url, language)
    elif website == "mdtv":
        res = mdtv.main(file_number, appoint_url, language, file_path, appoint_number)
    elif website == "madouqu":
        res = madouqu.main(file_number, appoint_url, language, file_path, appoint_number)
    elif website == "hscangku":
        res = hscangku.main(file_number, appoint_url, language, file_path, appoint_number)
    elif website == "cableav":
        res = cableav.main(file_number, appoint_url, language, file_path, appoint_number)
    elif website == "getchu":
        res = getchu.main(file_number, appoint_url, language)
    elif website == "getchu_dmm":
        res = getchu_dmm.main(file_number, appoint_url, language)
    elif website == "mywife":
        res = mywife.main(file_number, appoint_url, language)
    elif website == "giga":
        res = giga.main(file_number, appoint_url, language)
    elif website == "hdouban":
        res = hdouban.main(file_number, appoint_url, language, file_path, appoint_number, mosaic)
    elif website == "lulubar":
        res = lulubar.main(file_number, appoint_url, language)
    elif website == "love6":
        res = love6.main(file_number, appoint_url, language)
    elif website == "cnmdb":
        res = cnmdb.main(file_number, appoint_url, language, file_path, appoint_number)
    elif website == "faleno":
        res = faleno.main(file_number, appoint_url, language)
    elif website == "fantastica":
        res = fantastica.main(file_number, appoint_url, language)
    elif website == "theporndb":
        res = theporndb.main(file_number, appoint_url, language, file_path)
    elif website == "dahlia":
        res = dahlia.main(file_number, appoint_url, language)
    elif website == "prestige":
        res = prestige.main(file_number, appoint_url, language)
    elif website == "kin8":
        res = kin8.main(file_number, appoint_url, language)
    elif website == "javday":
        res = javday.main(file_number, appoint_url, language)
    else:
        res = javdb.main(file_number, appoint_url, language)

    res.site = website
    return res


# used by _decide_websites
def _call_crawlers(
    all_res: dict[str, CrawlerResult],
    input_info: InputInfo,  # input
    final_res: FinalResult,  # output
    website_list: list[str],
    field_name: str,
    field_cnname: str,
    field_language: str,
    config: Any,
    file_number: str,
    short_number: str,
    mosaic: str,
) -> None:
    """
    按照设置的网站顺序获取各个字段信息
    """
    if "official" in config.website_set and field_name not in ["title", "title_zh", "outline_zh", "wanted", "score"]:
        website_list.insert(0, "official")

    backup_data = {}
    backup_website = ""
    for website in website_list:
        if (
            (website in ["avsox", "mdtv"] and mosaic in ["有码", "无码破解", "流出", "里番", "动漫"])
            or (website == "mdtv" and mosaic == "无码")
        ) and field_name != "title":
            continue

        title_language = "jp"
        if field_name in ["title_zh", "outline_zh"]:
            title_language = "zh_cn"
            field_name = field_name.replace("_zh", "")
        elif field_name in ["originaltitle", "originalplot", "trailer", "wanted"]:
            title_language = "jp"
        elif website in ["airav_cc", "iqqtv", "airav", "avsex", "javlibrary", "mdtv", "madouqu", "lulubar"]:
            title_language = getattr(config, field_language)

        site_res = all_res.get(website, None) or _call_crawler(
            input_info["appoint_number"],
            input_info["appoint_url"],
            input_info["file_path"],
            website,
            title_language,
            file_number,
            short_number,
            mosaic,
            config.title_language,
        )
        all_res[website] = site_res

        if not site_res.success:
            continue

        if field_cnname == "标题":
            final_res.update(site_res.data)

        # 判断是否有可用数据
        if not (site_res.data.title and site_res.data.get(field_name)):
            continue

        # 保存备用数据
        if not len(backup_data):
            backup_data.update(site_res.data.__dict__)
            backup_website = website

        # 如果是标题字段，更新来源信息
        if field_cnname == "标题":
            final_res.metadata.outline_from = website
            final_res.metadata.poster_from = website
            final_res.metadata.cover_from = website
            final_res.metadata.extrafanart_from = website
            final_res.metadata.trailer_from = website

        # 处理语言检测逻辑
        should_skip = False
        if config.scrape_like != "speed":
            if website in ["airav_cc", "iqqtv", "airav", "avsex", "javlibrary", "lulubar"] and field_name in [
                "title",
                "outline",
                "originaltitle",
                "originalplot",
            ]:
                detected_lang = langid.classify(site_res.data.get(field_name))[0]
                if detected_lang != "ja" and title_language == "jp":
                    LogBuffer.info().write(
                        f"\n    🔴 {field_cnname} 检测为非日文，跳过！({website})\n     ↳ {site_res.data.get(field_name)}"
                    )
                    should_skip = True
                elif detected_lang == "ja" and title_language != "jp":
                    LogBuffer.info().write(
                        f"\n    🔴 {field_cnname} 检测为日文，跳过！({website})\n     ↳ {site_res.data.get(field_name)}"
                    )
                    should_skip = True
            elif website == "official":
                website = site_res.data.source

        if should_skip:
            continue

        # 标记获取成功并返回
        LogBuffer.info().write(
            f"\n    🟢 {field_cnname} 获取成功！({website})\n     ↳ {site_res.data.get(field_name)} "
        )
        return

    if len(backup_data):
        LogBuffer.info().write(
            f"\n    🟢 {field_cnname} 使用备用数据！({backup_website})\n     ↳ {backup_data[field_name]} "
        )
        if field_cnname == "标题":
            input_info.update(backup_data)
    else:
        LogBuffer.info().write(f"\n    🔴 {field_cnname} 获取失败！")


# used by _crawl
def _call_specific_crawler(input_info: InputInfo, final_res: FinalResult, website: str) -> FinalResult:
    file_number = input_info["number"]
    short_number = input_info["short_number"]
    mosaic = input_info["mosaic"]
    final_res.metadata.fields_info = ""

    title_language = config.title_language
    org_language = title_language
    if website not in ["airav_cc", "iqqtv", "airav", "avsex", "javlibrary", "mdtv", "madouqu", "lulubar"]:
        title_language = "jp"
    elif website == "mdtv":
        title_language = "zh_cn"
    site_res = _call_crawler(
        input_info["appoint_number"],
        input_info["appoint_url"],
        input_info["file_path"],
        website,
        title_language,
        file_number,
        short_number,
        mosaic,
        org_language,
    )
    if not site_res.success:
        return final_res
    final_res.update(site_res.data)
    if not input_info["title"]:
        return final_res
    if site_res.data.cover:
        final_res.metadata.cover_list = [(website, site_res.data.cover)]

    # 加入来源信息
    final_res.metadata.outline_from = website
    final_res.metadata.poster_from = website
    final_res.metadata.cover_from = website
    final_res.metadata.extrafanart_from = website
    final_res.metadata.trailer_from = website
    final_res.metadata.fields_info = f"\n 🌐 [website] {LogBuffer.req().get().strip('-> ')}"

    if short_number:
        final_res.data.number = file_number

    final_res.metadata.actor_amazon = list(set(site_res.data.actor.split(",")))
    final_res.data.all_actor = input_info["all_actor"] if input_info.get("all_actor") else site_res.data.actor
    final_res.data.all_actor_photo = (
        input_info["all_actor_photo"] if input_info.get("all_actor_photo") else site_res.data.actor_photo
    )

    return final_res


# used by _decide_websites
def _deal_each_field(
    all_json_data: dict[str, CrawlerResult],
    input_info: InputInfo,
    final_res: FinalResult,
    website_list: list[str],
    field_name: str,
    field_cnname: str,
    field_language: str,
    config: Any,
) -> None:
    """
    按照设置的网站顺序处理字段
    """
    if config.scrape_like == "speed":
        website_list = [input_info["source"]]

    elif "official" in config.website_set:
        if all_json_data["official"].data.title:
            if field_name not in ["title", "originaltitle", "outline", "originalplot", "wanted", "score"]:
                website_list.insert(0, all_json_data["official"].data.source)

    if not website_list:
        return

    backup_data = None
    LogBuffer.info().write(
        f"\n\n    🙋🏻‍ {field_cnname} \n    ====================================\n    🌐 来源优先级：{' -> '.join(website_list)}"
    )
    backup_website = ""
    title_language = getattr(config, field_language, "jp")
    for website in website_list:
        if website not in ["airav_cc", "iqqtv", "airav", "avsex", "javlibrary", "mdtv", "madouqu", "lulubar"]:
            title_language = "jp"
        elif (
            field_name == "originaltitle"
            or field_name == "originalplot"
            or field_name == "trailer"
            or field_name == "wanted"
        ):
            title_language = "jp"
        try:
            web_data_json = all_json_data[website].data
        except:
            continue

        if web_data_json.title and web_data_json.get(field_name):
            if backup_data is None:
                backup_data = web_data_json.get(field_name)
                backup_website = website

            if config.scrape_like != "speed":
                if field_name in ["title", "outline", "originaltitle", "originalplot"]:
                    if website in ["airav_cc", "iqqtv", "airav", "avsex", "javlibrary", "lulubar"]:
                        if langid.classify(web_data_json.get(field_name))[0] != "ja":
                            if title_language == "jp":
                                LogBuffer.info().write(f"\n    🔴 {website} (失败，检测为非日文，跳过！)")
                                continue
                        elif title_language != "jp":
                            LogBuffer.info().write(f"\n    🔴 {website} (失败，检测为日文，跳过！)")
                            continue
            if field_name == "poster":
                final_res.metadata.poster_from = website
                final_res.data.image_download = web_data_json.image_download
            elif field_name == "cover":
                final_res.metadata.cover_from = website
            elif field_name == "extrafanart":
                final_res.metadata.extrafanart_from = website
            elif field_name == "trailer":
                final_res.metadata.trailer_from = website
            elif field_name == "outline":
                final_res.metadata.outline_from = website
            elif field_name == "actor":
                final_res.data.all_actor = input_info.get("all_actor") or web_data_json.actor
                final_res.data.all_actor_photo = input_info.get("all_actor_photo") or web_data_json.actor_photo
            elif field_name == "originaltitle":
                if web_data_json.actor:
                    final_res.metadata.amazon_orginaltitle_actor = web_data_json.actor.split(",")[0]
            final_res.data.set(field_name, web_data_json.get(field_name))
            final_res.metadata.fields_info += "\n     " + "%-13s" % field_name + f": {website} ({title_language})"
            LogBuffer.info().write(f"\n    🟢 {website} (成功)\n     ↳ {input_info[field_name]}")
            break
        else:
            LogBuffer.info().write(f"\n    🔴 {website} (失败)")
    else:
        if backup_data is not None:
            final_res.data.set(field_name, backup_data)
            final_res.metadata.fields_info += "\n     " + f"{field_name:<13}" + f": {backup_website} ({title_language})"
            LogBuffer.info().write(f"\n    🟢 {backup_website} (使用备用数据)\n     ↳ {backup_data}")
        else:
            final_res.metadata.fields_info += "\n     " + f"{field_name:<13}" + f": {'-----'} ({'not found'})"


# used by _crawl
def _crawl_websites(
    input_info: InputInfo,
    final_res: FinalResult,
    number_website_list: list[str],
) -> FinalResult:
    """
    获取一组网站的数据：按照设置的网站组，请求各字段数据，并返回最终的数据
    """
    file_number = input_info["number"]
    short_number = input_info["short_number"]
    scrape_like = config.scrape_like
    none_fields = config.none_fields  # 不刮削的字段

    # 获取使用的网站
    title_jp_website_list = config.title_website.split(",")
    title_zh_website_list = config.title_zh_website.split(",")
    outline_jp_website_list = config.outline_website.split(",")
    outline_zh_website_list = config.outline_zh_website.split(",")
    actor_website_list = config.actor_website.split(",")
    thumb_website_list = config.thumb_website.split(",")
    poster_website_list = config.poster_website.split(",")
    extrafanart_website_list = config.extrafanart_website.split(",")
    trailer_website_list = config.trailer_website.split(",")
    tag_website_list = config.tag_website.split(",")
    release_website_list = config.release_website.split(",")
    runtime_website_list = config.runtime_website.split(",")
    score_website_list = config.score_website.split(",")
    director_website_list = config.director_website.split(",")
    series_website_list = config.series_website.split(",")
    studio_website_list = config.studio_website.split(",")
    publisher_website_list = config.publisher_website.split(",")
    wanted_website_list = config.wanted_website.split(",")
    title_jp_website_new_list = _get_new_website_list(
        title_jp_website_list, number_website_list, file_number, short_number, "title"
    )
    title_zh_website_new_list = _get_new_website_list(
        title_zh_website_list, number_website_list, file_number, short_number, "title_zh"
    )
    outline_jp_website_new_list = _get_new_website_list(
        outline_jp_website_list, number_website_list, file_number, short_number, "outline"
    )
    outline_zh_website_new_list = _get_new_website_list(
        outline_zh_website_list, number_website_list, file_number, short_number, "outline_zh"
    )
    actor_website_new_list = _get_new_website_list(
        actor_website_list, number_website_list, file_number, short_number, "actor"
    )
    thumb_website_new_list = _get_new_website_list(
        thumb_website_list, number_website_list, file_number, short_number, "thumb"
    )
    poster_website_new_list = _get_new_website_list(
        poster_website_list, number_website_list, file_number, short_number, "poster"
    )
    extrafanart_website_new_list = _get_new_website_list(
        extrafanart_website_list, number_website_list, file_number, short_number, "extrafanart"
    )
    trailer_website_new_list = _get_new_website_list(
        trailer_website_list, number_website_list, file_number, short_number, "trailer"
    )
    tag_website_new_list = _get_new_website_list(
        tag_website_list, number_website_list, file_number, short_number, "tag"
    )
    release_website_new_list = _get_new_website_list(
        release_website_list, number_website_list, file_number, short_number, "release"
    )
    runtime_website_new_list = _get_new_website_list(
        runtime_website_list, number_website_list, file_number, short_number, "runtime"
    )
    score_website_new_list = _get_new_website_list(
        score_website_list, number_website_list, file_number, short_number, "score"
    )
    director_website_new_list = _get_new_website_list(
        director_website_list, number_website_list, file_number, short_number, "director"
    )
    series_website_new_list = _get_new_website_list(
        series_website_list, number_website_list, file_number, short_number, "series"
    )
    studio_website_new_list = _get_new_website_list(
        studio_website_list, number_website_list, file_number, short_number, "studio"
    )
    publisher_website_new_list = _get_new_website_list(
        publisher_website_list, number_website_list, file_number, short_number, "publisher"
    )
    wanted_website_new_list = _get_new_website_list(
        wanted_website_list, number_website_list, file_number, short_number, "wanted"
    )

    # 初始化变量
    all_res: dict[str, CrawlerResult] = {}

    # 生成各字段及请求网站列表，并请求数据
    if scrape_like == "speed":
        request_field_list = [("title", "标题", "title_language", number_website_list)]
    else:
        if "official" in config.website_set:
            title_jp_website_new_list.insert(0, "official")
        request_field_list = [
            ("title", "标题", "title_language", title_jp_website_new_list),
            ("title_zh", "中文标题", "title_language", title_zh_website_new_list),
            ("outline", "简介", "outline_language", outline_jp_website_new_list),
            ("outline_zh", "中文简介", "outline_language", outline_zh_website_new_list),
            ("actor", "演员", "actor_language", actor_website_new_list),
            ("cover", "背景图", "title_language", thumb_website_new_list),
            ("poster", "封面图", "title_language", poster_website_new_list),
            ("extrafanart", "剧照", "title_language", extrafanart_website_new_list),
            ("tag", "标签", "tag_language", tag_website_new_list),
            ("release", "发行日期", "title_language", release_website_new_list),
            ("runtime", "时长", "title_language", runtime_website_new_list),
            ("score", "评分", "title_language", score_website_new_list),
            ("director", "导演", "director_language", director_website_new_list),
            ("series", "系列", "series_language", series_website_new_list),
            ("studio", "片商", "studio_language", studio_website_new_list),
            ("publisher", "发行商", "publisher_language", publisher_website_new_list),
            ("trailer", "预告片", "title_language", trailer_website_new_list),
            ("wanted", "想看人数", "title_language", wanted_website_new_list),
        ]
        if config.outline_language == "jp":
            request_field_list.pop(3)
        if config.title_language == "jp":
            request_field_list.pop(1)
        if not wanted_website_new_list:
            request_field_list.pop()

    for field_name, field_cnname, field_language, website_list in request_field_list:
        if field_name in none_fields:
            continue
        _call_crawlers(
            all_res,
            input_info,
            final_res,
            website_list,
            field_name,
            field_cnname,
            field_language,
            config,
            file_number,
            short_number,
            input_info["mosaic"],
        )
        if field_name == "title" and not input_info["title"]:
            return final_res

    # 处理字段字段：从已请求的网站中，按字段网站优先级取值
    title_website_list = title_jp_website_list
    outline_website_list = outline_jp_website_list
    number_website_list = [i for i in number_website_list if i in all_res.keys()]
    new_number_website_list = number_website_list
    if "official" in all_res.keys() and all_res["official"].data.title:
        official_website_name = all_res["official"].data.source
        new_number_website_list = [official_website_name] + number_website_list
        title_jp_website_list = [official_website_name] + title_jp_website_list
        outline_jp_website_list = [official_website_name] + outline_jp_website_list
    if config.title_language != "jp":
        title_website_list = title_zh_website_list + title_jp_website_list
    if config.outline_language != "jp":
        outline_website_list = outline_zh_website_list + outline_jp_website_list
    title_website_new_list = _get_new_website_list(
        title_website_list, new_number_website_list, file_number, short_number, "title", all=True
    )
    title_jp_website_new_list = _get_new_website_list(
        title_jp_website_list, new_number_website_list, file_number, short_number, "title", all=True
    )
    outline_website_new_list = _get_new_website_list(
        outline_website_list, new_number_website_list, file_number, short_number, "outline", all=True
    )
    outline_jp_website_new_list = _get_new_website_list(
        outline_jp_website_list, new_number_website_list, file_number, short_number, "outline", all=True
    )
    actor_website_new_list = _get_new_website_list(
        actor_website_list, number_website_list, file_number, short_number, "actor", all=True
    )
    thumb_website_new_list = _get_new_website_list(
        thumb_website_list, number_website_list, file_number, short_number, "thumb", all=True
    )
    poster_website_new_list = _get_new_website_list(
        poster_website_list, number_website_list, file_number, short_number, "poster", all=True
    )
    extrafanart_website_new_list = _get_new_website_list(
        extrafanart_website_list, number_website_list, file_number, short_number, "extrafanart", all=True
    )
    tag_website_new_list = _get_new_website_list(
        tag_website_list, number_website_list, file_number, short_number, "tag", all=True
    )
    release_website_new_list = _get_new_website_list(
        release_website_list, number_website_list, file_number, short_number, "release", all=True
    )
    runtime_website_new_list = _get_new_website_list(
        runtime_website_list, number_website_list, file_number, short_number, "runtime", all=True
    )
    score_website_new_list = _get_new_website_list(
        score_website_list, number_website_list, file_number, short_number, "score", all=True
    )
    director_website_new_list = _get_new_website_list(
        director_website_list, number_website_list, file_number, short_number, "director", all=True
    )
    series_website_new_list = _get_new_website_list(
        series_website_list, number_website_list, file_number, short_number, "series", all=True
    )
    studio_website_new_list = _get_new_website_list(
        studio_website_list, number_website_list, file_number, short_number, "studio", all=True
    )
    publisher_website_new_list = _get_new_website_list(
        publisher_website_list, number_website_list, file_number, short_number, "publisher", all=True
    )
    trailer_website_new_list = _get_new_website_list(
        trailer_website_list, number_website_list, file_number, short_number, "trailer", all=True
    )
    wanted_website_new_list = _get_new_website_list(
        wanted_website_list, number_website_list, file_number, short_number, "wanted"
    )
    deal_field_list = [
        ("title", "标题", "title_language", title_website_new_list),
        ("originaltitle", "原标题", "outline_language", title_jp_website_new_list),
        ("outline", "简介", "outline_language", outline_website_new_list),
        ("originalplot", "原简介", "outline_language", outline_jp_website_new_list),
        ("actor", "演员", "actor_language", actor_website_new_list),
        ("cover", "背景图", "title_language", thumb_website_new_list),
        ("poster", "封面图", "title_language", poster_website_new_list),
        ("extrafanart", "剧照", "title_language", extrafanart_website_new_list),
        ("tag", "标签", "tag_language", tag_website_new_list),
        ("release", "发行日期", "title_language", release_website_new_list),
        ("runtime", "时长", "title_language", runtime_website_new_list),
        ("score", "评分", "title_language", score_website_new_list),
        ("director", "导演", "director_language", director_website_new_list),
        ("series", "系列", "series_language", series_website_new_list),
        ("studio", "片商", "studio_language", studio_website_new_list),
        ("publisher", "发行商", "publisher_language", publisher_website_new_list),
        ("trailer", "预告片", "title_language", trailer_website_new_list),
        ("wanted", "想看人数", "title_language", wanted_website_list),
    ]
    if not wanted_website_new_list or (scrape_like == "speed" and input_info["source"] not in wanted_website_new_list):
        deal_field_list.pop()

    for field_name, field_cnname, field_language, website_list in deal_field_list:
        _deal_each_field(all_res, input_info, final_res, website_list, field_name, field_cnname, field_language, config)

    # 把已刮削成功网站的 cover url 按照 cover 网站优先级，保存为一个列表，第一个图片下载失败时，可以使用其他图片下载
    cover_list = []
    for each_website in thumb_website_new_list:
        if each_website in all_res.keys() and all_res[each_website].data.title:
            temp_url = all_res[each_website].data.cover
            if temp_url not in cover_list:
                cover_list.append([each_website, temp_url])
    if not cover_list:
        final_res.data.cover = ""  # GBBH-1041 背景图图挂了
    final_res.metadata.cover_list = cover_list

    # 把已刮削成功网站的 actor，保存为一个列表，用于 Amazon 搜图，因为有的网站 actor 不对，比如 MOPP-023 javbus错的
    actor_amazon_list = []
    actor_amazon_list_cn = []
    actor_amazon_list_tw = []
    actor_new_website = []
    [
        actor_new_website.append(i)
        for i in title_jp_website_new_list + title_website_new_list + actor_website_new_list
        if i not in actor_new_website
    ]
    for each_website in actor_new_website:
        if each_website in all_res.keys() and all_res[each_website].data.title:
            temp_actor = all_res[each_website].data.actor
            if temp_actor:
                actor_amazon_list.extend(temp_actor.split(","))
                if all_res[each_website].data.title:
                    actor_amazon_list_cn.extend(all_res[each_website].data.actor.split(","))
    actor_amazon_list = actor_amazon_list + actor_amazon_list_cn + actor_amazon_list_tw
    actor_amazon = []
    [actor_amazon.append(i.strip()) for i in actor_amazon_list if i.strip() and i.strip() not in actor_amazon]
    if "素人" in actor_amazon:
        actor_amazon.remove("素人")
    final_res.metadata.actor_amazon = actor_amazon

    # 处理 year
    release = input_info["release"]
    if release and (r := re.search(r"\d{4}", release)):
        final_res.data.year = r.group()

    # 处理 number：素人影片时使用有数字前缀的number
    if short_number:
        final_res.data.number = file_number

    final_res.metadata.fields_info = (
        f"\n 🌐 [website] {LogBuffer.req().get().strip('-> ')}{final_res.metadata.fields_info}"
    )
    if "javdb" in all_res:
        final_res.data.javdb_id = all_res["javdb"].data.javdb_id
    return final_res


# used by crawl
def _crawl(input_info: InputInfo, website_name: str) -> FinalResult:
    file_number = input_info["number"]
    file_path = input_info["file_path"]
    short_number = input_info["short_number"]
    appoint_number = input_info["appoint_number"]
    appoint_url = input_info["appoint_url"]
    has_sub = input_info["has_sub"]
    c_word = input_info["c_word"]
    leak = input_info["leak"]
    wuma = input_info["wuma"]
    youma = input_info["youma"]
    cd_part = input_info["cd_part"]
    destroyed = input_info["destroyed"]
    mosaic = input_info["mosaic"]
    version = input_info["version"]
    number = input_info["number"]
    if appoint_number:
        number = appoint_number
    final_res = FinalResult.new_empty()
    final_res.metadata.fields_info = ""
    # ================================================网站规则添加开始================================================

    if website_name == "all":  # 从全部网站刮削
        # =======================================================================先判断是不是国产，避免浪费时间
        if (
            mosaic == "国产"
            or mosaic == "國產"
            or (re.search(r"([^A-Z]|^)MD[A-Z-]*\d{4,}", file_number) and "MDVR" not in file_number)
            or re.search(r"MKY-[A-Z]+-\d{3,}", file_number)
        ):
            final_res.data.mosaic = "国产"
            website_list = config.website_guochan.split(",")
            final_res = _crawl_websites(input_info, final_res, website_list)

        # =======================================================================kin8
        elif file_number.startswith("KIN8"):
            website_name = "kin8"
            final_res = _call_specific_crawler(input_info, final_res, website_name)

        # =======================================================================同人
        elif file_number.startswith("DLID"):
            website_name = "getchu"
            final_res = _call_specific_crawler(input_info, final_res, website_name)

        # =======================================================================里番
        elif "getchu" in file_path.lower() or "里番" in file_path or "裏番" in file_path:
            website_name = "getchu_dmm"
            final_res = _call_specific_crawler(input_info, final_res, website_name)

        # =======================================================================Mywife No.1111
        elif "mywife" in file_path.lower():
            website_name = "mywife"
            final_res = _call_specific_crawler(input_info, final_res, website_name)

        # =======================================================================FC2-111111
        elif "FC2" in file_number.upper():
            file_number_1 = re.search(r"\d{5,}", file_number)
            if file_number_1:
                file_number_1.group()
                website_list = config.website_fc2.split(",")
                final_res = _crawl_websites(input_info, final_res, website_list)
            else:
                LogBuffer.error().write(f"未识别到FC2番号：{file_number}")

        # =======================================================================sexart.15.06.14
        elif re.search(r"[^.]+\.\d{2}\.\d{2}\.\d{2}", file_number) or (
            "欧美" in file_path and "东欧美" not in file_path
        ):
            website_list = config.website_oumei.split(",")
            final_res = _crawl_websites(input_info, final_res, website_list)

        # =======================================================================无码抓取:111111-111,n1111,HEYZO-1111,SMD-115
        elif mosaic == "无码" or mosaic == "無碼":
            website_list = config.website_wuma.split(",")
            final_res = _crawl_websites(input_info, final_res, website_list)

        # =======================================================================259LUXU-1111
        elif short_number or "SIRO" in file_number.upper():
            website_list = config.website_suren.split(",")
            final_res = _crawl_websites(input_info, final_res, website_list)

        # =======================================================================ssni00321
        elif re.match(r"\D{2,}00\d{3,}", file_number) and "-" not in file_number and "_" not in file_number:
            website_list = ["dmm"]
            final_res = _crawl_websites(input_info, final_res, website_list)

        # =======================================================================剩下的（含匹配不了）的按有码来刮削
        else:
            website_list = config.website_youma.split(",")
            final_res = _crawl_websites(input_info, final_res, website_list)
    else:
        final_res = _call_specific_crawler(input_info, final_res, website_name)

    # ================================================网站请求结束================================================
    # ======================================超时或未找到返回
    if final_res.data.title == "":
        return final_res

    # 马赛克
    if leak:
        final_res.data.mosaic = "无码流出"
    elif destroyed:
        final_res.data.mosaic = "无码破解"
    elif wuma:
        final_res.data.mosaic = "无码"
    elif youma:
        final_res.data.mosaic = "有码"
    elif mosaic:
        final_res.data.mosaic = mosaic
    if not input_info.get("mosaic"):
        if is_uncensored(number):
            final_res.data.mosaic = "无码"
        else:
            final_res.data.mosaic = "有码"
    print(number, cd_part, input_info["mosaic"], LogBuffer.req().get().strip("-> "))

    # 车牌字母
    letters = get_number_letters(number)

    # 原标题，用于amazon搜索
    originaltitle = input_info.get("originaltitle") or ""
    final_res.metadata.originaltitle_amazon = originaltitle
    for each in input_info["actor_amazon"]:  # 去除演员名，避免搜索不到
        try:
            end_actor = re.compile(rf" {each}$")
            final_res.metadata.originaltitle_amazon = re.sub(end_actor, "", input_info["originaltitle_amazon"])
        except:
            pass

    # VR 时下载小封面
    if "VR" in number:
        final_res.data.image_download = True

    # 返回处理后的json_data
    final_res.data.number = number
    final_res.metadata.letters = letters
    final_res.metadata.has_sub = has_sub
    final_res.metadata.c_word = c_word
    final_res.metadata.leak = leak
    final_res.metadata.wuma = wuma
    final_res.metadata.youma = youma
    final_res.metadata.cd_part = cd_part
    final_res.metadata.destroyed = destroyed
    final_res.metadata.version = version
    final_res.metadata.file_path = file_path
    final_res.metadata.appoint_number = appoint_number
    final_res.metadata.appoint_url = appoint_url

    return final_res


def _get_new_website_list(
    field_website_list: list[str],
    number_website_list: list[str],
    file_number: str,
    short_number: str,
    field: str,
    all: bool = False,
) -> list[str]:
    whole_fields = config.whole_fields  # 继续补全的字段
    field_website_list = [i for i in field_website_list if i.strip()]  # 去空
    number_website_list = [i for i in number_website_list if i.strip()]  # 去空
    same_list = [i for i in field_website_list if i in number_website_list]  # 取交集
    if (
        field in whole_fields or field == "title" or all
    ):  # 取剩余未相交网站， trailer 不取未相交网站，title 默认取未相交网站
        if field != "trailer":
            diff_list = [i for i in number_website_list if i not in field_website_list]
            same_list.extend(diff_list)
    dic_escape = {
        "title": config.title_website_exclude.split(","),
        "outline": config.outline_website_exclude.split(","),
        "actor": config.actor_website_exclude.split(","),
        "thumb": config.thumb_website_exclude.split(","),
        "poster": config.poster_website_exclude.split(","),
        "extrafanart": config.extrafanart_website_exclude.split(","),
        "trailer": config.trailer_website_exclude.split(","),
        "tag": config.tag_website_exclude.split(","),
        "release": config.release_website_exclude.split(","),
        "runtime": config.runtime_website_exclude.split(","),
        "score": config.score_website_exclude.split(","),
        "director": config.director_website_exclude.split(","),
        "series": config.series_website_exclude.split(","),
        "studio": config.studio_website_exclude.split(","),
        "publisher": config.publisher_website_exclude.split(","),
    }  # 根据字段排除的网站

    escape_list = dic_escape.get(field)
    if escape_list:
        same_list = [i for i in same_list if i not in escape_list]  # 根据字段排除一些不含这些字段的网站

    # mgstage 素人番号检查
    if short_number:
        not_frist_field_list = ["title", "actor"]  # 这些字段以外，素人把 mgstage 放在第一位
        if field not in not_frist_field_list and "mgstage" in same_list:
            same_list.remove("mgstage")
            same_list.insert(0, "mgstage")

    # faleno.jp 番号检查 dldss177 dhla009
    elif re.findall(r"F[A-Z]{2}SS", file_number):
        same_list = _deal_some_list(field, "faleno", same_list)

    # dahlia-av.jp 番号检查
    elif file_number.startswith("DLDSS") or file_number.startswith("DHLA"):
        same_list = _deal_some_list(field, "dahlia", same_list)

    # fantastica 番号检查 FAVI、FAAP、FAPL、FAKG、FAHO、FAVA、FAKY、FAMI、FAIT、FAKA、FAMO、FASO、FAIH、FASH、FAKS、FAAN
    elif (
        re.search(r"FA[A-Z]{2}-?\d+", file_number.upper())
        or file_number.upper().startswith("CLASS")
        or file_number.upper().startswith("FADRV")
        or file_number.upper().startswith("FAPRO")
        or file_number.upper().startswith("FAKWM")
        or file_number.upper().startswith("PDS")
    ):
        same_list = _deal_some_list(field, "fantastica", same_list)

    return same_list


def _deal_some_list(field: str, website: str, same_list: list[str]) -> list[str]:
    if website not in same_list:
        same_list.append(website)
    if field in ["title", "outline", "thumb", "poster", "trailer", "extrafanart"]:
        same_list.remove(website)
        same_list.insert(0, website)
    elif field in ["tag", "score", "director", "series"]:
        same_list.remove(website)
    return same_list


def _get_website_name(j_website_name: str, file_mode: FileMode) -> str:
    # 获取刮削网站
    website_name = "all"
    if file_mode == FileMode.Single:  # 刮削单文件（工具页面）
        website_name = Flags.website_name
    elif file_mode == FileMode.Again:  # 重新刮削
        website_temp = j_website_name
        if website_temp:
            website_name = website_temp
    elif config.scrape_like == "single":
        website_name = config.website_single

    return website_name


def crawl(input_info: InputInfo, file_mode: FileMode) -> FinalResult:
    website_name = _get_website_name(input_info["website_name"], file_mode)
    final_res = _crawl(input_info, website_name)
    final_res.data = _post_process(final_res.data)
    return final_res


# used by crawl
def _post_process(movie_data: MovieData) -> MovieData:
    # 标题为空返回
    title = movie_data.title
    if not title:
        return movie_data

    # 演员
    movie_data.actor = (
        str(movie_data.actor)
        .strip(" [ ]")
        .replace("'", "")
        .replace(", ", ",")
        .replace("<", "(")
        .replace(">", ")")
        .strip(",")
    )  # 列表转字符串（避免个别网站刮削返回的是列表）

    # 标签
    tag = (
        str(movie_data.tag).strip(" [ ]").replace("'", "").replace(", ", ",")
    )  # 列表转字符串（避免个别网站刮削返回的是列表）
    tag = re.sub(r",\d+[kKpP],", ",", tag)
    tag_rep_word = [",HD高画质", ",HD高畫質", ",高画质", ",高畫質"]
    for each in tag_rep_word:
        if tag.endswith(each):
            tag = tag.replace(each, "")
        tag = tag.replace(each + ",", ",")
    movie_data.tag = tag

    # poster图
    if not movie_data.get("poster"):
        movie_data.poster = ""

    # 发行日期
    release = movie_data.release
    if release:
        release = release.replace("/", "-").strip(". ")
        if len(release) < 10:
            release_list = re.findall(r"(\d{4})-(\d{1,2})-(\d{1,2})", release)
            if release_list:
                r_year, r_month, r_day = release_list[0]
                r_month = "0" + r_month if len(r_month) == 1 else r_month
                r_day = "0" + r_day if len(r_day) == 1 else r_day
                release = r_year + "-" + r_month + "-" + r_day
    movie_data.release = release

    # 评分
    if movie_data.score:
        movie_data.score = "%.1f" % float(movie_data.score)

    # publisher
    if not movie_data.get("publisher"):
        movie_data.publisher = movie_data.studio

    # 字符转义，避免显示问题
    key_word = [
        "title",
        "originaltitle",
        "number",
        "outline",
        "originalplot",
        "actor",
        "tag",
        "series",
        "director",
        "studio",
        "publisher",
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
        "<br/>": "",
        "・": "·",
        "“": "「",
        "”": "」",
        "...": "…",
        "\xa0": "",
        "\u3000": "",
        "\u2800": "",
    }
    for each in key_word:
        for key, value in rep_word.items():
            movie_data.__dict__[each] = movie_data.__dict__[each].replace(key, value)

    return movie_data
