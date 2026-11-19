#!/usr/bin/env python3
"""Checks the client and server packs are ready to release together.

- Every place that shows the version agrees with CLIENT/manifest.json, and CHANGELOG.md has an entry
  for it.
- The manifest lists no project twice and modlist.html names as many mods as the manifest.
- SERVER/server-icon.png is a 64x64 PNG, and a local profile image named by the manifest exists.
- Every config, script, KubeJS and CustomNPCs file that exists on both sides is identical, nothing
  exists only on the server, and Scalpel rules (if any) exist on both sides.
- No runtime files (caches, fingerprints, chunk tasks) ship, and SERVER/mods holds no .disabled jars.

Usage: python tools/check_release.py
"""
import json
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import set_version  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CLIENT = os.path.join(ROOT, "CLIENT")
SERVER = os.path.join(ROOT, "SERVER")
SHARED = ["config", "defaultconfigs", "kubejs", "scripts", "customnpcs"]
# Files the game writes at runtime; the CurseForge export picks them up from the instance
JUNK = [
    r"config/chunky/tasks/",
    r"config/embeddium-fingerprint\.json$",
    r"config/voicechat/username-cache\.json$",
    r"config/resourceful-config-web\.json$",
    r"config/mcreator_mem_fix\.json$",
    r"config/xaeropatreon\.txt$",
    r"\.bak$",
    r"\.log$",
]

problems = []


def read(path):
    return open(os.path.join(ROOT, path), "rb").read().decode("utf-8-sig")


def check_version():
    manifest = json.loads(read("CLIENT/manifest.json"))
    version = manifest["version"]
    for path, pattern in set_version.places():
        found = [m[1] for m in re.findall(pattern, read(path), re.M)]
        if found != [version]:
            problems.append(f"{path} shows {found or 'no version'}, manifest says {version}")
    if f"## [{version}]" not in read("CHANGELOG.md"):
        problems.append(f"CHANGELOG.md has no entry for {version}")
    return manifest


def check_manifest(manifest):
    ids = [f["projectID"] for f in manifest["files"]]
    for pid in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append(f"project {pid} is in the manifest more than once")
    names = re.findall(r"<li><a href=", read("CLIENT/modlist.html"))
    if len(names) != len(ids):
        problems.append(f"modlist.html names {len(names)} mods, the manifest lists {len(ids)}")


def check_icons(manifest):
    image = manifest.get("image", "")
    if image and not image.startswith("http") and not os.path.isfile(os.path.join(CLIENT, image)):
        problems.append(f"the manifest's profile image {image!r} is missing")
    head = open(os.path.join(SERVER, "server-icon.png"), "rb").read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n" or struct.unpack(">II", head[16:24]) != (64, 64):
        problems.append("SERVER/server-icon.png is not a 64x64 PNG")


def files_under(base):
    out = set()
    for d in SHARED:
        for dp, _, fn in os.walk(os.path.join(base, d)):
            out.update(os.path.relpath(os.path.join(dp, f), base).replace(os.sep, "/") for f in fn)
    return out


def check_sync():
    client_base = os.path.join(CLIENT, "overrides")
    client, server = files_under(client_base), files_under(SERVER)
    for f in sorted(client & server):
        if open(os.path.join(client_base, f), "rb").read() != open(os.path.join(SERVER, f), "rb").read():
            problems.append(f"{f} differs between client and server")
    for f in sorted(server - client):
        problems.append(f"{f} exists only on the server")
    for f in sorted(client - server):
        if f.startswith("config/scalpel/"):
            problems.append(f"{f} is missing on the server; Scalpel refuses joins when rules differ")
    for side, files in (("CLIENT/overrides", client), ("SERVER", server)):
        for f in sorted(files):
            if any(re.search(p, f) for p in JUNK):
                problems.append(f"{side}/{f} is a runtime file and shouldn't ship")
    return len(client - server)


def check_server_mods():
    mods = os.path.join(SERVER, "mods")
    if not os.path.isdir(mods):
        problems.append("SERVER/mods is missing")
        return
    for name in sorted(os.listdir(mods)):
        if name.endswith(".disabled"):
            problems.append(f"SERVER/mods/{name} is a disabled leftover")


def main():
    manifest = check_version()
    check_manifest(manifest)
    check_icons(manifest)
    client_only = check_sync()
    check_server_mods()
    if problems:
        print("Not ready:")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"Ready: version {manifest['version']} everywhere, client and server in sync "
          f"({client_only} client-only files), no runtime files or disabled jars.")


if __name__ == "__main__":
    main()
