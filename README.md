# Apocalypse Begins [BETA]

The 3.x line of [Apocalypse Begins](https://www.curseforge.com/minecraft/modpacks/apocalypse-begins-zombie-apocalypse), a zombie apocalypse survival modpack for Minecraft 1.20.1 and Forge 47.4.10. It no longer gets new content; releases here fix bugs and keep it running.

## Layout

| Folder | What it holds |
|---|---|
| `CLIENT/` | The CurseForge export: `manifest.json`, `modlist.html` and `overrides/` |
| `SERVER/` | The server pack. Its `mods/` come from CurseForge and stay out of git |
| `tools/` | `set_version.py`, `check_release.py` and `icon/make_icon.py` |

The first commit is the published 3.0.1, unchanged.

## Releasing

1. `python tools/set_version.py <version>` sets the version in the manifest, Better Compatibility Checker, the title and loading screens and the server MOTD, then draws the version into the profile image (`CLIENT/profileImage/`) and `SERVER/server-icon.png`.
2. Write the version's entry in `CHANGELOG.md`.
3. `python tools/check_release.py` checks that the version agrees everywhere, client and server configs match, and no runtime files or disabled jars ship.
