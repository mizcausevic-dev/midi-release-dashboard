"""Add the fourth batch after verifying source, tags, Pages, media, and clips."""
import json
from datetime import datetime, timezone
from pathlib import Path

project = Path(__file__).resolve().parents[1]
base = project.parent / "midi-release-train" / "fourth-ten-releases"
evidence = json.loads((base / "remote-evidence.json").read_text(encoding="utf-8"))
packs = [
    ("dark-edm-chord-vault", "Dark EDM Chord Vault", 128),
    ("nineties-trance-chords-melodies", "90s Trance Chords & Melodies", 138),
    ("bass-house-hooks", "Bass House Hooks", 126),
    ("tech-house-groove-builder", "Tech House Groove Builder", 126),
    ("melodic-house-chord-journeys", "Melodic House Chord Journeys", 122),
    ("house-techno-crossover", "House / Techno Crossover", 128),
    ("hardstyle-anthem-toolkit", "Hardstyle Anthem Toolkit", 150),
    ("disco-funk-chords", "Disco & Funk Chords", 112),
    ("progressive-rock-writing-kit", "Progressive Rock Writing Kit", 108),
    ("afro-house-inspired-melodies", "Afro House-Inspired Melodies", 120),
]
proofs = {row["slug"]: row for row in evidence["rows"]}
path = project / "src" / "data.json"
data = json.loads(path.read_text(encoding="utf-8"))
rows = data["queries"]["releases"]["rows"]
rows[:] = [row for row in rows if row["slug"] not in {pack[0] for pack in packs}]
new = []
for index, (slug, name, bpm) in enumerate(packs, 55):
    proof = proofs[slug]
    report = json.loads((base / slug / "checks" / "validation-report.json").read_text(encoding="utf-8"))
    clips = json.loads((base / slug / "checks" / "clip-validation.json").read_text(encoding="utf-8"))
    if not (proof.get("local")==proof.get("remote")==proof.get("tag_commit") and proof.get("tag")=="refs/tags/v1.0.0" and proof.get("pages")=="built" and proof.get("http")==200 and proof.get("art_http")==200 and report["status"]=="PASS" and clips["status"]=="PASS"):
        raise ValueError(f"Incomplete evidence for {slug}")
    page = f"https://mizcausevic-dev.github.io/{slug}/"
    new.append({"order":index,"name":name,"slug":slug,"category":"New batch 4","bpm":bpm,"midiFiles":28+clips["files_checked"],"studies":4,"tag":"v1.0.0","repository":f"https://github.com/mizcausevic-dev/{slug}","page":page,"pagesStatus":"built","httpStatus":200,"validation":"PASS","artwork":page+"art/hero.jpg"})
rows[:0] = new
data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
actions = data["queries"]["next_actions"]["rows"]
actions[0]["evidence"] = "A local audit found 11 of the earlier 44 releases contained both a JPG hero and an MP4. The 20 later releases also contain both, leaving 33 earlier packs without this media pair."
actions[1]["scope"] = "All 64 packs"
actions[2]["scope"] = "All 64 public releases"
actions[3]["scope"] = "64 Pages sites"
source = data["queries"]["releases"].get("source", {})
for metric in source.get("metricDefinitions", []):
    if metric.get("label") == "Published release":
        metric["definition"] = "One of the 64 session repositories with verified public GitHub source and Pages."
    if metric.get("label") == "Validated MIDI exports":
        metric["definition"] = "Sum of recorded MIDI exports, including validated focused clips in the fourth batch."
for item in source.get("evidenceFlow", []):
    if "GitHub Pages API state was observed as built" in item.get("detail", ""):
        item["detail"] = "GitHub Pages API state was observed as built for all 64 releases during their respective release checks."
path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")
