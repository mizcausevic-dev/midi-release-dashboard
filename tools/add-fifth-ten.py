"""Add the fifth batch after verified remote, MIDI, and clip evidence."""
import json
from datetime import datetime, timezone
from pathlib import Path

project = Path(__file__).resolve().parents[1]
base = project.parent / "midi-release-train" / "fifth-ten-releases"
proofs = {r["slug"]:r for r in json.loads((base/"remote-evidence.json").read_text(encoding="utf-8"))["rows"]}
packs = [
    ("hip-hop-chord-melody-sketches","Hip-Hop Chord & Melody Sketches",88),
    ("ambientcore-textures","Ambientcore Textures",70),
    ("soulful-house-chords","Soulful House Chords",122),
    ("piano-house-hooks","Piano House Hooks",126),
    ("garage-house-grooves","Garage House Grooves",126),
    ("melodic-techno-sequences","Melodic Techno Sequences",124),
    ("dark-techno-melodies","Dark Techno Melodies",132),
    ("uplifting-trance-leads","Uplifting Trance Leads",140),
    ("afrobeats-inspired-melodies","Afrobeats-Inspired Melodies",104),
    ("trap-melody-toolkit","Trap Melody Toolkit",140),
]
path = project/"src"/"data.json"
data = json.loads(path.read_text(encoding="utf-8"))
rows = data["queries"]["releases"]["rows"]
rows[:] = [r for r in rows if r["slug"] not in {p[0] for p in packs}]
new = []
for order,(slug,name,bpm) in enumerate(packs,65):
    proof = proofs[slug]
    report = json.loads((base/slug/"checks"/"validation-report.json").read_text(encoding="utf-8"))
    clips = json.loads((base/slug/"checks"/"clip-validation.json").read_text(encoding="utf-8"))
    if not (proof.get("local")==proof.get("remote")==proof.get("tag_commit") and proof.get("tag")=="refs/tags/v1.0.0" and proof.get("pages")=="built" and proof.get("http")==200 and proof.get("art_http")==200 and report["status"]=="PASS" and clips["status"]=="PASS"):
        raise ValueError(f"Incomplete evidence for {slug}")
    page = f"https://mizcausevic-dev.github.io/{slug}/"
    new.append({"order":order,"name":name,"slug":slug,"category":"New batch 5","bpm":bpm,"midiFiles":28+clips["files_checked"],"studies":4,"tag":"v1.0.0","repository":f"https://github.com/mizcausevic-dev/{slug}","page":page,"pagesStatus":"built","httpStatus":200,"validation":"PASS","artwork":page+"art/hero.jpg"})
rows[:0] = new
data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
actions = data["queries"]["next_actions"]["rows"]
actions[0]["evidence"] = "A local audit found 11 of the earlier 44 releases contained both a JPG hero and an MP4. The 30 later releases also contain both, leaving 33 earlier packs without this media pair."
actions[1]["scope"] = "All 74 packs"
actions[2]["scope"] = "All 74 public releases"
actions[3]["scope"] = "74 Pages sites"
source = data["queries"]["releases"].get("source",{})
for metric in source.get("metricDefinitions",[]):
    if metric.get("label") == "Published release":
        metric["definition"] = "One of the 74 session repositories with verified public GitHub source and Pages."
    if metric.get("label") == "Validated MIDI exports":
        metric["definition"] = "Sum of recorded MIDI exports, including validated focused clips in batches four and five."
for item in source.get("evidenceFlow",[]):
    if "GitHub Pages API state was observed as built" in item.get("detail",""):
        item["detail"] = "GitHub Pages API state was observed as built for all 74 releases during their respective release checks."
path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8",newline="\n")
