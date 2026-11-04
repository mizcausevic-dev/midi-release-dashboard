# MIDI Release Control

A snapshot of the MIDI packs published in this session, with links to each repository and Pages site and a prioritized review queue. The figures are a dated snapshot, not live monitoring. A built Pages state and HTTP response are technical observations, not listening review or commercial clearance.

## Source and build

The reviewed rows are in `src/data.json`; the dashboard is in `src/content/dashboard/`. The installed Data app prebuilt compiler fails on this Windows installation because its source manifest includes a backslash-delimited path. The verified source build works with Node and the locked dependencies:

```powershell
npm ci --ignore-scripts
node <data-plugin>/output_formats/html/scripts/data-app.mjs build --project-dir <dashboard-project> --source
python tools/stage-artwork.py
```

The deployment consists of `dist/index.html` and `dist/artwork/`. Copy both to the existing `gh-pages` branch. The source build is tied to the installed Data plugin; the deployed site does not require it. The 33 dashboard-specific WebP covers in `src/content/assets/pack-art/` were individually AI-generated for the corresponding pack and optimized for web delivery. They are dashboard artwork and do not replace the original covers in the individual release repositories. Update the snapshot only after checking actual remote results. Roll back by pushing a reviewed previous artifact as a normal commit and verify the Pages URL.

## Known limitations

The dashboard reports observations captured on November 4, 2026. MIDI file validation does not assess musical merit, genre representation, listening quality, or rights clearance. Filter and layout verification depends on browser access.
