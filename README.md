# SDK-Sanitizer 🛡️

> Scan your **Android** app (APK or source) for **hidden third-party SDK trackers** and surface the related **privacy/compliance risks (GDPR / CCPA)** — as a CLI and a GitHub Action. Local, fast, no app upload to any cloud.

![status](https://img.shields.io/badge/status-MVP-orange) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![data](https://img.shields.io/badge/tracker%20data-Exodus%20(ODbL)-purple) ![output](https://img.shields.io/badge/output-SARIF%20%7C%20JSON%20%7C%20MD-lightgrey)

## ✨ Features
- 🔍 Detects known trackers by **code signatures** (package/class names) and **network signatures** (endpoints).
- ⚖️ Maps tracker categories → **GDPR/CCPA notes** + a **severity** (low→high) for triage.
- 📦 Scans **source folders** (zero heavy deps, stdlib only) or **APK files** (`androguard`, optional).
- 🧾 Reports in **SARIF** (GitHub code scanning), **JSON** (automation), **Markdown** (humans).
- 🚦 `--fail-on` for **CI gating** (non-zero exit on findings ≥ a severity).
- 🔄 `--update` pulls the latest signature DB from the **Exodus Privacy** API.

## 🚀 Install
```bash
git clone https://github.com/DuminAndrew/SDK-Sanitizer
cd SDK-Sanitizer
pip install -e .            # gives the `sdk-sanitizer` command (core needs no extra deps)
pip install -e ".[apk]"     # + APK support (androguard)
pip install -e ".[update]"  # + live DB update (requests)
```
> Or run from source without install: `python -m sdk_sanitizer.cli <target>`

## 🧭 Usage
```bash
sdk-sanitizer ./app/src           # scan source dir → Markdown report
sdk-sanitizer app-release.apk -f json -o report.json
sdk-sanitizer . -f sarif -o sdk.sarif --fail-on high   # CI: fail if high+ trackers
sdk-sanitizer --update                                  # refresh tracker DB (Exodus)
```

### GitHub Action
```yaml
- uses: DuminAndrew/SDK-Sanitizer@v1
  with:
    target: 'app/src/main'
    format: 'sarif'
    fail-on: 'high'   # optional: fail the job
```
SARIF is uploaded to GitHub code scanning automatically.

## 🧱 Architecture
```
sdk_sanitizer/
  trackers.py   # load snapshot DB / fetch from Exodus API
  extractor.py  # source scan (stdlib) | APK scan (androguard, optional)
  matcher.py    # regex match classes/domains vs signatures
  compliance.py # category → GDPR/CCPA notes + severity
  reporters.py  # SARIF / JSON / Markdown
  cli.py        # argparse, CI exit codes
data/trackers_snapshot.json  # bundled known-tracker signatures
action.yml                   # GitHub Action (composite)
tests/                       # unit tests (no APK/network)
```
Pure, testable core (no external deps); `androguard`/`requests` are lazy/optional. Roadmap: Kotlin/dexlib2 Gradle plugin, manifest permission analysis, R8/ProGuard-aware matching.

## ⚖️ Legal & data attribution
Tracker signatures are derived from **Exodus Privacy** (ODbL/DbCL — see [`NOTICE`](NOTICE)); Exodus **source code (AGPL-3.0) is NOT used**. This tool performs heuristic static analysis and **is not legal advice**; results may include false positives (obfuscation, re-classing). Verify before acting.

## 💚 Support / Crypto donations
Replace the placeholders with your **real verified addresses + QR images** before publishing.

| Coin | Network | Address (placeholder) |
|---|---|---|
| BTC | Bitcoin | `bc1qXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` |
| ETH | Ethereum / EVM | `0xXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` |
| USDT | TRON (TRC20) | `TXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX` |

### 🔐 Donation safety
- Verify the address only from the **official release page** (not forks/issues/screenshots).
- Match the **network** (TRC20 ≠ ERC20) — wrong network = lost funds.
- Donations are voluntary; they **do not** grant support SLA or constitute investment.
- Maintainers never DM you asking for donations.

## 📄 License
MIT © DuminAndrew (code) · tracker data © Exodus Privacy contributors (ODbL).
