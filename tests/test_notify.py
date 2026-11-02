import json
from datetime import datetime
from io import BytesIO

import booking.notify as notify


def test_予約を通知サービスへ送る(monkeypatch):
    sent_requests = []

    def fake_urlopen(request):
        sent_requests.append(request)
        return BytesIO()

    monkeypatch.setenv("NOTIFY_API_KEY", "test-key")
    monkeypatch.setattr(notify, "urlopen", fake_urlopen)

    notify.notify_reserved("会議室A", datetime(2026, 12, 1, 10, 30))

    request = sent_requests[0]
    assert request.full_url == "https://notify.example.com/api/messages"
    assert request.method == "POST"
    assert json.loads(request.data) == {
        "room_name": "会議室A",
        "start": "2026-12-01T10:30:00",
    }
    assert request.get_header("Authorization") == "Bearer test-key"
    assert request.get_header("Content-type") == "application/json"