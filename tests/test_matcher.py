"""Юнит-тесты ядра (stdlib unittest) — без APK и сети."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk_sanitizer.trackers import load_trackers
from sdk_sanitizer.matcher import match_trackers
from sdk_sanitizer.compliance import assess, max_severity
from sdk_sanitizer.reporters import to_json, to_markdown, to_sarif


class TestCore(unittest.TestCase):
    def setUp(self):
        self.trackers = load_trackers()

    def test_db_loads(self):
        self.assertGreater(len(self.trackers), 5)

    def test_code_match(self):
        tokens = ["com.example.app.MainActivity", "com.google.android.gms.ads.AdView", "com.appsflyer.AppsFlyerLib"]
        found = match_trackers(tokens, [], self.trackers)
        names = {f["name"] for f in found}
        self.assertIn("Google AdMob", names)
        self.assertIn("AppsFlyer", names)
        self.assertTrue(all("code" in f["matched_on"] for f in found))

    def test_network_match(self):
        found = match_trackers([], ["app-measurement.com", "graph.facebook.com"], self.trackers)
        names = {f["name"] for f in found}
        self.assertIn("Google Firebase Analytics", names)

    def test_no_false_positive_on_clean(self):
        found = match_trackers(["com.example.clean.Service", "org.acme.util.Helper"], ["example.com"], self.trackers)
        self.assertEqual(found, [])

    def test_assess_and_severity(self):
        found = match_trackers(["com.google.android.gms.ads"], [], self.trackers)
        results = assess(found)
        self.assertEqual(results[0]["severity"], "high")  # Advertisement → high
        self.assertTrue(results[0]["compliance_notes"])
        self.assertEqual(max_severity(results), "high")

    def test_reporters_do_not_crash(self):
        found = match_trackers(["com.flurry.android"], [], self.trackers)
        results = assess(found)
        self.assertIn("Flurry", to_markdown(results, "x", "medium"))
        self.assertIn("\"findings\"", to_json(results, "x", "medium"))
        self.assertIn("2.1.0", to_sarif(results, "x", "medium"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
