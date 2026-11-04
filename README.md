# MIDI Release Control

A snapshot of the MIDI packs published in this session, with links to each repository and Pages site and a prioritized review queue. The figures are a dated snapshot, not live monitoring. A built Pages state and HTTP response are technical observations, not listening review or commercial clearance.

## Source and build

The reviewed rows are in `src/data.json`; the dashboard is in `src/content/dashboard/`. The installed Data app prebuilt compiler fails on this Windows installation because its source manifest includes a backslash-delimited path. The verified source build works with Node and the locked dependencies:

```powershell
npm ci --ignore-scripts
node <data-plugin>/output_formats/html/scripts/data-app.mjs build --project-dir <dashboard-project> --source
```

The generated `dist/index.html` is the static deployment artifact. The source build is tied to the installed Data plugin; the deployed HTML does not require it. Update the snapshot only after checking actual remote results. The `gh-pages` branch holds the deployed artifact; roll back by pushing a reviewed previous artifact as a normal commit and verify the Pages URL.

## Known limitations

The dashboard reports observations captured on November 4, 2026. MIDI file validation does not assess musical merit, genre representation, listening quality, or rights clearance. Filter and layout verification depends on browser access.
