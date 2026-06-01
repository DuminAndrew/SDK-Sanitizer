"""Сопоставление найденных в приложении классов/доменов с сигнатурами трекеров."""
import re


def _compile(sig):
    sig = (sig or "").strip()
    if not sig:
        return None
    try:
        return re.compile(sig)
    except re.error:
        return re.compile(re.escape(sig))


def match_trackers(tokens, domains, trackers):
    """tokens — классы/пакеты (строки), domains — домены. Возвращает список найденных трекеров."""
    token_blob = "\n".join(sorted(set(tokens)))
    domain_blob = "\n".join(sorted(set(domains)))
    found = []
    for t in trackers:
        matched = []
        cs = _compile(t.get("code_signature"))
        if cs and cs.search(token_blob):
            matched.append("code")
        ns = _compile(t.get("network_signature"))
        if ns and ns.search(domain_blob):
            matched.append("network")
        if matched:
            found.append({
                "name": t.get("name", "?"),
                "categories": t.get("categories", []),
                "matched_on": matched,
            })
    found.sort(key=lambda x: x["name"].lower())
    return found
