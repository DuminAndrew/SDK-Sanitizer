"""Тесты матчера сигнатур и базы трекеров (pytest)."""
import pytest

from sdk_sanitizer.matcher import match_trackers
from sdk_sanitizer.trackers import load_trackers


@pytest.fixture(scope="module")
def trackers():
    return load_trackers()


def test_db_has_enough_trackers(trackers):
    # Расширенная база well-known SDK.
    assert len(trackers) >= 25


def test_db_entries_well_formed(trackers):
    for t in trackers:
        assert t.get("name")
        assert isinstance(t.get("categories"), list) and t["categories"]
        # Должна быть хотя бы одна сигнатура.
        assert t.get("code_signature") or t.get("network_signature")


def test_code_match(trackers):
    tokens = [
        "com.example.app.MainActivity",
        "com.google.android.gms.ads.AdView",
        "com.appsflyer.AppsFlyerLib",
    ]
    found = match_trackers(tokens, [], trackers)
    names = {f["name"] for f in found}
    assert "Google AdMob" in names
    assert "AppsFlyer" in names
    assert all("code" in f["matched_on"] for f in found)


def test_network_match(trackers):
    found = match_trackers([], ["app-measurement.com", "graph.facebook.com"], trackers)
    names = {f["name"] for f in found}
    assert "Google Firebase Analytics" in names
    assert "Facebook (Login/Analytics/Ads)" in names


def test_new_trackers_detected(trackers):
    tokens = [
        "io.branch.referral.Branch",
        "com.segment.analytics.Analytics",
        "io.sentry.Sentry",
        "com.unity3d.ads.UnityAds",
        "com.applovin.sdk.AppLovinSdk",
        "com.huawei.hms.analytics.HiAnalytics",
    ]
    found = match_trackers(tokens, [], trackers)
    names = {f["name"] for f in found}
    for expected in ("Branch", "Segment", "Sentry", "Unity Ads", "AppLovin", "Huawei HMS Analytics"):
        assert expected in names


def test_no_false_positive_on_clean(trackers):
    found = match_trackers(
        ["com.example.clean.Service", "org.acme.util.Helper"],
        ["example.com"],
        trackers,
    )
    assert found == []


def test_results_sorted_by_name(trackers):
    found = match_trackers(
        ["com.flurry.android", "com.google.android.gms.ads", "com.amplitude.api"],
        [],
        trackers,
    )
    names = [f["name"] for f in found]
    assert names == sorted(names, key=str.lower)
