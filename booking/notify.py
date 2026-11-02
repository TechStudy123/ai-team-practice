"""予約確定を通知サービスへ送る。"""
import json
import os
from datetime import datetime
from urllib.request import Request, urlopen

NOTIFY_URL = "https://notify.example.com/api/messages"


def notify_reserved(room_name: str, start: datetime) -> None:
    """予約が確定したことを通知サービスへ知らせる。"""
    body = json.dumps({"room_name": room_name, "start": start.isoformat()}).encode("utf-8")
    request = Request(
        NOTIFY_URL,
        data=body,
        headers={
            "Authorization": f"Bearer {os.environ['NOTIFY_API_KEY']}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urlopen(request):
        pass