#!/usr/bin/env python3
from models.crawlers import dmm, getchu
from models.data_models import CrawlerResult


def main(
    number,
    appoint_url="",
    language="jp",
):
    name = "getchu_dmm"
    res_getchu = getchu.main(number, appoint_url, "jp")
    data = res_getchu.data
    if not data:
        return CrawlerResult.failed(name)

    poster = data.poster
    outline = data.outline
    if data.title:
        number = data.number
        if number.startswith("DLID") or "dl.getchu" in appoint_url:
            return res_getchu
    res_dmm = dmm.main(number, appoint_url, "jp")
    if res_dmm.data and res_dmm.data.title:
        data.update(res_dmm.data)
        if poster:  # 使用 getchu 封面
            data.poster = poster
        if outline:  # 使用 getchu 简介
            data.outline = outline
            data.originalplot = outline
    return CrawlerResult(name, data=data)


if __name__ == "__main__":
    # yapf: disable
    # print(main('コンビニ○○Z 第三話 あなた、ヤンクレママですよね。旦那に万引きがバレていいんですか？'))
    # print(main('[PoRO]エロコンビニ店長 泣きべそ蓮っ葉・栞～お仕置きじぇらしぃナマ逸機～'))
    # print(main('ACHDL-1159'))
    # print(main('好きにしやがれ GOTcomics'))    # 書籍，没有番号 # dmm 没有
    # print(main('ACMDP-1005')) # 有时间、导演，上下集ACMDP-1005B
    # print(main('ISTU-5391'))    # dmm 没有
    # print(main('INH-392'))
    # print(main('OVA催眠性指導 ＃4宮島椿の場合')) # 都没有
    # print(main('OVA催眠性指導 ＃5宮島椿の場合')) # 都没有
    # print(main('GLOD-148')) # getchu 没有
    # print(main('(18禁アニメ) (無修正) 紅蓮 第1幕 「鬼」 (spursengine 960x720 h.264 aac)'))
    print(main('誘惑 ～始発の章～'))  # print(main('ISTU-5391', appoint_url='http://www.getchu.com/soft.phtml?id=1180483'))  # print(main('SPY×FAMILY Vol.1 Blu-ray Disc＜初回生産限定版＞'))    # dmm 没有
