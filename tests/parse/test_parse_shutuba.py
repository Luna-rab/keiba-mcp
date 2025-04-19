import pytest

from src.parse import parse_shutuba


@pytest.fixture
def shutuba_html() -> bytes:
    with open("tests/assets/netkeiba_shutuba_oukasho_20250413.html", "rb") as f:
        return f.read()


def test_parse_shutuba(shutuba_html: bytes) -> None:
    # Test with a valid input file
    result = parse_shutuba(shutuba_html)

    assert result.race_name == "桜花賞"
    assert result.race_id == "202509020611"
    assert result.date == "2025年4月13日"
    assert result.time == "15:40"
    assert result.place == "阪神"
    assert result.course == "芝1600m"
    assert result.weather == "雨"
    assert result.condition == "稍"

    assert len(result.shutuba) == 18
    assert result.shutuba[0].waku == 1
    assert result.shutuba[0].num == 1
    assert result.shutuba[0].horse.horse_name == "ヴーレヴー"
    assert result.shutuba[0].horse.horse_id == "2022104617"
    assert result.shutuba[0].sex_age == "牝3"
    assert result.shutuba[0].impost_weight == "55.0"
    assert result.shutuba[0].jockey.jockey_name == "浜中"
    assert result.shutuba[0].jockey.jockey_id == "01115"
    assert result.shutuba[0].odds == 38.5
    assert result.shutuba[0].pop == 10
