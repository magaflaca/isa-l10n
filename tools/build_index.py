"""Builds index.json (what IsaClient downloads first) and the language table of README.md from the packs.

    python tools/build_index.py           write index.json and README.md
    python tools/build_index.py --check   only check the packs (exit 1 on any problem): for pull requests

For each pack in packs/: how many of the texts of the newest IsaClient (source/en.json) it translates, its size and
SHA-256 (IsaClient checks every download against it). A language keeps its "updated" date until its file changes.
"""
import datetime
import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS = os.path.join(ROOT, "packs")
INDEX = os.path.join(ROOT, "index.json")
README = os.path.join(ROOT, "README.md")
REPO = "magaflaca/isa-l10n"

# Country flags as emoji for the README table (the pack's "Flag").
def flag_emoji(code):
    code = (code or "").upper()
    special = {"UK": "GB", "CN": "CN", "BR": "BR", "US": "US"}
    code = special.get(code, code)
    if len(code) != 2 or not code.isalpha():
        return "🏳️"
    return "".join(chr(0x1F1E6 + ord(c) - ord("A")) for c in code)


def badge(percent):
    color = "brightgreen" if percent >= 95 else "green" if percent >= 80 else "yellowgreen" if percent >= 60 else "yellow" if percent >= 40 else "orange" if percent >= 20 else "red"
    return "![%d%%](https://img.shields.io/badge/-%d%%25-%s?style=flat-square)" % (percent, percent, color)


def main():
    only_check = "--check" in sys.argv
    source = check.strings(check.load(os.path.join(ROOT, "source", "en.json")))
    keys = list(source)
    previous = {}
    if os.path.exists(INDEX):
        try:
            previous = {e["code"]: e for e in check.load(INDEX).get("languages", [])}
        except Exception:
            previous = {}
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    languages = []
    total_problems = 0
    for name in sorted(os.listdir(PACKS)):
        if not name.endswith(".json"):
            continue
        path = os.path.join(PACKS, name)
        raw = open(path, "rb").read()
        # Served as committed (LF): hashed the same way, so IsaClient's check of the download matches.
        if b"
" in raw or raw.startswith(b"ï»¿"):
            raw = raw.replace(b"
", b"
")
            if raw.startswith(b"ï»¿"):
                raw = raw[3:]
            with open(path, "wb") as f:
                f.write(raw)
        try:
            pack = json.loads(raw.decode("utf-8-sig"))
        except ValueError as e:
            print("%s: not valid JSON: %s" % (name, e))
            total_problems += 1
            continue
        missing = [f for f in ("Code", "Name", "EnglishName", "Flag", "Strings") if f not in pack]
        if missing:
            print("%s: missing %s" % (name, ", ".join(missing)))
            total_problems += 1
            continue
        if pack["Code"] + ".json" != name:
            print("%s: \"Code\" is %s, the file must be named %s.json" % (name, pack["Code"], pack["Code"]))
            total_problems += 1
        strings = pack["Strings"]
        found = check.check(set(keys), strings, name)
        total_problems += len(found)
        translated = sum(1 for k in keys if strings.get(k))
        sha = hashlib.sha256(raw).hexdigest()
        old = previous.get(pack["Code"], {})
        languages.append({
            "code": pack["Code"],
            "name": pack["Name"],
            "englishName": pack["EnglishName"],
            "flag": pack["Flag"],
            "author": pack.get("Author", ""),
            "file": "packs/" + name,
            "sha256": sha,
            "bytes": len(raw),
            "translated": translated,
            "total": len(keys),
            "percent": round(100.0 * translated / len(keys), 1) if keys else 0,
            "updated": old.get("updated") if old.get("sha256") == sha and old.get("updated") else now,
        })
        print("%-8s %5d of %d (%.1f%%)%s" % (pack["Code"], translated, len(keys), 100.0 * translated / max(1, len(keys)), "" if not found else "  %d problems" % len(found)))
    if only_check:
        print("OK" if not total_problems else "%d problems" % total_problems)
        return 0 if not total_problems else 1
    languages.sort(key=lambda e: (-e["percent"], e["englishName"]))
    index = {
        "format": 1,
        "updated": max([e["updated"] for e in languages] or [now]),
        "texts": len(keys),
        "languages": languages,
    }
    with open(INDEX, "w", encoding="utf-8", newline="\n") as f:
        json.dump(index, f, ensure_ascii=False, indent=1)
        f.write("\n")
    write_readme(languages, len(keys))
    print("index.json: %d languages, %d texts" % (len(languages), len(keys)))
    return 0


def write_readme(languages, texts):
    rows = ["| | Language | Translated | Texts | Updated |", "|---|---|---|---:|---|"]
    for e in languages:
        name = e["name"] if e["name"] == e["englishName"] else "%s (%s)" % (e["name"], e["englishName"])
        rows.append("| %s | [%s](packs/%s.json) | %s | %d / %d | %s |" % (flag_emoji(e["flag"]), name, e["code"], badge(int(e["percent"])), e["translated"], e["total"], e["updated"][:10]))
    table = "<!-- languages:start -->\n" + "\n".join(rows) + "\n\n_%d texts in the newest IsaClient. This table and `index.json` are rebuilt automatically on every change._\n<!-- languages:end -->" % texts
    text = open(README, encoding="utf-8").read() if os.path.exists(README) else ""
    if "<!-- languages:start -->" in text:
        text = re.sub(r"<!-- languages:start -->.*?<!-- languages:end -->", lambda m: table, text, flags=re.S)
    else:
        text += "\n" + table + "\n"
    with open(README, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


if __name__ == "__main__":
    sys.exit(main())
