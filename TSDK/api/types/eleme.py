from typing import TypedDict, List, Dict


class SearchPoiNearbyRes(TypedDict):
    address: str
    city: str
    city_id: int
    dist: float
    distance: str
    district_adcode: str
    geohash: str
    id: str
    koubei_district_adcode: str
    koubei_prefecture_adcode: str
    latitude: float
    logTraeId: str
    longitude: float
    name: str
    prefecture_adcode: str
    prefecture_city_name: str
    prefecture_id: int
    request_id: str
    short_address: None
    source: str
    sourceFrom: None

class reverseGeoCodingRes(TypedDict):
    address: str
    city: str
    city_id: int
    dist: float
    distance: str
    district_adcode: str
    geohash: str
    koubei_district_adcode: str
    koubei_prefecture_adcode: str
    latitude: float
    longitude: float
    name: str
    prefecture_adcode: str
    prefecture_city_name: str
    prefecture_id: int
