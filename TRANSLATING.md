# Translating IsaClient

IsaClient is a client for the game Terraria (1.4.5): a panel of features and cheats, a music and video player, chat
tools, bots, building tools, an AI assistant. Players see these texts in menus, buttons, tooltips and chat messages.

Each language is a JSON file: every English text (the key, **copied exactly**) mapped to its translation.
`source/context.json` says where each text is shown, what kind of text it is, and gives a note when needed.

## Must keep exactly

- `{0}`, `{1}`... are filled in by the game (a name, a number, another text). Keep every one of them; you may move
  them where the sentence needs them. `{{` and `}}` are literal braces: keep them as they are.
- Commands start with a dot: `.video`, `.sendpic`, `.help`... Never translate or change them. In usage texts, the
  arguments a command takes are typed in English too: keep `<name|link>`, `[on|off]`, `pause | resume`, `<seconds>`
  and the like unchanged (translate only the sentences around them).
- Chat tags: `[c/RRGGBB:text]` (translate only the text after the colon), `[i:123]`, `[i/s5:123]`, `[isalink/...:...]`.
- Line breaks (`\n`): the same number, where the sentence breaks.
- Spaces at the start or end of a text (they join it to other text): keep them.
- Names: IsaClient, TerraAngel, zMod, ZazaMod, Terraria, TShock, Imgur, YouTube, yt-dlp, Groq, Discord, Steam, ImGui,
  Harmony, Windows, Media Foundation, UUID, IP, VPN, GIF, MP4, PNG, JSON, FPS, HP, NPC (use the usual word for NPC in
  your language if Terraria uses one). Keyboard keys: Ctrl, Shift, Alt, Enter, Esc, Tab, Insert, F1-F12, Ctrl+V.
- Short values that are words ("on", "off", "Enabled", "Disabled") are translated: they are shown alone or inside
  other texts ("Noclip {0}" is filled with "Enabled" or "Disabled").

## How it should read

- Use the names the official Terraria translation uses in your language for items, biomes, bosses, NPCs, events,
  game modes (Journey Mode, Expert...), buffs, and UI words (inventory, hotbar, map, chest...).
- Natural, short, friendly; like a well made game UI. Buttons stay short (similar length to English when possible).
  Tooltips and descriptions are full sentences. Keep the tone (informal "you" where the language allows: tú, ты, du,
  tu, você).
- A text that is cut in the middle ("Playing: {0}", " (original)", "Loop: {0}") is part of a bigger line: translate it
  so that it reads well once filled in.
- Do not add or drop information, emojis or punctuation that changes meaning. Keep "..." where English has it.
- Text that is not language (a code, a symbol, a format like `0:00`) stays as it is.


## Words with an area: `tetris::Hold`

Some English words mean different things in different parts of IsaClient ("Hold" is the Tetris box with the piece you
keep, and also an auto clicker mode). Those get a key with the area in front: `tetris::Hold`, `autoclick::Hold`.
Translate only the word, never the `area::` part: `"tetris::Hold": "Reserva"`. Until one is translated, the plain
word's translation is used. If a word doesn't fit everywhere it is shown (its note says "Shown in N places"), tell the
IsaClient team: it gets areas of its own.

## Terraria's names

`glossary/<code>.json` has the official name, in your language, of every item, NPC, boss, buff, biome and event
IsaClient mentions. Use exactly those (inside sentences too).

## When done

Run `python tools/check.py packs/<code>.json` (or `python tools/check.py <the file you were given> <your file>`) and
fix every problem it lists until it prints OK.
