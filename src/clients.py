import httpx
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


async def get_race_shutuba_html(race_id: str) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Remote(command_executor="http://selenium:4444/wd/hub", options=options)

    try:
        url = f"https://race.netkeiba.com/race/shutuba.html?race_id={race_id}"
        driver.get(url)

        # ページが完全に読み込まれるのを待つ
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # HTMLコンテンツを取得
        html_content = driver.page_source

        return html_content
    finally:
        driver.quit()


async def get_race_result_html(race_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/race/{race_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


async def get_horse_profile_html(horse_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/horse/{horse_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


async def get_horse_result_html(horse_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/horse/result/{horse_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


async def get_horse_ped_html(horse_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/horse/ped/{horse_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


async def get_jockey_profile_html(jockey_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/jockey/{jockey_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content
