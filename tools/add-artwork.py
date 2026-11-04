"""Assign each recorded release its own published artwork URL."""
import json
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "src" / "data.json"
data = json.loads(path.read_text(encoding="utf-8"))
for row in data["queries"]["releases"]["rows"]:
    art = "hero.jpg" if row["slug"] == "footwork-codex" or row["category"] in ("New batch 2", "New batch 3") else "cover.svg"
    row["artwork"] = row["page"] + "art/" + art
path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
