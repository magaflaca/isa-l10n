"""Checks IsaClient translations: what the game fills in, commands, chat tags, line breaks and spaces must survive.

    python tools/check.py packs/es.json                 a language pack (against source/en.json)
    python tools/check.py <chunk.json> <translated.json> a translated chunk against the chunk it came from

Prints every problem; exit code 0 when there is none.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLACEHOLDER = re.compile(r"(?<!\{)\{(\d+)\}(?!\})")
COMMAND = re.compile(r"(?<![\w/.:])\.[a-z][a-z0-9]+\b")
TAG = re.compile(r"\[(c|i|g|a|n|isalink)(/[^:\]]*)?:")
CONTEXT = re.compile(r"^[a-z]{2,20}::(?=\S)")


def placeholders(text):
    return sorted(PLACEHOLDER.findall(text.replace("{{", "").replace("}}", "")))


def problems(key, value):
    """Problems of one translation (empty list when it is fine). Keys like "tetris::Hold" are checked by the text."""
    out = []
    if not isinstance(value, str):
        return ["not a text"]
    if not value.strip():
        return []
    text = CONTEXT.sub("", key)
    if CONTEXT.match(value):
        out.append("the area mark (\"" + key.split("::")[0] + "::\") is not part of the translation")
    if placeholders(text) != placeholders(value):
        out.append("{0}, {1}... differ (keep every one: " + ", ".join("{" + p + "}" for p in placeholders(text)) + ")")
    if text.count("{{") != value.count("{{") or text.count("}}") != value.count("}}"):
        out.append("literal braces {{ }} differ")
    if text.count("\n") != value.count("\n"):
        out.append("line breaks differ (%d in English, %d here)" % (text.count("\n"), value.count("\n")))
    for command in sorted(set(COMMAND.findall(text))):
        if command not in value:
            out.append("command " + command + " changed")
    if sorted(m.group(0) for m in TAG.finditer(text)) != sorted(m.group(0) for m in TAG.finditer(value)):
        out.append("chat tags [c/...:] [i:...] differ")
    if text != text.lstrip() and value == value.lstrip():
        out.append("the space at the start was lost")
    if text != text.rstrip() and value == value.rstrip():
        out.append("the space at the end was lost")
    return out


def load(path):
    with open(path, encoding="utf-8-sig") as f:
        return json.load(f)


def strings(data):
    return data["Strings"] if isinstance(data, dict) and isinstance(data.get("Strings"), dict) else data


def check(source_keys, translated, label):
    found = []
    for key, value in translated.items():
        if key not in source_keys:
            found.append("unknown text (keys are copied exactly from English): " + json.dumps(key, ensure_ascii=False))
            continue
        for problem in problems(key, value):
            found.append(problem + ": " + json.dumps(key, ensure_ascii=False) + " -> " + json.dumps(value, ensure_ascii=False))
    for line in found:
        print(label + ": " + line)
    return found


def main():
    if len(sys.argv) == 2:
        source = strings(load(os.path.join(ROOT, "source", "en.json")))
        pack = load(sys.argv[1])
        for field in ("Code", "Name", "EnglishName", "Flag", "Strings"):
            if field not in pack:
                print("missing \"%s\"" % field)
                return 1
        found = check(set(source), strings(pack), os.path.basename(sys.argv[1]))
        done = sum(1 for k in source if strings(pack).get(k))
        print(("OK" if not found else "%d problems" % len(found)) + " (%d of %d texts translated)" % (done, len(source)))
        return 0 if not found else 1
    if len(sys.argv) == 3:
        source = strings(load(sys.argv[1]))
        found = check(set(source), strings(load(sys.argv[2])), os.path.basename(sys.argv[2]))
        print(("OK" if not found else "%d problems" % len(found)) + " (%d texts)" % len(source))
        return 0 if not found else 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
