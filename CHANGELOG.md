# Changelog

## [3.1.0] SERVER - unreleased

- The building commands (/spawn, /placeBlockEntity, /placeKeypad, /placeKeycardReader, /spawnNPC and /pregen) now need operator permission. Before, any player on a server could use them to spawn items and mobs. Buildings still run them as before.
- Fixed the bandit, police and survivor NPCs not spawning in buildings on Linux servers.
- Fixed the detonator never appearing in throwables loot.
- Mobs no longer regain full health when their chunk reloads.
- Updated Infectious Patch to 1.0.3, so zombies placed by buildings, spawners and commands stay in lit places.
- Removed runtime files the 3.0.1 pack shipped by mistake: a cancelled chunk pre-generation task, caches and per-install files.
- Better Compatibility Checker now names the pack Apocalypse Begins [BETA].
- The server list now shows the pack name and version.
- Pinned the server starter jar to 0.1.35, so a new upstream release can't change the server without warning.

## [3.1.0] CLIENT - unreleased

- Fixed the detonator never appearing in throwables loot, and mobs regaining full health when their chunk reloads.
- The building commands now need operator permission.
- Updated Infectious Patch to 1.0.3, so zombies placed by buildings, spawners and commands stay in lit places.
- Added Shaders Companion 0.9.3, which comes with ABZA Shader and lets it show what's off screen in water and glass reflections.
- Removed the custom BSL settings, so every shader starts from its own defaults. No shader is on by default.
- Turned off the Distant Horizons memory warnings and the Oculus update message.
- Reworded the vaccine tooltip.
- Removed runtime files the 3.0.1 pack shipped by mistake.
- The modpack manifest and Better Compatibility Checker now name the pack Apocalypse Begins [BETA].

## [3.0.1] - 2026-07-13

- The last release before this repository. CLIENT/ and SERVER/ in the first commit are the published files.
