"""Add releases only after remote and local evidence has been recorded."""
import json
from datetime import datetime, timezone
from pathlib import Path

project = Path(__file__).resolve().parents[1]
base = project.parent / "midi-release-train" / "third-ten-releases"
evidence = json.loads((base / "remote-evidence.json").read_text(encoding="utf-8"))
names = [
    ("neo-soul-keys","Neo-Soul Keys",84),
    ("melodic-trance-studies","Melodic Trance",138),
    ("jungle-breaks-inspired","Jungle Breaks-Inspired",164),
    ("organic-house-studies","Organic House",120),
    ("uk-bassline-inspired","UK Bassline-Inspired",138),
    ("idm-micro-rhythms","IDM Micro-Rhythms",116),
    ("contemporary-rnb-studies","Contemporary R&B",78),
    ("boom-bap-sketches","Boom-Bap Sketches",90),
    ("cinematic-tension-studies","Cinematic Tension",72),
    ("polyrhythmic-minimalism","Polyrhythmic Minimalism",112),
]
lookup = {row["slug"]: row for row in evidence["rows"]}
path = project / "src" / "data.json"
data = json.loads(path.read_text(encoding="utf-8"))
rows = data["queries"]["releases"]["rows"]
rows[:] = [row for row in rows if row["slug"] not in {n[0] for n in names}]
new = []
for i, (slug,name,bpm) in enumerate(names, 45):
    proof = lookup[slug]
    report = json.loads((base / slug / "checks" / "validation-report.json").read_text(encoding="utf-8"))
    if not (proof.get("local")==proof.get("remote")==proof.get("tag_commit") and proof.get("tag")=="refs/tags/v1.0.0" and proof.get("pages")=="built" and proof.get("http")==200 and proof.get("art_http")==200 and report["status"]=="PASS"):
        raise ValueError(f"Incomplete release evidence: {slug}")
    page = f"https://mizcausevic-dev.github.io/{slug}/"
    new.append({"order":i,"name":name,"slug":slug,"category":"New batch 3","bpm":bpm,"midiFiles":28,"studies":4,"tag":"v1.0.0","repository":f"https://github.com/mizcausevic-dev/{slug}","page":page,"pagesStatus":"built","httpStatus":200,"validation":"PASS","artwork":page+"art/hero.jpg"})
rows[:0] = new
data["generatedAt"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
actions = data["queries"]["next_actions"]["rows"]
actions[0]["evidence"] = "A local audit found 11 of the earlier 44 releases contained both a JPG hero and an MP4. The ten new releases also contain both, leaving 33 earlier packs without this media pair."
actions[1]["scope"] = "All 54 packs"
actions[2]["scope"] = "All 54 public releases"
actions[3]["scope"] = "54 Pages sites"
for metric in data["queries"]["releases"].get("source",{}).get("metricDefinitions",[]):
    if metric.get("label") == "Published release":
        metric["definition"] = "One of the 54 session repositories with verified public GitHub source and Pages."
path.write_text(json.dumps(data, indent=2, ensure_ascii=False)+"\n", encoding="utf-8", newline="\n")
