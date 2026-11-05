param(
  [string]$Node = 'node',
  [string]$DataPlugin = (Join-Path $env:USERPROFILE '.codex\plugins\cache\openai-curated-remote\data-analytics\1.1.1-exp-pages.2')
)
$ErrorActionPreference = 'Stop'
$project = Split-Path -Parent $PSScriptRoot
$compiler = Join-Path $DataPlugin 'output_formats\html\scripts\data-app.mjs'
if (-not (Test-Path -LiteralPath $compiler -PathType Leaf)) { throw "Data compiler not found: $compiler" }
& $Node $compiler build --project-dir $project --source
if ($LASTEXITCODE -ne 0) { throw "Dashboard source build failed with exit code $LASTEXITCODE" }
& python (Join-Path $PSScriptRoot 'stage-artwork.py')
if ($LASTEXITCODE -ne 0) { throw "Dashboard artwork staging failed with exit code $LASTEXITCODE" }
Write-Host "Dashboard ready: $(Join-Path $project 'dist\index.html')"
