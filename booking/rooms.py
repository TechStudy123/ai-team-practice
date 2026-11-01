"""会議室の一覧。"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    room_id: str
    name: str
    capacity: int
    price_per_hour: int  # 1時間あたりの料金（円）


ROOMS = {
    "A": Room("A", "会議室A", 4, 500),
    "B": Room("B", "会議室B", 8, 1000),
    "C": Room("C", "大会議室", 20, 3000),
}


def find_room(room_id: str) -> Room:
    """部屋の ID から部屋を探す。無ければ KeyError。"""
    return ROOMS[room_id]
