#!/usr/bin/env python3


from models.config.config import config
from models.crawlers import iqqtv
from models.data_models import CrawlerResult


def main(
    number,
    appoint_url="",
    language="zh_cn",
):
    all_language = (
        config.title_language
        + config.outline_language
        + config.actor_language
        + config.tag_language
        + config.series_language
        + config.studio_language
    )
    appoint_url = appoint_url.replace("/cn/", "/jp/").replace("iqqtv.cloud/player", "iqqtv.cloud/jp/player")
    res = iqqtv.main(number, appoint_url, "jp")
    if res.data is None:
        return CrawlerResult.failed("iqqtv")
    if "zh_cn" in all_language:
        language = "zh_cn"
        appoint_url = res.data.website.replace("/jp/", "/cn/")
    if "zh_tw" in all_language:
        language = "zh_tw"
        appoint_url = res.data.website.replace("/jp/", "/")

    res_zh = iqqtv.main(number, appoint_url, language)
    if res_zh.data is None:
        return CrawlerResult.failed("iqqtv")
    res_zh.data.originaltitle = res.data.originaltitle
    res_zh.data.originalplot = res.data.originalplot
    return res_zh


if __name__ == "__main__":
    print(main("abs-141"))
    # print(main('HYSD-00083'))
    # print(main('IESP-660'))
    # print(main('n1403'))  # print(main('GANA-1910'))  # print(main('heyzo-1031'))  # print(main_us('x-art.19.11.03'))  # print(main('032020-001'))  # print(main('S2M-055'))  # print(main('LUXU-1217'))

    # print(main('1101132', ''))  # print(main('OFJE-318'))  # print(main('110119-001'))  # print(main('abs-001'))  # print(main('SSIS-090', ''))  # print(main('SSIS-090', ''))  # print(main('SNIS-016', ''))  # print(main('HYSD-00083', ''))  # print(main('IESP-660', ''))  # print(main('n1403', ''))  # print(main('GANA-1910', ''))  # print(main('heyzo-1031', ''))  # print(main_us('x-art.19.11.03'))  # print(main('032020-001', ''))  # print(main('S2M-055', ''))  # print(main('LUXU-1217', ''))  # print(main_us('x-art.19.11.03', ''))
