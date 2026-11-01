"""予約の登録と料金の計算。"""
from dataclasses import dataclass
from datetime import datetime

from booking.rooms import Room, find_room

OPEN_HOUR = 9    # 9時から
CLOSE_HOUR = 18  # 18時まで


@dataclass(frozen=True)
class Reservation:
    room_id: str
    start: datetime
    end: datetime
    people: int


def overlaps(a: Reservation, b: Reservation) -> bool:
    """同じ部屋で時間が重なっていれば True。"""
    if a.room_id != b.room_id:
        return False
    return a.start <= b.end and b.start <= a.end


def check(new: Reservation, existing: list[Reservation]) -> None:
    """予約できるかを確かめる。できなければ ValueError。"""
    room = find_room(new.room_id)
    if new.end <= new.start:
        raise ValueError("終わりの時刻は始まりより後にしてください")
    if new.start.hour < OPEN_HOUR or new.end.hour > CLOSE_HOUR or (
        new.end.hour == CLOSE_HOUR and new.end.minute > 0
    ):
        raise ValueError(f"予約できるのは {OPEN_HOUR}時から{CLOSE_HOUR}時までです")
    if new.people > room.capacity:
        raise ValueError(f"{room.name}の定員は{room.capacity}人です")
    for r in existing:
        if overlaps(new, r):
            raise ValueError("その時間はすでに予約があります")


def add(new: Reservation, existing: list[Reservation]) -> list[Reservation]:
    """確かめてから予約を足した新しい一覧を返す。"""
    check(new, existing)
    return [*existing, new]


def fee(room: Room, start: datetime, end: datetime) -> int:
    """料金（円）。30分単位で切り上げる。"""
    minutes = int((end - start).total_seconds() // 60)
    blocks = -(-minutes // 30)  # 30分単位の切り上げ
    return blocks * room.price_per_hour // 2
