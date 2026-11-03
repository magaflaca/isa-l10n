# IsaClient languages

The translations of [IsaClient](https://client.hacks.win), the Terraria 1.4.5 client. IsaClient doesn't carry them:
it reads this repository, lists every language with how much of it is translated, and downloads a language the
first time you use it (the one you pick in the language window, or the game's own). Downloaded languages update by
themselves when this repository changes, and keep working without internet.

<!-- languages:start -->
| | Language | Translated | Texts | Updated |
|---|---|---|---:|---|
| 🇨🇳 | [简体中文 (Chinese (Simplified))](packs/zh-Hans.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |
| 🇫🇷 | [Français (French)](packs/fr.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |
| 🇩🇪 | [Deutsch (German)](packs/de.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |
| 🇯🇵 | [日本語 (Japanese)](packs/ja.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |
| 🇧🇷 | [Português (Brasil) (Portuguese (Brazil))](packs/pt-BR.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |
| 🇷🇺 | [Русский (Russian)](packs/ru.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |
| 🇪🇸 | [Español (Spanish)](packs/es.json) | ![99%](https://img.shields.io/badge/-99%25-brightgreen?style=flat-square) | 7488 / 7513 | 2026-11-03 |

_7513 texts in the newest IsaClient. This table and `index.json` are rebuilt automatically on every change._
<!-- languages:end -->

## Help translate

Every language is one file in [`packs/`](packs). Each English text (the key, copied exactly) maps to its translation;
a missing text shows in English until someone translates it.

1. Read [TRANSLATING.md](TRANSLATING.md): what must stay as it is (`{0}`, `.commands`, `[c/FF0000:tags]`...) and how
   it should read.
2. Look a text up in [`source/context.json`](source/context.json): where it is shown, what kind of text it is
   (button, tooltip, chat message...) and a note when a word means something special there.
3. Use Terraria's own names for items, bosses, NPCs, biomes and events: [`glossary/`](glossary) has the official ones in
   every language, taken from the game.
4. Check your file: `python tools/check.py packs/<code>.json`.
5. Open a pull request (or send the file to the IsaClient team). The checks run on every pull request; once merged,
   players get it within minutes.

A new language: copy [`source/en.json`](source/en.json) to `packs/<code>.json`, set `Code` (like `it` or `pl`),
`Name` (in that language), `EnglishName` and `Flag` (a country code like `it`), and translate the values.

## What is here

| | |
|---|---|
| [`index.json`](index.json) | What IsaClient reads first: every language, how many texts it has, size and SHA-256 (downloads are checked against it). Rebuilt automatically. |
| [`packs/`](packs) | One file per language. |
| [`source/en.json`](source/en.json) | Every text of the newest IsaClient (the keys). |
| [`source/context.json`](source/context.json) | Where each text is shown, what kind of text it is, and notes. |
| [`glossary/`](glossary) | Terraria's official names used by IsaClient, in each language. |
| [`tools/`](tools) | `check.py` (checks a file) and `build_index.py` (rebuilds `index.json` and the table above). |

The English texts come from IsaClient's code: when IsaClient changes, `source/` changes with it, and texts that no
longer exist leave the packs.
