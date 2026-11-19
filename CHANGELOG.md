# Changelog

## [3.1.0] SERVER - unreleased

- Needs a new world. Worlds from 3.0.1 aren't supported.
- The building commands (/spawn, /placeBlockEntity, /placeKeypad, /placeKeycardReader, /spawnNPC and /pregen) now need operator permission. Before, any player on a server could use them to spawn items and mobs. Buildings still run them as before.
- Fixed the bandit, police and survivor NPCs not spawning in buildings on Linux servers.
- Fixed the detonator never appearing in throwables loot.
- Mobs no longer regain full health when their chunk reloads.
- The anvil no longer puts an enchantment on gear it can't go on, or next to an enchantment it conflicts with, and combining two equal books stops at the enchantment's maximum level.
- Lowered the Undead Revamp 2 Bomber's explosion damage from 1000 to 12.
- Lost Cities no longer builds stairs between streets on different levels.
- Added Scalpel. The hidden item list moved from JEITweaker to Scalpel, and Scalpel now cuts the items Item Obliterator used to block, so they no longer drop, craft or work.
- Removed JEITweaker, Item Obliterator and Item Obliterator Despawn Fix, which Scalpel replaces.
- Removed The Flesh That Hates, Prion Infection and Entomophobia, which 3.0.1 shipped turned off.
- Updated Superb Warfare to 0.8.9.2 and added [SBW] Performance Fix, for better FPS around mob crowds.
- Updated Infectious Patch to 1.0.3, so zombies placed by buildings, spawners and commands stay in lit places.
- Removed runtime files the 3.0.1 pack shipped by mistake: a cancelled chunk pre-generation task, caches and per-install files.
- Better Compatibility Checker now names the pack Apocalypse Begins [BETA].
- The server list now shows the pack name and version.
- Pinned the server starter jar to 0.1.35, so a new upstream release can't change the server without warning.

## [3.1.0] CLIENT - unreleased

- Needs a new world. Worlds from 3.0.1 aren't supported.
- Fixed the detonator never appearing in throwables loot, and mobs regaining full health when their chunk reloads.
- The anvil no longer puts an enchantment on gear it can't go on, or next to an enchantment it conflicts with, and combining two equal books stops at the enchantment's maximum level.
- Lowered the Undead Revamp 2 Bomber's explosion damage from 1000 to 12.
- Lost Cities no longer builds stairs between streets on different levels.
- The building commands now need operator permission.
- Added Scalpel, which replaces JEITweaker, Item Obliterator and Item Obliterator Despawn Fix.
- Removed The Flesh That Hates, Prion Infection and Entomophobia, which 3.0.1 shipped turned off.
- Updated Superb Warfare to 0.8.9.2 and added [SBW] Performance Fix.
- Updated Infectious Patch to 1.0.3.
- Added Shaders Companion 0.9.3, which comes with ABZA Shader and lets it show what's off screen in water and glass reflections.
- Removed the custom BSL settings, so every shader starts from its own defaults. No shader is on by default.
- The title and loading screens show the version without "PRE-ALPHA | 10% Complete".
- Turned off the Distant Horizons memory warnings and the Oculus update message.
- Reworded the vaccine tooltip.
- Removed runtime files the 3.0.1 pack shipped by mistake.
- The modpack manifest and Better Compatibility Checker now name the pack Apocalypse Begins [BETA].

## [3.0.1] - 2026-07-13

- The last release before this repository. CLIENT/ and SERVER/ in the first commit are the published files.
