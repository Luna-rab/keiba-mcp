from bs4 import BeautifulSoup

from src.models import (
    RaceShutuba,
)


def parse_shutuba(html: bytes) -> RaceShutuba:
    """
    netkeibaの出馬表ページをパースする

    Args:
        html: 出馬表のHTML

    Returns:
        RaceShutuba: パースした出馬表データ
    """
    soup = BeautifulSoup(html, "lxml")
