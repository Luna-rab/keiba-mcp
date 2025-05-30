import asyncio
import json

from mcp.server.fastmcp import FastMCP

from src.clients import (
    get_horse_profile_html,
    get_jockey_profile_html,
    get_race_result_html,
    get_race_shutuba_html,
)
from src.parse.parse_horse import parse_horse_profile
from src.parse.parse_jockey import parse_jockey
from src.parse.parse_race import parse_race_result
from src.parse.parse_shutuba import parse_shutuba

# Initialize FastMCP server
mcp = FastMCP("weather")


@mcp.tool()
async def get_shutuba(race_id: str) -> str:
    """競馬のレース出馬表情報を取得する関数
    https://race.netkeiba.com/race/shutuba.html から取得する

    Input:
        race_id: str - 取得したいレースのID

    Output:
        str - 出馬表データをJSON形式にシリアライズした文字列
        出力されるJSONオブジェクトには以下の情報が含まれます：
        - race_name: レース名
        - race_id: レースID
        - date: 開催日
        - time: 発走時刻
        - place: 開催場所
        - course: コース情報
        - weather: 天候
        - condition: 馬場状態
        - shutuba: 出走馬の情報のリスト。各要素には以下が含まれます：
          - waku: 枠番
          - num: 馬番
          - horse: 馬情報（horse_name: 馬名, horse_id: 馬ID）
          - sex_age: 性齢
          - impost_weight: 斤量
          - jockey: 騎手情報（jockey_name: 騎手名, jockey_id: 騎手ID）
          - horse_weight: 馬体重
          - odds: オッズ
          - pop: 人気順位

    レースIDを元にHTMLを取得し、パーサーで構造化された出馬表データに変換して返します。
    """
    html = await get_race_shutuba_html(race_id)
    shutuba = parse_shutuba(html)

    return shutuba.model_dump_json()


@mcp.tool()
async def get_race_result(race_id: str) -> str:
    """競馬のレース結果情報を取得する関数
    https://db.netkeiba.com/race/{race_id}/ から取得する

    Input:
        race_id: str - 取得したいレースのID

    Output:
        str - レース結果データをJSON形式にシリアライズした文字列
        出力されるJSONオブジェクトには以下の情報が含まれます：
        - race_name: レース名
        - race_id: レースID
        - date: 開催日
        - time: 発走時刻
        - place: 開催場所
        - course: コース情報
        - weather: 天候
        - condition: 馬場状態
        - results: 着順情報のリスト。各要素には以下の情報が含まれます：
          - rank: 着順
          - waku: 枠番
          - num: 馬番
          - horse: 馬情報（horse_name: 馬名, horse_id: 馬ID）
          - sex_age: 性齢
          - impost_weight: 斤量
          - jockey: 騎手情報（jockey_name: 騎手名, jockey_id: 騎手ID）
          - time: タイム
          - margin: 着差
          - odds: オッズ
          - pop: 人気順位
          - horse_weight: 馬体重

    レースIDを元にHTMLを取得し、パーサーで構造化されたレース結果データに変換して返します。
    """
    html = await get_race_result_html(race_id)
    result = parse_race_result(html)

    return result.model_dump_json()



@mcp.tool()
async def bulk_get_horse_profile(horse_ids: list[str]) -> str:
    """競馬の馬プロフィール情報を一括取得する関数
    https://db.netkeiba.com/horse/{horse_id}/ から取得する

    Input:
        horse_id: list[str] - 取得したい馬のID配列

    Output:
        str - 馬プロフィールデータをJSON形式にシリアライズした文字列
        出力されるJSONオブジェクトには以下の情報が含まれます：
        [
            - horse_name: 馬名
            - horse_id: 馬ID
            - birth: 生年月日
            - total_prize: 獲得賞金
            - total_record: 通算成績
            - ped: 血統情報。以下の情報が含まれます：
                - father: 父馬情報（horse_name: 馬名, horse_id: 馬ID）
                - mother: 母馬情報（horse_name: 馬名, horse_id: 馬ID）
                - father_father: 父の父情報（horse_name: 馬名, horse_id: 馬ID）
                - father_mother: 父の母情報（horse_name: 馬名, horse_id: 馬ID）
                - mother_father: 母の父情報（horse_name: 馬名, horse_id: 馬ID）
                - mother_mother: 母の母情報（horse_name: 馬名, horse_id: 馬ID）
            - race_result: レース結果情報のリスト。各要素には以下の情報が含まれます：
                - race: レース情報（race_name: レース名, race_id: レースID）
                - race_date: レース日
                - place: 開催場所
                - weather: 天候
                - course: コース
                - condition: 馬場状態
                - horse_number: 頭数
                - rank: 着順
                - waku: 枠
                - num: 馬番
                - impost_weight: 斤量
                - jockey: 騎手情報（jockey_name: 騎手名, jockey_id: 騎手ID）
                - time: タイム
                - margin: 着差
                - odds: オッズ
                - pop: 人気
                - horse_weight: 馬体重
        ]

    馬IDを元にHTMLを取得し、パーサーで構造化された馬プロフィールデータに変換して返します。
    """
    coroutines = [get_horse_profile_html(horse_id) for horse_id in horse_ids]
    htmls = await asyncio.gather(*coroutines)

    profiles = [parse_horse_profile(html).model_dump() for html in htmls]
    return json.dumps(profiles, ensure_ascii=False)


@mcp.tool()
async def bulk_get_jockey_profile(jockey_ids: list[str]) -> str:
    """騎手のプロフィール情報を一括取得する関数
    https://db.netkeiba.com/jockey/{jockey_id}/ から取得する

    Input:
        jockey_id: str - 取得したい騎手のID配列

    Output:
        str - 騎手プロフィールデータをJSON形式にシリアライズした文字列
        出力されるJSONオブジェクトには以下の情報が含まれます：
        [
            - jockey_name: 騎手名
            - jockey_id: 騎手ID
            - height_weight: 身長・体重
            - debut_year: デビュー年
            - current_year_wins: 本年勝利数
            - total_wins: 通算勝利数
            - current_year_prize: 本年獲得賞金
            - total_prize: 通算獲得賞金
            - g1_wins: G1勝利数
            - stakes_wins: 重賞勝利数
        ]

    騎手IDを元にHTMLを取得し、パーサーで構造化された騎手プロフィールデータに変換して返します。
    """
    coroutines = [get_jockey_profile_html(jockey_id) for jockey_id in jockey_ids]
    htmls = await asyncio.gather(*coroutines)

    profiles = [parse_jockey(html).model_dump() for html in htmls]
    return json.dumps(profiles, ensure_ascii=False)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
