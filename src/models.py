from pydantic import BaseModel, Field


class RaceShutuba(BaseModel):
    race_name: str = Field(..., description="レース名")
    race_id: str = Field(..., description="レースID")
    date: str = Field(..., description="日付")
    time: str = Field(..., description="発走時刻")
    place: str = Field(..., description="開催場所")
    course: str = Field(..., description="コース")
    weather: str = Field(..., description="天候")
    condition: str = Field(..., description="馬場状態")
    shutuba: list["RaceShutubaItem"] = Field(..., description="出馬表")


class RaceShutubaItem(BaseModel):
    waku: int = Field(..., description="枠")
    num: int = Field(..., description="馬番")
    horse: "HorseProfilePicked" = Field(..., description="馬情報")
    sex_age: str = Field(..., description="性齢")
    impost_weight: str = Field(..., description="斤量")
    jockey: "JockeyInfoPicked" = Field(..., description="騎手情報")
    horse_weight: str = Field(..., description="馬体重")
    odds: str = Field(..., description="オッズ")
    pop: str = Field(..., description="人気")


class RaceResult(BaseModel):
    race_name: str = Field(..., description="レース名")
    race_id: str = Field(..., description="レースID")
    date: str = Field(..., description="日付")
    time: str = Field(..., description="発走時刻")
    place: str = Field(..., description="開催場所")
    distance: str = Field(..., description="距離")
    course: str = Field(..., description="コース")
    weather: str = Field(..., description="天候")
    condition: str = Field(..., description="馬場状態")
    results: list["RaceResultItem"] = Field(..., description="レース結果")


class RaceResultPicked(BaseModel):
    race_name: str = Field(..., description="レース名")
    race_id: str = Field(..., description="レースID")


class RaceResultItem(BaseModel):
    rank: int = Field(..., description="着順")
    waku: int = Field(..., description="枠")
    num: int = Field(..., description="馬番")
    horse: "HorseProfilePicked" = Field(..., description="馬情報")
    sex_age: str = Field(..., description="性齢")
    weight: str = Field(..., description="斤量")
    jockey: "JockeyInfoPicked" = Field(..., description="騎手情報")
    time: str = Field(..., description="タイム")
    margin: str = Field(..., description="着差")
    odds: float = Field(..., description="オッズ")
    pop: int = Field(..., description="人気")
    horse_weight: str = Field(..., description="馬体重")


class HorseProfile(BaseModel):
    horse_name: str = Field(..., description="馬名")
    horse_id: str = Field(..., description="馬ID")
    birth: str = Field(..., description="生年月日")
    trainer: str = Field(..., description="調教師")
    trainer_id: str = Field(..., description="調教師ID")
    owner: str = Field(..., description="馬主")
    owner_id: str = Field(..., description="馬主ID")
    breeder: str = Field(..., description="生産者")
    breeder_id: str = Field(..., description="生産者ID")
    area: str = Field(..., description="産地")
    seri: str = Field(..., description="セリ取引価格")
    total_prize: str = Field(..., description="獲得賞金")
    total_record: str = Field(..., description="通算成績")


class HorseProfilePicked(BaseModel):
    horse_name: str = Field(..., description="馬名")
    horse_id: str = Field(..., description="馬ID")


class HorsePed(BaseModel):
    horse_name: str = Field(..., description="馬名")
    horse_id: str = Field(..., description="馬ID")
    father: HorseProfilePicked = Field(..., description="父")
    mother: HorseProfilePicked = Field(..., description="母")
    father_father: HorseProfilePicked = Field(..., description="父の父")
    father_mother: HorseProfilePicked = Field(..., description="父の母")
    mother_father: HorseProfilePicked = Field(..., description="母の父")
    mother_mother: HorseProfilePicked = Field(..., description="母の母")


class HorseRaceResult(BaseModel):
    horse_name: str = Field(..., description="馬名")
    horse_id: str = Field(..., description="馬ID")
    race_result: list["HorseRaceResultItem"] = Field(..., description="レース結果")


class HorseRaceResultItem(BaseModel):
    race_result: list[RaceResultPicked] = Field(..., description="レース結果")
    race_date: str = Field(..., description="レース日")
    horse_number: int = Field(..., description="頭数")
    rank: int = Field(..., description="着順")
    waku: int = Field(..., description="枠")
    num: int = Field(..., description="馬番")
    weight: str = Field(..., description="斤量")
    jockey: "JockeyInfoPicked" = Field(..., description="騎手情報")
    time: str = Field(..., description="タイム")
    margin: str = Field(..., description="着差")
    odds: float = Field(..., description="オッズ")
    pop: int = Field(..., description="人気")
    horse_weight: str = Field(..., description="馬体重")


class JockeyInfo(BaseModel):
    jockey_name: str = Field(..., description="騎手名")
    jockey_id: str = Field(..., description="騎手ID")
    height_weight: str = Field(..., description="身長(cm)/体重(kg)")
    debut_year: str = Field(..., description="デビュー年")
    current_year_wins_central: str = Field(..., description="本年勝利数")
    total_wins_central: str = Field(..., description="通算勝利数")
    current_year_prize_central: str = Field(..., description="本年獲得賞金(円)")
    total_prize_central: str = Field(..., description="通算獲得賞金(円)")
    g1_wins_central: str = Field(..., description="GI勝利数")
    stakes_wins_central: str = Field(..., description="重賞勝利数")


class JockeyInfoPicked(BaseModel):
    jockey_name: str = Field(..., description="騎手名")
    jockey_id: str = Field(..., description="騎手ID")
