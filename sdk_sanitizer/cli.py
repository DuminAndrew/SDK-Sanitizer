"""CLI: sdk-sanitizer <apk|папка> [-f md|json|sarif] [--fail-on LEVEL]."""
import argparse
import os
import sys

from .trackers import load_trackers, fetch_trackers, save_snapshot
from .matcher import match_trackers
from .compliance import assess, max_severity, SEV_ORDER
from .reporters import to_json, to_markdown, to_sarif
from . import extractor


def main(argv=None):
    p = argparse.ArgumentParser(prog="sdk-sanitizer",
                                description="Скан Android-приложения (APK/исходники) на трекеры и риски приватности (GDPR/CCPA).")
    p.add_argument("target", nargs="?", help="путь к .apk или папке исходников")
    p.add_argument("-f", "--format", choices=["md", "json", "sarif"], default="md")
    p.add_argument("-o", "--output", help="файл отчёта (по умолчанию stdout)")
    p.add_argument("--fail-on", choices=["low", "medium", "high", "critical"],
                   help="ненулевой код возврата, если макс. серьёзность >= уровня (для CI)")
    p.add_argument("--db", help="свой JSON с трекерами")
    p.add_argument("--update", action="store_true", help="обновить локальную БД из Exodus API и выйти")
    args = p.parse_args(argv)

    if args.update:
        try:
            data = fetch_trackers()
            n = save_snapshot(data)
            print(f"БД трекеров обновлена: {n} записей (источник: Exodus, ODbL).")
            return 0
        except Exception as e:
            print(f"Ошибка обновления: {e}", file=sys.stderr)
            return 1

    if not args.target:
        p.error("укажите путь к .apk или папке исходников")

    trackers = load_trackers(args.db)

    if os.path.isdir(args.target):
        tokens, domains, _perms = extractor.scan_source(args.target)
    elif args.target.lower().endswith(".apk") and os.path.isfile(args.target):
        try:
            tokens, domains, _perms = extractor.scan_apk(args.target)
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            return 1
    else:
        p.error("target должен быть существующим .apk или папкой")

    found = match_trackers(tokens, domains, trackers)
    results = assess(found)
    msev = max_severity(results)

    report = {"md": to_markdown, "json": to_json, "sarif": to_sarif}[args.format](results, args.target, msev)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Отчёт сохранён: {args.output} | трекеров: {len(results)} | макс. серьёзность: {msev}")
    else:
        sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None
        print(report)

    if args.fail_on:
        order = {"none": 0, **SEV_ORDER}
        if order.get(msev, 0) >= order[args.fail_on]:
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
