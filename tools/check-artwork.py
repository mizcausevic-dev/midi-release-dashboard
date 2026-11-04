"""Check recorded artwork URLs without following or changing repository state."""
import concurrent.futures
import json
import urllib.request
from pathlib import Path

data = json.loads((Path(__file__).resolve().parents[1] / "src" / "data.json").read_text(encoding="utf-8"))
def check(row):
    try:
        req = urllib.request.Request(row["artwork"], method="HEAD", headers={"User-Agent": "MIDI-dashboard-check/1.0"})
        with urllib.request.urlopen(req, timeout=20) as response:
            return row["slug"], response.status, response.headers.get("Content-Type")
    except Exception as exc:
        return row["slug"], "ERROR", str(exc)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(check, data["queries"]["releases"]["rows"]))
for slug, status, detail in results:
    if status != 200 or not (detail or "").startswith("image/"):
        print(slug, status, detail)
print(f"Artwork: {sum(x[1] == 200 and (x[2] or '').startswith('image/') for x in results)}/{len(results)} image responses")
raise SystemExit(any(x[1] != 200 or not (x[2] or "").startswith("image/") for x in results))
