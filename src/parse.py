import re

from bs4 import BeautifulSoup

from src.models import (
    HorseProfilePicked,
    JockeyInfoPicked,
    RaceShutuba,
    RaceShutubaItem,
)


def parse_shutuba(html: str) -> RaceShutuba:
    """
    netkeibaの出馬表ページをパースする

    Args:
        html: 出馬表のHTML

    Returns:
        RaceShutuba: パースした出馬表データ
    """
    soup = BeautifulSoup(html, "lxml")

    # レース名、日付、場所を取得
    title_element = soup.select_one("head > title")
    title_element.get_text() if title_element is not None else ""
    match = re.match(
        r"^(.+?) 出馬表 \| (\d{4}年\d{1,2}月\d{1,2}日) (.+?\d+R) レース情報\(JRA\) - netkeiba",
        title_element.get_text() if title_element is not None else "",
    )
    # titleをパースし、インデックスが存在しない場合はデフォルトで空文字列を設定
    title_parts = match.groups() if match else []
    race_name = title_parts[0].strip() if len(title_parts) > 0 else ""
    date = title_parts[1].strip() if len(title_parts) > 1 else ""
    place = title_parts[2].strip() if len(title_parts) > 2 else ""

    race_name, date, place = match.groups() if match else ("", "", "")

    # レースIDを取得
    shutuba_link_element = soup.select_one(
        "#page > div.RaceColumn01 > div > div.RaceMainColumn > div.RaceNumWrap > ul > li.Active > a"
    )
    shutuba_href: str = shutuba_link_element["href"] if shutuba_link_element is not None else ""
    id_match = re.match(r"^\?race_id=(\d{12})", shutuba_href)
    race_id = id_match.group(1) if id_match else ""

    # 発走時刻、コース、天気、馬場状態を取得
    raceinfo_element = soup.select_one(
        "#page > div.RaceColumn01 > div > div.RaceMainColumn > div.RaceList_NameBox > div.RaceList_Item02 > div.RaceData01"
    )
    raceinfo_text = raceinfo_element.get_text() if raceinfo_element is not None else ""

    # レース情報のフィールドをパースし、インデックスが存在しない場合はデフォルトで空文字列を設定
    raceinfo_parts = raceinfo_text.split("/") if raceinfo_text else []
    time = raceinfo_parts[0].strip() if len(raceinfo_parts) > 0 else ""
    course = raceinfo_parts[1].strip() if len(raceinfo_parts) > 1 else ""
    weather = raceinfo_parts[2].strip() if len(raceinfo_parts) > 2 else ""
    condition = raceinfo_parts[3].strip() if len(raceinfo_parts) > 3 else ""

    return RaceShutuba(
        race_name=race_name,
        race_id=race_id,
        date=date,
        time=time,
        place=place,
        course=course,
        weather=weather,
        condition=condition,
        shutuba=parse_shutuba_items(html),
    )


def parse_shutuba_items(html: bytes) -> list[RaceShutubaItem]:
    """
    出馬表の馬情報をパースする

    Args:
        html: 出馬表のHTML

    Returns:
        list[RaceShutubaItem]: パースした出馬表データ
    """
    soup = BeautifulSoup(html, "lxml")

    # print(soup.select("#page > div.RaceColumn02 > div.RaceTableArea > table > tr"))

    # 出馬表の馬情報を取得
    shutuba_items: list[RaceShutubaItem] = []
    for item in soup.select("#page > div.RaceColumn02 > div.RaceTableArea > table > tbody > tr"):
        # 枠番を取得
        waku_element = item.select_one("td:nth-child(1) > span")
        waku = int(waku_element.get_text()) if waku_element else -1

        # 馬番を取得
        num_element = item.select_one("td:nth-child(2)")
        num = int(num_element.get_text()) if num_element else -1

        # 馬情報を取得
        horse_element = item.select_one("td:nth-child(4) > div > div > span > a")
        horse_href: str = horse_element["href"] if horse_element is not None else ""
        horse_id_match = re.match(r"https://db.netkeiba.com/horse/(\d{10})", horse_href)
        horse_id = horse_id_match.group(1) if horse_id_match else ""
        horse_name = horse_element.get_text() if horse_element is not None else ""
        horse = HorseProfilePicked(
            horse_name=horse_name,
            horse_id=horse_id,
        )

        # 性齢を取得
        sex_age_element = item.select_one("td:nth-child(5)")
        sex_age = sex_age_element.get_text() if sex_age_element else ""

        # 斤量を取得
        impost_weight_element = item.select_one("td:nth-child(6)")
        impost_weight = impost_weight_element.get_text() if impost_weight_element else ""

        # 騎手情報を取得
        jockey_element = item.select_one("td:nth-child(7) > a")
        jockey_href: str = jockey_element["href"] if jockey_element is not None else ""
        jockey_id_match = re.match(r"https://db.netkeiba.com/jockey/result/recent/(\d{5})", jockey_href)
        jockey_id = jockey_id_match.group(1) if jockey_id_match else ""
        jockey_name = (jockey_element.get_text() if jockey_element is not None else "").strip()
        jockey = JockeyInfoPicked(
            jockey_name=jockey_name,
            jockey_id=jockey_id,
        )

        # 馬体重を取得
        horse_weight_element = item.select_one("td:nth-child(9)")
        horse_weight = (horse_weight_element.get_text() if horse_weight_element else "").strip()

        # オッズを取得
        odds_element = item.select_one("td:nth-child(10) > span")
        odds = odds_element.get_text() if odds_element else ""

        # 人気を取得
        pop_element = item.select_one("td:nth-child(11) > span")
        pop = pop_element.get_text() if pop_element else ""

        shutuba_items.append(
            RaceShutubaItem(
                waku=waku,
                num=num,
                horse=horse,
                sex_age=sex_age,
                impost_weight=impost_weight,
                jockey=jockey,
                horse_weight=horse_weight,
                odds=odds,
                pop=pop,
            )
        )

    return shutuba_items
