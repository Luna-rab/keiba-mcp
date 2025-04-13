import httpx


def get_race_shutuba_html(race_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            "https://race.netkeiba.com/race/shutuba.html",
            params={
                "race_id": race_id,
            },
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


def get_race_result_html(race_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/race/{race_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


def get_horse_profile_html(horse_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/horse/{horse_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


def get_horse_result_html(horse_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/horse/result/{horse_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


def get_horse_ped_html(horse_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/horse/ped/{horse_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content


def get_jockey_profile_html(jockey_id: str) -> bytes:
    with httpx.Client() as client:
        response = client.get(
            f"https://db.netkeiba.com/jockey/{jockey_id}",
        )
        if response.status_code != httpx.codes.OK:
            raise Exception(f"Failed to fetch data: {response.status_code}")

        return response.content
