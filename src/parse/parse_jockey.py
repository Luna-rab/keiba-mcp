import re

from bs4 import BeautifulSoup

from src.models import JockeyInfo


def parse_jockey(html: bytes) -> JockeyInfo:
    """騎手情報を取得する関数
    https://db.netkeiba.com/jockey/{jockey_id}/ から取得する

    Input:
        html: str - 取得したい騎手のHTML

    Output:
        JockeyInfo - 騎手情報
    """

    soup = BeautifulSoup(html, "lxml")

    # 騎手名
    jockey_element = soup.select_one("#db_main_box > div > div.db_head_name.fc > div > h1")
    jockey_name = re.sub(r"\s", "", jockey_element.get_text()) if jockey_element is not None else ""

    # 騎手ID
    jockey_id_element = soup.select_one("#db_main_box > div > div.db_head_regist.fc > ul > li:nth-child(1) > a")
    jockey_id_href: str = jockey_id_element["href"] if jockey_id_element is not None else ""
    id_match = re.match(r"https://db.netkeiba.com/jockey/(\d{5})/", jockey_id_href)
    jockey_id = id_match.group(1) if id_match else ""

    # 身長・体重
    height_weight_element = soup.select_one("#DetailTable > tbody > tr:nth-child(1) > td")
    height_weight = height_weight_element.get_text() if height_weight_element is not None else ""

    # デビュー年
    debut_year_element = soup.select_one("#DetailTable > tbody > tr:nth-child(3) > td")
    debut_year = debut_year_element.get_text() if debut_year_element is not None else ""

    # 本年勝利数
    current_year_wins_element = soup.select_one("#DetailTable > tbody > tr:nth-child(4) > td")
    current_year_wins = current_year_wins_element.get_text() if current_year_wins_element is not None else ""

    # 通算勝利数
    total_wins_element = soup.select_one("#DetailTable > tbody > tr:nth-child(5) > td")
    total_wins = total_wins_element.get_text() if total_wins_element is not None else ""

    # 本年獲得賞金
    current_year_prize_element = soup.select_one("#DetailTable > tbody > tr:nth-child(6) > td")
    current_year_prize = current_year_prize_element.get_text() if current_year_prize_element is not None else ""

    # 通算獲得賞金
    total_prize_element = soup.select_one("#DetailTable > tbody > tr:nth-child(7) > td")
    total_prize = total_prize_element.get_text() if total_prize_element is not None else ""

    # G1勝利数
    g1_wins_element = soup.select_one("#DetailTable > tbody > tr:nth-child(8) > td")
    g1_wins = g1_wins_element.get_text() if g1_wins_element is not None else ""

    # 重賞勝利数
    stakes_wins_element = soup.select_one("#DetailTable > tbody > tr:nth-child(9) > td")
    stakes_wins = stakes_wins_element.get_text() if stakes_wins_element is not None else ""

    return JockeyInfo(
        jockey_name=jockey_name,
        jockey_id=jockey_id,
        height_weight=height_weight,
        debut_year=debut_year,
        current_year_wins=current_year_wins,
        total_wins=total_wins,
        current_year_prize=current_year_prize,
        total_prize=total_prize,
        g1_wins=g1_wins,
        stakes_wins=stakes_wins,
    )
