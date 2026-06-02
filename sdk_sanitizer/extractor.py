"""Извлечение классов/пакетов и доменов из исходников или APK.
Исходники — только stdlib. APK — через androguard (опционально)."""
import os
import re
from pathlib import Path

SRC_EXT = {".java", ".kt", ".kts", ".xml", ".gradle", ".smali", ".json", ".properties", ".txt", ".pro"}
PKG_RE = re.compile(r"[a-zA-Z][\w]+(?:\.[a-zA-Z][\w]+){2,}")
DOMAIN_RE = re.compile(r"https?://([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})")
PERM_RE = re.compile(
    r"<uses-permission[^>]*android:name\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE
)
SKIP_DIRS = (os.sep + "node_modules", os.sep + ".git", os.sep + "build", os.sep + ".gradle", os.sep + ".idea")


def scan_source(root):
    """Возвращает (tokens, domains, permissions[]) — для папки исходников.

    permissions собираются из всех AndroidManifest.xml через <uses-permission>.
    """
    root = Path(root)
    tokens, domains, perms = set(), set(), set()
    for dp, _dns, fns in os.walk(root):
        if any(s in dp for s in SKIP_DIRS):
            continue
        for fn in fns:
            if Path(fn).suffix.lower() not in SRC_EXT:
                continue
            try:
                txt = Path(dp, fn).read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            tokens.update(PKG_RE.findall(txt))
            domains.update(DOMAIN_RE.findall(txt))
            if fn.lower() == "androidmanifest.xml":
                perms.update(PERM_RE.findall(txt))
    return tokens, domains, sorted(perms)


def scan_apk(path):
    """Возвращает (tokens, domains, permissions[]) — для APK (нужен androguard)."""
    try:
        from androguard.misc import AnalyzeAPK
    except ImportError:
        raise RuntimeError("Для разбора APK установите androguard: pip install androguard") from None
    a, dexes, _dx = AnalyzeAPK(path)
    tokens = set()
    if not isinstance(dexes, (list, tuple)):
        dexes = [dexes]
    for dex in dexes:
        for cls in dex.get_classes():
            name = str(cls.get_name())
            if name.startswith("L") and name.endswith(";"):
                name = name[1:-1]
            tokens.add(name.replace("/", "."))
    perms = []
    try:
        perms = sorted(set(a.get_permissions()))
    except Exception:
        pass
    return tokens, set(), perms
