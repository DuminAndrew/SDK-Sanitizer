# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-02

### Added

- Initial release of **SDK-Sanitizer** — a local, static scanner for hidden
  third-party SDK trackers and privacy (GDPR/CCPA) risks in Android apps.
- Dual signature matching: **code signatures** (package/class names) and
  **network signatures** (endpoints), regex-based with literal fallback.
- Compliance assessment mapping tracker categories to **severity** and
  **GDPR/CCPA notes** (`compliance.py`).
- **Manifest permission analysis** (`permissions.py`): dangerous permissions are
  mapped to a severity and a GDPR/CCPA note, collected from `AndroidManifest.xml`
  for source scans and via `androguard` for APKs.
- Three report formats: **SARIF** (GitHub code scanning), **JSON** (automation),
  and **Markdown** (human review) — all including the permission findings.
- Bundled signature snapshot of ~30 well-known SDKs (AdMob, Firebase
  Analytics/Crashlytics, Fabric, GA, GTM, Facebook, Flurry, Yandex AppMetrica,
  AppsFlyer, Amplitude, Adjust, OneSignal, Mixpanel, Branch, Segment, Sentry,
  Bugsnag, Unity Ads, AppLovin, ironSource, Vungle, Chartboost, Tapjoy, Comscore,
  Braze, CleverTap, Localytics, Kochava, Singular, Tealium, HockeyApp, Instabug,
  Huawei HMS Analytics).
- `--update` to refresh the local database from the Exodus Privacy API.
- CLI with `-f/--format`, `-o/--output`, `--fail-on`, `--db`, `--update`.
- Composite **GitHub Action** with optional SARIF upload to code scanning.
- `--fail-on` CI gate (exit code `2` when max severity meets a threshold).
- Test suite (`pytest`) covering matcher, compliance, permissions, reporters,
  the extractor, and no-false-positive behaviour.
- `ruff` linting configuration and a CI workflow with a Python 3.9–3.12 matrix.
- Example fake Android source tree under `examples/` for demos.

### Attribution

- Tracker signature concepts, categories, and data are derived from the
  [Exodus Privacy](https://exodus-privacy.eu.org/) project (ODbL/DbCL). See
  [`NOTICE`](NOTICE).

[Unreleased]: https://github.com/DuminAndrew/SDK-Sanitizer/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/DuminAndrew/SDK-Sanitizer/releases/tag/v0.1.0
