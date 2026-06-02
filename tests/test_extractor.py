"""Тесты экстрактора исходников (включая сбор разрешений из манифеста)."""
import os

from sdk_sanitizer import extractor

EXAMPLES = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples"
)


def test_scan_examples_returns_tokens_domains_perms():
    tokens, domains, perms = extractor.scan_source(EXAMPLES)
    assert any(t.startswith("com.google.android.gms.ads") for t in tokens)
    assert "app-measurement.com" in domains
    assert "android.permission.ACCESS_FINE_LOCATION" in perms


def test_permissions_collected_only_from_manifest(tmp_path):
    manifest = tmp_path / "AndroidManifest.xml"
    manifest.write_text(
        '<manifest><uses-permission android:name="android.permission.CAMERA"/>'
        '<uses-permission android:name="android.permission.READ_SMS" /></manifest>',
        encoding="utf-8",
    )
    # Java-файл с тем же текстом не должен давать разрешений.
    (tmp_path / "Foo.java").write_text(
        'String x = "android.permission.RECORD_AUDIO";', encoding="utf-8"
    )
    _tokens, _domains, perms = extractor.scan_source(str(tmp_path))
    assert "android.permission.CAMERA" in perms
    assert "android.permission.READ_SMS" in perms
    assert "android.permission.RECORD_AUDIO" not in perms


def test_scan_empty_dir(tmp_path):
    tokens, domains, perms = extractor.scan_source(str(tmp_path))
    assert tokens == set()
    assert domains == set()
    assert perms == []
