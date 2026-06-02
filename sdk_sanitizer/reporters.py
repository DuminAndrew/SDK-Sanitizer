"""Форматирование отчёта: Markdown / JSON / SARIF (для CI)."""
import json


def to_json(results, target, max_sev, perms=None):
    perms = perms or []
    return json.dumps({
        "tool": "SDK-Sanitizer",
        "target": target,
        "max_severity": max_sev,
        "trackers_found": len(results),
        "findings": results,
        "dangerous_permissions_found": len(perms),
        "permissions": perms,
    }, ensure_ascii=False, indent=2)


def to_markdown(results, target, max_sev, perms=None):
    perms = perms or []
    L = ["# SDK-Sanitizer — отчёт", "",
         f"**Цель:** `{target}`  ",
         f"**Найдено трекеров:** {len(results)}  ",
         f"**Опасных разрешений:** {len(perms)}  ",
         f"**Макс. серьёзность:** `{max_sev}`", ""]
    if not results:
        L.append("✅ Трекеры из базы не обнаружены.")
    else:
        L += ["## Трекеры", "",
              "| Трекер | Категории | Совпадение | Серьёзность |", "|---|---|---|---|"]
        for r in results:
            L.append(f"| {r['name']} | {', '.join(r['categories'])} | {', '.join(r['matched_on'])} | {r['severity']} |")
        L += ["", "## Замечания по приватности (GDPR/CCPA)"]
        for r in results:
            if r["compliance_notes"]:
                L.append(f"- **{r['name']}**:")
                for n in r["compliance_notes"]:
                    L.append(f"  - {n}")

    if perms:
        L += ["", "## Опасные разрешения манифеста", "",
              "| Разрешение | Серьёзность | Замечание (GDPR/CCPA) |", "|---|---|---|"]
        for pms in perms:
            L.append(f"| `{pms['name']}` | {pms['severity']} | {pms['note']} |")

    L += ["", "> ⚠️ Не юридическая консультация. Эвристический статический анализ; возможны ложные срабатывания (обфускация R8/ProGuard, реклассинг). Данные сигнатур — Exodus Privacy (ODbL), см. NOTICE."]
    return "\n".join(L)


def to_sarif(results, target, max_sev, perms=None):
    perms = perms or []
    rules, sarif_results, seen = [], [], set()
    level_map = {"critical": "error", "high": "error", "medium": "warning", "low": "note"}
    for r in results:
        rid = "tracker/" + r["name"].lower().replace(" ", "_").replace("(", "").replace(")", "").replace("/", "-")
        if rid not in seen:
            seen.add(rid)
            rules.append({"id": rid, "name": r["name"],
                          "shortDescription": {"text": f"Трекер {r['name']} ({', '.join(r['categories'])})"}})
        sarif_results.append({
            "ruleId": rid,
            "level": level_map.get(r["severity"], "warning"),
            "message": {"text": f"Обнаружен трекер {r['name']} [{', '.join(r['matched_on'])}]; категории: {', '.join(r['categories'])}"},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": target}}}],
        })
    for pms in perms:
        rid = "permission/" + pms["name"].lower()
        if rid not in seen:
            seen.add(rid)
            rules.append({"id": rid, "name": pms["name"],
                          "shortDescription": {"text": f"Опасное разрешение {pms['name']}"}})
        sarif_results.append({
            "ruleId": rid,
            "level": level_map.get(pms["severity"], "warning"),
            "message": {"text": f"Опасное разрешение {pms['permission']}: {pms['note']}"},
            "locations": [{"physicalLocation": {"artifactLocation": {"uri": target}}}],
        })
    return json.dumps({
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{"tool": {"driver": {"name": "SDK-Sanitizer", "version": "0.1.0", "informationUri": "https://github.com/DuminAndrew/SDK-Sanitizer", "rules": rules}}, "results": sarif_results}],
    }, ensure_ascii=False, indent=2)
