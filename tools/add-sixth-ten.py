import json
from datetime import datetime,timezone
from pathlib import Path
project=Path(__file__).resolve().parents[1]
base=project.parent/'midi-release-train'/'sixth-ten-releases'
profiles=json.loads((base/'batch-profiles.json').read_text(encoding='utf8'))
proof={x['slug']:x for x in json.loads((base/'live-evidence.json').read_text(encoding='utf8'))}
cleanup=json.loads((base/'cleanup-evidence.json').read_text(encoding='utf8'))
assert len(profiles)==len(proof)==len(cleanup)==10 and all(x['ok'] for x in proof.values())
path=project/'src'/'data.json';data=json.loads(path.read_text(encoding='utf8'));rows=data['queries']['releases']['rows']
assert len(rows)==74 and not set(proof).intersection(x['slug'] for x in rows)
new=[]
for i,p in enumerate(profiles,75):
 slug,name,code,bpm=p[:4];e=proof[slug];page=e['page']
 new.append({'order':i,'name':name,'slug':slug,'category':'New batch 6','bpm':bpm,'midiFiles':e['midi_files'],'studies':4,'tag':'v1.0.0','repository':'https://github.com/mizcausevic-dev/'+slug,'page':page,'pagesStatus':'built','httpStatus':200,'validation':'PASS','artwork':page+'art/hero.jpg','video':e['video'],'videoStatus':'verified'})
rows[:0]=new
data['generatedAt']=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
for action in data['queries']['next_actions']['rows']:
 action['scope']=action['scope'].replace('74','84')
 action['evidence']=action['evidence'].replace('All 74 preview audio files decoded','The 74 earlier preview audio files decoded').replace('All 74 motion previews are live','All 84 motion previews are live')
source=data['queries']['releases']['source']
source['evidenceFlow'].append({'title':'Sixth batch','detail':'Ten new repositories, version tags and Pages sites were verified. Public video, artwork and MIDI archive bytes matched the recorded SHA-256 values. The new MP4 files and temporary publishing checkouts were removed locally after verification.'})
for metric in source.get('metricDefinitions',[]):
 if metric.get('label')=='Published release':metric['definition']='One of the 84 session repositories with verified public GitHub source and Pages.'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
print('Added ten verified releases; total',len(rows))
