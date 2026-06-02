# Contributing to SDK-Sanitizer

Thanks for taking the time to contribute! This project welcomes bug reports,
new tracker signatures, permission mappings, and improvements to the scanner.

## Ways to contribute

- **New tracker signatures** — add a well-known SDK to `data/trackers_snapshot.json`
  with a real `code_signature` (package/class), `network_signature` (endpoint), and
  correct `categories`. Include a test in `tests/test_matcher.py`.
- **Permission mappings** — extend `sdk_sanitizer/permissions.py` with a dangerous
  permission, its severity, and a GDPR/CCPA note.
- **Bug fixes / features** — see the roadmap in the README.
- **Docs** — clarifications and examples are always welcome.

## Development setup

```bash
git clone https://github.com/DuminAndrew/SDK-Sanitizer
cd SDK-Sanitizer
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

## Before opening a pull request

Run the full local check — it mirrors CI and must be green:

```bash
ruff check .
pytest -q
python -m sdk_sanitizer.cli examples -f md
```

- Keep the **core** (`trackers`, `matcher`, `compliance`, `permissions`, `reporters`)
  dependency-free (standard library only). `androguard` and `requests` stay lazy and
  optional.
- Add or update tests for any behaviour change.
- Follow the existing code style; `ruff` enforces it.
- Use clear, focused commits and a descriptive PR title.

## Tracker signature guidelines

- Use **stable** package roots (e.g. `com.appsflyer`), not fragile inner-class names.
- Escape regex metacharacters in signatures (the matcher falls back to literal on
  invalid patterns, but explicit is better).
- Prefer first-party documented endpoints for `network_signature`.
- Map categories accurately — severity is derived from them in `compliance.py`.

## Code of Conduct

By participating you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

By contributing, you agree that your contributions are licensed under the
project's [MIT License](LICENSE). Tracker signature data remains attributed to
Exodus Privacy (ODbL/DbCL) — see [`NOTICE`](NOTICE).
