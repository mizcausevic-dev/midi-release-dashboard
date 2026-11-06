# MIDI Release Control

A snapshot of the MIDI packs published in this session, with links to each repository and Pages site and a prioritized review queue. The figures are a dated snapshot, not live monitoring. A built Pages state and HTTP response are technical observations, not listening review or commercial clearance.

## Source and build

The reviewed rows are in `src/data.json`; the dashboard is in `src/content/dashboard/`. This legacy dashboard uses the Data app's source compiler and its locally installed, locked dependencies. The prebuilt compiler in the installed Data plugin currently fails on Windows because it rejects a backslash-delimited source path; the source compiler verifies the protected runtime and builds the same dashboard without changing that plugin.

```powershell
powershell -NoProfile -File tools/build-dashboard.ps1 -Node '<absolute-path-to-supported-node.exe>'
```

The wrapper requires the compatible dependencies already installed, Python, and the specified installed Data plugin; `-DataPlugin` can override its default path. It does not install packages or modify the protected runtime. The deployment consists of `dist/index.html` and `dist/artwork/`. Copy both to the existing `gh-pages` branch. The source build is tied to the installed Data plugin; the deployed site does not require it. The 33 dashboard-specific WebP covers in `src/content/assets/pack-art/` were individually AI-generated for the corresponding pack and optimized for web delivery. They are dashboard artwork and do not replace the original covers in the individual release repositories. Update the snapshot only after checking actual remote results. Roll back by pushing a reviewed previous artifact as a normal commit and verify the Pages URL.

## Known limitations

The dashboard reports observations captured on November 6, 2026. The bounded comparison found no exact or pitch-normalized cross-pack match groups in the principal melody parts and focused clips it compared. It found 78 pitch-normalized groups within individual packs, including potentially related clips, for contextual review. All 200 captioned motion previews were checked during the release run; each is a simple-synth excerpt, not a master. MIDI validation does not assess musical merit, genre representation, listening quality, or rights clearance. Filter and layout verification depends on browser access.
