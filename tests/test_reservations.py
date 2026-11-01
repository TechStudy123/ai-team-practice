from datetime import datetime

import pytest

from booking.reservations import Reservation, add, fee
from booking.rooms import find_room


def at(hour: int, minute: int = 0) -> datetime:
    return datetime(2026, 12, 1, hour, minute)


def test_予約を足せる():
    r = Reservation("A", at(10), at(11), people=3)
    assert add(r, []) == [r]


def test_同じ部屋で時間が重なると予約できない():
    first = Reservation("A", at(10), at(12), people=2)
    second = Reservation("A", at(11), at(13), people=2)
    with pytest.raises(ValueError):
        add(second, [first])


def test_ちがう部屋なら同じ時間でも予約できる():
    first = Reservation("A", at(10), at(12), people=2)
    second = Reservation("B", at(10), at(12), people=2)
    assert len(add(second, [first])) == 2


def test_定員をこえると予約できない():
    with pytest.raises(ValueError):
        add(Reservation("A", at(10), at(11), people=5), [])


def test_営業時間の外は予約できない():
    with pytest.raises(ValueError):
        add(Reservation("A", at(8), at(10), people=2), [])


def test_料金は30分単位で切り上げる():
    room = find_room("B")  # 1時間 1000円
    assert fee(room, at(10), at(11)) == 1000
    assert fee(room, at(10), at(11, 10)) == 1500
