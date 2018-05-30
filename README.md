## description
My complex_modifications settings for Karabiner-Elements.

Karabiner-Elements settings must be formatted in JSON,
but writing complex settings in JSON is too difficult to human.
So I decided to write my settings in YAML, then convert them to JSON format.

## setup (require Python 3.6+)

```
pip install -r requirements.txt
```

## install settings

```
python install.py complex_modifications/*.yml
```

Command above does:
1. Read setting files in `complex_modifications` and convert to JSON.
2. Embed converted complex_modifications settings to Karabiner-Elements setting file: `~/.config/karabiner/karabiner.json`.

Karabiner-Elements dynamically reloads `~/.config/karabiner/karabiner.json` file when it is modified.

## reference
- Karabiner-Elements setting docs
  https://pqrs.org/osx/karabiner/json.html
