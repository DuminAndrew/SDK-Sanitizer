"""Тесты анализа разрешений манифеста."""
from sdk_sanitizer.permissions import (
    assess_permissions,
    max_permission_severity,
    normalize,
)


def test_normalize_strips_prefix():
    assert normalize("android.permission.CAMERA") == "CAMERA"
    assert normalize("CAMERA") == "CAMERA"


def test_dangerous_permission_detected():
    res = assess_permissions(["android.permission.ACCESS_FINE_LOCATION"])
    assert len(res) == 1
    assert res[0]["name"] == "ACCESS_FINE_LOCATION"
    assert res[0]["severity"] == "high"
    assert res[0]["note"]


def test_benign_permissions_ignored():
    res = assess_permissions([
        "android.permission.INTERNET",
        "android.permission.ACCESS_NETWORK_STATE",
        "android.permission.VIBRATE",
    ])
    assert res == []


def test_background_location_is_critical():
    res = assess_permissions(["android.permission.ACCESS_BACKGROUND_LOCATION"])
    assert res[0]["severity"] == "critical"


def test_duplicates_collapsed():
    res = assess_permissions([
        "android.permission.CAMERA",
        "android.permission.CAMERA",
        "CAMERA",
    ])
    assert len(res) == 1


def test_sorted_by_severity_desc():
    res = assess_permissions([
        "android.permission.POST_NOTIFICATIONS",  # low
        "android.permission.READ_SMS",            # critical
        "android.permission.CAMERA",              # high
    ])
    sevs = [r["severity"] for r in res]
    assert sevs == ["critical", "high", "low"]


def test_max_permission_severity():
    res = assess_permissions([
        "android.permission.POST_NOTIFICATIONS",
        "android.permission.READ_SMS",
    ])
    assert max_permission_severity(res) == "critical"


def test_max_permission_severity_none():
    assert max_permission_severity([]) == "none"
