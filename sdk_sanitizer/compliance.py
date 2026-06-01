"""Маппинг категорий трекеров на риски GDPR/CCPA и серьёзность.
Это эвристика, НЕ юридическая консультация."""

SEV_ORDER = {"low": 1, "medium": 2, "high": 3, "critical": 4}

CATEGORY_SEVERITY = {
    "Advertisement": "high",
    "Identification": "high",
    "Location": "high",
    "Profiling": "high",
    "Analytics": "medium",
    "Crash reporting": "low",
    "Notifications": "low",
}

GDPR_NOTES = {
    "Advertisement": "Реклама/таргетинг: требует явного согласия (GDPR ст.6(1)(a) + ePrivacy); CCPA — право на opt-out продажи/передачи данных.",
    "Analytics": "Аналитика обрабатывает ПД: нужна правовая основа и раскрытие в политике приватности (GDPR ст.13).",
    "Identification": "Идентификация устройства/пользователя — высокая чувствительность, явное согласие обязательно.",
    "Location": "Геоданные — особый риск, требуется явное согласие и минимизация.",
    "Profiling": "Профилирование (GDPR ст.22): прозрачность и право на возражение.",
    "Crash reporting": "Краш-репорты могут содержать ПД (стек, идентификаторы) — раскрыть в политике.",
}


def assess(found):
    results = []
    for f in found:
        sev = "low"
        notes = []
        for c in f.get("categories", []):
            s = CATEGORY_SEVERITY.get(c, "medium")
            if SEV_ORDER[s] > SEV_ORDER[sev]:
                sev = s
            if c in GDPR_NOTES and GDPR_NOTES[c] not in notes:
                notes.append(GDPR_NOTES[c])
        results.append({**f, "severity": sev, "compliance_notes": notes})
    results.sort(key=lambda r: (-SEV_ORDER[r["severity"]], r["name"].lower()))
    return results


def max_severity(results):
    order = {"none": 0, **SEV_ORDER}
    m = "none"
    for r in results:
        if order.get(r["severity"], 0) > order[m]:
            m = r["severity"]
    return m
