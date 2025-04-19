from mcp.server.fastmcp import FastMCP

from src.clients import get_race_result_html, get_race_shutuba_html
from src.parse import parse_race_result, parse_shutuba

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
        - results: 着順情報のリスト。各要素には以下が含まれます：
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


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport="stdio")
