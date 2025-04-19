import re

from bs4 import BeautifulSoup

from src.models import (
    HorsePed,
    HorseProfile,
    HorseProfilePicked,
    HorseRaceResultItem,
    JockeyInfoPicked,
    RaceResultPicked,
)


def parse_horse_profile(html: bytes) -> HorseProfile:
    """
    netkeibaの馬情報ページをパースする

    Args:
        html: 馬情報のHTML

    Returns:
        HorseProfilePicked: パースした馬情報データ
    """
    soup = BeautifulSoup(html, "lxml")

    # 馬名を取得
    horse_name_element = soup.select_one(
        "#db_main_box > div.db_head.fc > div.db_head_name.fc > div > div.horse_title > h1"
    )
    horse_name = horse_name_element.get_text() if horse_name_element is not None else ""

    # 馬IDを取得
    horse_id_element = soup.select_one(
        "#db_main_box > div.db_head.fc > div.db_head_name.fc > div > div.horse_title > p.eng_name > a"
    )
    horse_id_href: str = horse_id_element["href"] if horse_id_element is not None else ""
    id_match = re.match(r"https://en.netkeiba.com/db/horse/([0-9a-z]{10})/", horse_id_href)
    horse_id = id_match.group(1) if id_match else ""

    # 生年月日を取得
    birth_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child(1) > td"
    )
    birth = birth_element.get_text() if birth_element is not None else ""

    # 獲得賞金を取得
    total_prize_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child(8) > td"
    )
    total_prize = total_prize_element.get_text() if total_prize_element is not None else ""

    # 通算成績を取得
    total_record_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > table > tr:nth-child(9) > td"
    )
    total_record = total_record_element.get_text() if total_record_element is not None else ""

    return HorseProfile(
        horse_name=horse_name,
        horse_id=horse_id,
        birth=birth,
        total_prize=total_prize,
        total_record=total_record,
        ped=parse_horse_ped(html),  # 血統情報をパース
        race_result=parse_horse_race_result(html),  # レース結果をパース
    )


def parse_horse_ped(html: bytes) -> HorsePed:
    """
    netkeibaの馬情報ページをパースする
    Args:
        html: 馬情報のHTML
    Returns:
        HorsePed: パースした馬情報データ
    """

    soup = BeautifulSoup(html, "lxml")

    # 血統情報を取得
    # 父を取得
    father_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > div > dl > dd > table > tr:nth-child(1) > td:nth-child(1) > a"
    )
    father_href: str = father_element["href"] if father_element is not None else ""
    father_id_match = re.match(r"/horse/ped/([0-9a-z]{10})/", father_href)
    father_id = father_id_match.group(1) if father_id_match else ""
    father_name = father_element.get_text() if father_element is not None else ""
    father = HorseProfilePicked(
        horse_name=father_name,
        horse_id=father_id,
    )

    # 母を取得
    mother_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > div > dl > dd > table > tr:nth-child(3) > td:nth-child(1) > a"
    )
    mother_href: str = mother_element["href"] if mother_element is not None else ""
    mother_id_match = re.match(r"/horse/ped/([0-9a-z]{10})/", mother_href)
    mother_id = mother_id_match.group(1) if mother_id_match else ""
    mother_name = mother_element.get_text() if mother_element is not None else ""
    mother = HorseProfilePicked(
        horse_name=mother_name,
        horse_id=mother_id,
    )

    # 父の父を取得
    father_father_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > div > dl > dd > table > tr:nth-child(1) > td:nth-child(2) > a"
    )
    father_father_href: str = father_father_element["href"] if father_father_element is not None else ""
    father_father_id_match = re.match(r"/horse/ped/([0-9a-z]{10})/", father_father_href)
    father_father_id = father_father_id_match.group(1) if father_father_id_match else ""
    father_father_name = father_father_element.get_text() if father_father_element is not None else ""
    father_father = HorseProfilePicked(
        horse_name=father_father_name,
        horse_id=father_father_id,
    )

    # 父の母を取得
    father_mother_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > div > dl > dd > table > tr:nth-child(2) > td > a"
    )
    father_mother_href: str = father_mother_element["href"] if father_mother_element is not None else ""
    father_mother_id_match = re.match(r"/horse/ped/([0-9a-z]{10})/", father_mother_href)
    father_mother_id = father_mother_id_match.group(1) if father_mother_id_match else ""
    father_mother_name = father_mother_element.get_text() if father_mother_element is not None else ""
    father_mother = HorseProfilePicked(
        horse_name=father_mother_name,
        horse_id=father_mother_id,
    )

    # 母の父を取得
    mother_father_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > div > dl > dd > table > tr:nth-child(3) > td:nth-child(2) > a"
    )
    mother_father_href: str = mother_father_element["href"] if mother_father_element is not None else ""
    mother_father_id_match = re.match(r"/horse/ped/([0-9a-z]{10})/", mother_father_href)
    mother_father_id = mother_father_id_match.group(1) if mother_father_id_match else ""
    mother_father_name = mother_father_element.get_text() if mother_father_element is not None else ""
    mother_father = HorseProfilePicked(
        horse_name=mother_father_name,
        horse_id=mother_father_id,
    )

    # 母の母を取得
    mother_mother_element = soup.select_one(
        "#db_main_box > div.db_main_deta > div > div.db_prof_area_02 > div > dl > dd > table > tr:nth-child(4) > td > a"
    )
    mother_mother_href: str = mother_mother_element["href"] if mother_mother_element is not None else ""
    mother_mother_id_match = re.match(r"/horse/ped/([0-9a-z]{10})/", mother_mother_href)
    mother_mother_id = mother_mother_id_match.group(1) if mother_mother_id_match else ""
    mother_mother_name = mother_mother_element.get_text() if mother_mother_element is not None else ""
    mother_mother = HorseProfilePicked(
        horse_name=mother_mother_name,
        horse_id=mother_mother_id,
    )

    return HorsePed(
        father=father,
        mother=mother,
        father_father=father_father,
        father_mother=father_mother,
        mother_father=mother_father,
        mother_mother=mother_mother,
    )


def parse_horse_race_result(html: bytes) -> list[HorseRaceResultItem]:
    """
    netkeibaの馬情報ページをパースする
    Args:
        html: 馬情報のHTML
    Returns:
        HorseRaceResultItem: パースした馬情報データ
    """

    soup = BeautifulSoup(html, "lxml")

    horse_race_result_items: list[HorseRaceResultItem] = []
    # レース結果を取得
    for item in soup.select("#contents > div.db_main_race.fc > div > table > tbody > tr"):
        # レース日を取得
        date_element = item.select_one("td:nth-child(1) > a")
        race_date = date_element.get_text() if date_element is not None else ""

        # 開催場所を取得
        place_element = item.select_one("td:nth-child(2) > a")
        place = place_element.get_text() if place_element is not None else ""

        # 天候を取得
        weather_element = item.select_one("td:nth-child(3)")
        weather = weather_element.get_text() if weather_element is not None else ""

        # レース情報を取得
        race_element = item.select_one("td:nth-child(5) > a")
        race_href: str = race_element["href"] if race_element is not None else ""
        race_id_match = re.match(r"/race/(\d{12})", race_href)
        race_id = race_id_match.group(1) if race_id_match else ""
        race_name = race_element.get_text() if race_element is not None else ""
        race = RaceResultPicked(race_name=race_name, race_id=race_id)

        # 頭数を取得
        horse_number_element = item.select_one("td:nth-child(7)")
        horse_number = horse_number_element.get_text() if horse_number_element is not None else ""

        # 枠番を取得
        waku_element = item.select_one("td:nth-child(8)")
        waku = waku_element.get_text() if waku_element is not None else ""

        # 馬番を取得
        num_element = item.select_one("td:nth-child(9)")
        num = num_element.get_text() if num_element is not None else ""

        # オッズを取得
        odds_element = item.select_one("td:nth-child(10)")
        odds = odds_element.get_text() if odds_element is not None else ""

        # 人気を取得
        pop_element = item.select_one("td:nth-child(11)")
        pop = pop_element.get_text() if pop_element is not None else ""

        # 着順を取得
        rank_element = item.select_one("td:nth-child(12)")
        rank = rank_element.get_text() if rank_element is not None else ""

        # 騎手情報を取得
        jockey_element = item.select_one("td:nth-child(13) > a")
        jockey_href: str = jockey_element["href"] if jockey_element is not None else ""
        jockey_id_match = re.match(r"/jockey/result/recent/(\d{5})", jockey_href)
        jockey_id = jockey_id_match.group(1) if jockey_id_match else ""
        jockey_name = jockey_element.get_text() if jockey_element is not None else ""
        jockey = JockeyInfoPicked(jockey_name=jockey_name, jockey_id=jockey_id)

        # 斤量を取得
        impost_weight_element = item.select_one("td:nth-child(14)")
        impost_weight = impost_weight_element.get_text() if impost_weight_element is not None else ""

        # コースを取得
        course_element = item.select_one("td:nth-child(15)")
        course = course_element.get_text() if course_element is not None else ""

        # 馬場状態を取得
        condition_element = item.select_one("td:nth-child(16)")
        condition = condition_element.get_text() if condition_element is not None else ""

        # タイムを取得
        time_element = item.select_one("td:nth-child(18)")
        time = time_element.get_text() if time_element is not None else ""

        # 着差を取得
        margin_element = item.select_one("td:nth-child(19)")
        margin = margin_element.get_text() if margin_element is not None else ""

        # 馬体重を取得
        horse_weight_element = item.select_one("td:nth-child(24)")
        horse_weight = (horse_weight_element.get_text() if horse_weight_element is not None else "").strip()

        horse_race_result_items.append(
            HorseRaceResultItem(
                race=race,
                race_date=race_date,
                place=place,
                weather=weather,
                course=course,
                condition=condition,
                horse_number=horse_number,
                rank=rank,
                waku=waku,
                num=num,
                impost_weight=impost_weight,
                jockey=jockey,
                time=time,
                margin=margin,
                odds=odds,
                pop=pop,
                horse_weight=horse_weight,
            )
        )

    return horse_race_result_items
