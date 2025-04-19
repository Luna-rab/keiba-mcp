import re

from bs4 import BeautifulSoup

from src.models import (
    HorsePed,
    HorseProfile,
    HorseProfilePicked,
    HorseRaceResultItem,
    JockeyInfoPicked,
    RaceResult,
    RaceResultItem,
    RaceResultPicked,
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


def parse_shutuba_items(html: str) -> list[RaceShutubaItem]:
    """
    出馬表の馬情報をパースする

    Args:
        html: 出馬表のHTML

    Returns:
        list[RaceShutubaItem]: パースした出馬表データ
    """
    soup = BeautifulSoup(html, "lxml")

    # 出馬表の馬情報を取得
    shutuba_items: list[RaceShutubaItem] = []
    for item in soup.select("#page > div.RaceColumn02 > div.RaceTableArea > table > tbody > tr"):
        # 枠番を取得
        waku_element = item.select_one("td:nth-child(1) > span")
        waku = waku_element.get_text() if waku_element else ""

        # 馬番を取得
        num_element = item.select_one("td:nth-child(2)")
        num = num_element.get_text() if num_element else ""

        # 馬情報を取得
        horse_element = item.select_one("td:nth-child(4) > div > div > span > a")
        horse_href: str = horse_element["href"] if horse_element is not None else ""
        horse_id_match = re.match(r"https://db.netkeiba.com/horse/([0-9a-z]{10})", horse_href)
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


def parse_race_result(html: bytes) -> RaceResult:
    """
    レース結果をパースする

    Args:
        html: レース結果のHTML

    Returns:
        RaceResult: パースしたレース結果データ
    """
    soup = BeautifulSoup(html, "lxml")

    # レース名、日付を取得
    title_element = soup.select_one("head > title")
    title_element.get_text() if title_element is not None else ""
    match = re.match(
        r"^(.*?)｜(\d{4}年\d{1,2}月\d{1,2}日) \| 競馬データベース - netkeiba",
        title_element.get_text() if title_element is not None else "",
    )
    # titleをパースし、インデックスが存在しない場合はデフォルトで空文字列を設定
    title_parts = match.groups() if match else []
    race_name = title_parts[0].strip() if len(title_parts) > 0 else ""
    date = title_parts[1].strip() if len(title_parts) > 1 else ""

    # レースIDを取得
    race_id_element = soup.select_one("#main > div > div > div > div > ul > li > a.active")
    race_id_href: str = race_id_element["href"] if race_id_element is not None else ""
    id_match = re.match(r"^/race/(\d{12})", race_id_href)
    race_id = id_match.group(1) if id_match else ""

    # コース、天候、馬場状態、発走時刻を取得
    raceinfo_element = soup.select_one(
        "#main > div > div > div > diary_snap > div > div > dl > dd > p > diary_snap_cut > span"
    )
    raceinfo_text = raceinfo_element.get_text() if raceinfo_element is not None else ""
    # レース情報のフィールドをパースし、インデックスが存在しない場合はデフォルトで空文字列を設定
    raceinfo_parts = raceinfo_text.split("/") if raceinfo_text else []
    course = raceinfo_parts[0].strip() if len(raceinfo_parts) > 0 else ""
    weather = raceinfo_parts[1].strip() if len(raceinfo_parts) > 1 else ""
    condition = raceinfo_parts[2].strip() if len(raceinfo_parts) > 2 else ""
    time = raceinfo_parts[3].strip() if len(raceinfo_parts) > 3 else ""

    # 場所を取得
    place_element = soup.select_one("#main > div > div > div > ul > li > a.active")
    place = place_element.get_text() if place_element is not None else ""

    return RaceResult(
        race_name=race_name,
        race_id=race_id,
        date=date,
        time=time,
        place=place,
        course=course,
        weather=weather,
        condition=condition,
        results=parse_race_result_items(html),
    )


def parse_race_result_items(html: bytes) -> list[RaceResultItem]:
    """
    レース結果の馬情報をパースする

    Args:
        html: レース結果のHTML

    Returns:
        list[RaceResultItem]: パースしたレース結果データ
    """
    soup = BeautifulSoup(html, "lxml")

    race_result_items: list[RaceResultItem] = []
    for item in soup.select("#contents_liquid > table > tr")[1:]:  # 1行目はヘッダーなのでスキップ
        # 着順を取得
        rank_element = item.select_one("td:nth-child(1)")
        rank = rank_element.get_text() if rank_element else ""

        # 枠番を取得
        waku_element = item.select_one("td:nth-child(2) > span")
        waku = waku_element.get_text() if waku_element else ""

        # 馬番を取得
        num_element = item.select_one("td:nth-child(3)")
        num = num_element.get_text() if num_element else ""

        # 馬情報を取得
        horse_element = item.select_one("td:nth-child(4) > a")
        horse_href: str = horse_element["href"] if horse_element is not None else ""
        horse_id_match = re.match(r"/horse/([0-9a-z]{10})", horse_href)
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
        jockey_id_match = re.match(r"/jockey/result/recent/(\d{5})", jockey_href)
        jockey_id = jockey_id_match.group(1) if jockey_id_match else ""
        jockey_name = (jockey_element.get_text() if jockey_element is not None else "").strip()
        jockey = JockeyInfoPicked(
            jockey_name=jockey_name,
            jockey_id=jockey_id,
        )

        # タイムを取得
        time_element = item.select_one("td:nth-child(8)")
        time = time_element.get_text() if time_element is not None else ""

        # 着差を取得
        margin_element = item.select_one("td:nth-child(9)")
        margin = margin_element.get_text() if margin_element is not None else ""

        # オッズを取得
        odds_element = item.select_one("td:nth-child(11)")
        odds = odds_element.get_text() if odds_element is not None else ""

        # 人気を取得
        pop_element = item.select_one("td:nth-child(12) > span")
        pop = pop_element.get_text() if pop_element is not None else ""

        # 馬体重を取得
        horse_weight_element = item.select_one("td:nth-child(13)")
        horse_weight = (horse_weight_element.get_text() if horse_weight_element else "").strip()

        race_result_items.append(
            RaceResultItem(
                rank=rank,
                waku=waku,
                num=num,
                horse=horse,
                sex_age=sex_age,
                impost_weight=impost_weight,
                jockey=jockey,
                time=time,
                margin=margin,
                odds=odds,
                pop=pop,
                horse_weight=horse_weight,
            )
        )

    return race_result_items


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
