"""Тесты репортеров: SARIF/JSON/MD должны быть валидны и включать разрешения."""
import json

from sdk_sanitizer.compliance import assess
from sdk_sanitizer.matcher import match_trackers
from sdk_sanitizer.permissions import assess_permissions
from sdk_sanitizer.reporters import to_json, to_markdown, to_sarif
from sdk_sanitizer.trackers import load_trackers


def _sample():
    trackers = load_trackers()
    found = match_trackers(["com.flurry.android", "com.google.android.gms.ads"], [], trackers)
    results = assess(found)
    perms = assess_permissions([
        "android.permission.ACCESS_FINE_LOCATION",
        "android.permission.CAMERA",
    ])
    return results, perms


def test_json_is_valid_and_complete():
    results, perms = _sample()
    obj = json.loads(to_json(results, "tgt", "high", perms))
    assert obj["tool"] == "SDK-Sanitizer"
    assert obj["trackers_found"] == len(results)
    assert obj["dangerous_permissions_found"] == len(perms)
    assert obj["permissions"][0]["name"] in {"ACCESS_FINE_LOCATION", "CAMERA"}


def test_markdown_contains_sections():
    results, perms = _sample()
    md = to_markdown(results, "tgt", "high", perms)
    assert "# SDK-Sanitizer" in md
    assert "Google AdMob" in md
    assert "Опасные разрешения" in md
    assert "ACCESS_FINE_LOCATION" in md


def test_markdown_empty_results():
    md = to_markdown([], "tgt", "none", [])
    assert "Трекеры из базы не обнаружены" in md


def test_sarif_is_valid_2_1_0():
    results, perms = _sample()
    obj = json.loads(to_sarif(results, "tgt", "high", perms))
    assert obj["version"] == "2.1.0"
    run = obj["runs"][0]
    assert run["tool"]["driver"]["name"] == "SDK-Sanitizer"
    # Результатов столько же, сколько трекеров + разрешений.
    assert len(run["results"]) == len(results) + len(perms)
    # Все ruleId результатов присутствуют среди rules.
    rule_ids = {r["id"] for r in run["tool"]["driver"]["rules"]}
    for res in run["results"]:
        assert res["ruleId"] in rule_ids
        assert res["level"] in {"error", "warning", "note"}


def test_reporters_handle_no_permissions():
    results, _ = _sample()
    # perms по умолчанию None — не должно падать.
    assert "findings" in to_json(results, "x", "high")
    assert "SDK-Sanitizer" in to_markdown(results, "x", "high")
    assert "2.1.0" in to_sarif(results, "x", "high")
