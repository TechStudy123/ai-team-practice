from datetime import datetime

import pytest

from booking.reservations import Reservation, add, cancel, cancel_fee, fee
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


def test_予約を取り消せる():
    reservation = Reservation("A", at(10), at(11), people=2)
    other = Reservation("B", at(10), at(11), people=2)
    assert cancel(reservation, [reservation, other]) == [other]


def test_一覧にない予約を取り消すとエラーになる():
    reservation = Reservation("A", at(10), at(11), people=2)
    with pytest.raises(ValueError, match="その予約はありません"):
        cancel(reservation, [])


def test_開始24時間より前の取り消しは無料():
    reservation = Reservation("B", at(10), at(11), people=2)
    cancelled_at = datetime(2026, 11, 30, 9, 59)
    assert cancel_fee(reservation, cancelled_at) == 0


def test_開始24時間前ちょうどの取り消し料は半額():
    reservation = Reservation("B", at(10), at(11), people=2)
    cancelled_at = datetime(2026, 11, 30, 10)
    assert cancel_fee(reservation, cancelled_at) == 500


def test_開始24時間以内の取り消し料は半額():
    reservation = Reservation("B", at(10), at(11), people=2)
    cancelled_at = datetime(2026, 12, 1, 9)
    assert cancel_fee(reservation, cancelled_at) == 500
