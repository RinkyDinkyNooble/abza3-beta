#!/usr/bin/env python3
"""Sets the modpack version everywhere it appears.

Changes CLIENT/manifest.json, Better Compatibility Checker (client and server must match or players
can't join), the "Version" line on the FancyMenu title and loading screens, and the server list MOTD.
A config that exists on both sides is changed on both. CHANGELOG.md stays manual; check_release.py
checks everything afterwards.

Usage: python tools/set_version.py <version>
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SIDES = ["CLIENT/overrides", "SERVER"]

# Path, pattern whose second group is the version
ROOT_PLACES = [
    ("CLIENT/manifest.json", r'^(  "version": ")([^"]+)(")'),
    ("SERVER/server.properties", r"^(motd=.*v)(\d+(?:\.\d+)*)()"),
]
# Paths under CLIENT/overrides and SERVER; the client copy is required, the server copy is optional
SHARED_PLACES = [
    ("config/bcc-common.toml", r'^(\tmodpackVersion = ")([^"]+)(")'),
    ("config/fancymenu/customization/title_screen_layout.txt", r"^(  source = Version )(\S+)()"),
    ("config/fancymenu/customization/drippy_loading_overlay_layout.txt", r"^(  source = Version )(\S+)()"),
]


def places():
    out = list(ROOT_PLACES)
    for rel, pattern in SHARED_PLACES:
        for side in SIDES:
            path = side + "/" + rel
            if side == SIDES[0] or os.path.isfile(os.path.join(ROOT, path)):
                out.append((path, pattern))
    return out


def main():
    if len(sys.argv) != 2 or not re.fullmatch(r"\d+(\.\d+)*", sys.argv[1]):
        sys.exit("Usage: python tools/set_version.py <version>, digits and dots only")
    version = sys.argv[1]
    todo = []
    for path, pattern in places():
        full = os.path.join(ROOT, path)
        text = open(full, "rb").read().decode("utf-8")
        found = re.findall(pattern, text, re.M)
        if len(found) != 1:
            sys.exit(f"{path}: expected 1 version line, found {len(found)}; nothing was changed")
        todo.append((path, full, text, pattern, found[0][1]))
    for path, full, text, pattern, old in todo:
        text = re.sub(pattern, lambda m: m.group(1) + version + m.group(3), text, flags=re.M)
        open(full, "wb").write(text.encode("utf-8"))
        print(f"{path}: {old} -> {version}")


if __name__ == "__main__":
    main()
