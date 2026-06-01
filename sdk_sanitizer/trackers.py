"""Загрузка базы сигнатур трекеров (локальный снапшот) + опциональное обновление из Exodus API."""
import json
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data" / "trackers_snapshot.json"
EXODUS_API = "https://reports.exodus-privacy.eu.org/api/trackers"


def load_trackers(path=None):
    p = Path(path) if path else DATA
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("trackers", [])


def fetch_trackers():
    """Скачать свежую БД трекеров Exodus (нужен requests). Данные — ODbL, требуют атрибуции."""
    import requests  # ленивый импорт
    r = requests.get(EXODUS_API, timeout=30, headers={"User-Agent": "SDK-Sanitizer/0.1"})
    r.raise_for_status()
    raw = r.json().get("trackers", {})
    items = raw.values() if isinstance(raw, dict) else raw
    out = []
    for t in items:
        out.append({
            "name": t.get("name", ""),
            "code_signature": t.get("code_signature", "") or "",
            "network_signature": t.get("network_signature", "") or "",
            "categories": t.get("categories", []) or [],
        })
    return out


def save_snapshot(trackers, path=None):
    p = Path(path) if path else DATA
    payload = {
        "_meta": {
            "description": "Снапшот сигнатур трекеров. Источник: Exodus Privacy (ODbL/DbCL). См. NOTICE.",
            "source": EXODUS_API,
            "license": "ODbL-1.0",
        },
        "trackers": trackers,
    }
    with open(p, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return len(trackers)
