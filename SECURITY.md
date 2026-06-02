# Security Policy

## Supported Versions

SDK-Sanitizer is in active development. Security fixes are applied to the latest
released version on the `main` branch.

| Version | Supported          |
|---------|--------------------|
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it **privately** — do not
open a public issue.

- Email **duminandrew@gmail.com** with a clear description and reproduction steps.
- Alternatively, use GitHub's [private security advisories](https://github.com/DuminAndrew/SDK-Sanitizer/security/advisories/new).

Please include:

- The affected component (e.g. extractor, matcher, CLI, GitHub Action).
- Steps to reproduce or a proof-of-concept.
- The potential impact as you see it.

You can expect an initial acknowledgement within **5 business days**. Once a fix
is available, a coordinated disclosure timeline will be agreed upon.

## Scope and design notes

SDK-Sanitizer performs **local, static** analysis. The core uses only the Python
standard library and never uploads the scanned app or transmits data, except:

- `--update`, which fetches the public Exodus Privacy tracker database over HTTPS.

Be mindful that scan inputs (APKs, source trees) may be untrusted. The tool reads
files as text with errors ignored and does not execute scanned code.
