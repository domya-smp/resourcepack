# DomSMP resource pack

[Download domsmp.zip](https://github.com/domya-smp/resourcepack/releases/latest/download/domsmp.zip)
— requires access to this private repository.

## Build

```sh
python3 scripts/build.py
```

Requires Python 3.10+. Output: `dist/domsmp.zip`.

## Release

**Actions → Build and release domsmp → Run workflow**, branch `main`.
Pushes and pull requests only build the `domsmp` artifact.

## Off-season TAB header

The `domsmp:off_season` bitmap font contains the original «МЕЖСЕЗОНЬЕ» title,
with a sage, chalk and dusty rose gradient. Its two adjacent glyphs are U+E110
and U+E111. The standard Minecraft fonts are unchanged.

In a double-quoted YAML header line, use:

```yaml
- "<white><font:domsmp:off_season>\uE110\uE111</font></white>"
```

Reserve two empty header lines above the title, then one empty line before
the online count. The bitmap renders at 22 GUI pixels high, with an ascent of 20.
Players must enable this pack on their client before the title can render.

To regenerate the lettering, install Pillow and run
`python3 scripts/generate_off_season_title.py`, then rebuild the pack normally.
The optional `dist/off-season-preview.png` previews the lettering; it is not
an in-game screenshot and is not included in the ZIP.
