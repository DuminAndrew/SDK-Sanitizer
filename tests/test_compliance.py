"""Тесты оценки соответствия (severity + GDPR/CCPA-ноты)."""
from sdk_sanitizer.compliance import assess, max_severity


def test_advertisement_is_high():
    found = [{"name": "X", "categories": ["Advertisement"], "matched_on": ["code"]}]
    results = assess(found)
    assert results[0]["severity"] == "high"
    assert results[0]["compliance_notes"]


def test_crash_reporting_is_low():
    found = [{"name": "X", "categories": ["Crash reporting"], "matched_on": ["code"]}]
    results = assess(found)
    assert results[0]["severity"] == "low"


def test_takes_highest_category():
    found = [{"name": "X", "categories": ["Analytics", "Advertisement"], "matched_on": ["code"]}]
    results = assess(found)
    assert results[0]["severity"] == "high"


def test_unknown_category_defaults_medium():
    found = [{"name": "X", "categories": ["Mystery"], "matched_on": ["code"]}]
    results = assess(found)
    assert results[0]["severity"] == "medium"


def test_max_severity_none_when_empty():
    assert max_severity([]) == "none"


def test_max_severity_picks_highest():
    found = [
        {"name": "A", "categories": ["Crash reporting"], "matched_on": ["code"]},
        {"name": "B", "categories": ["Advertisement"], "matched_on": ["code"]},
    ]
    results = assess(found)
    assert max_severity(results) == "high"


def test_results_sorted_severity_desc():
    found = [
        {"name": "Low", "categories": ["Crash reporting"], "matched_on": ["code"]},
        {"name": "High", "categories": ["Advertisement"], "matched_on": ["code"]},
    ]
    results = assess(found)
    assert results[0]["name"] == "High"
