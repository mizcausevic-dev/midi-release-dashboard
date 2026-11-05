import json
from datetime import datetime,timezone
from pathlib import Path
project=Path(__file__).resolve().parents[1];base=project.parent/'midi-release-train'/'next-25-releases'
profiles=json.loads((base/'batch-profiles.json').read_text(encoding='utf8'));proof={x['slug']:x for x in json.loads((base/'live-evidence.json').read_text(encoding='utf8'))};cleanup=json.loads((base/'cleanup-evidence.json').read_text(encoding='utf8'))
assert len(profiles)==len(proof)==len(cleanup)==25 and all(x['ok'] for x in proof.values())
path=project/'src'/'data.json';data=json.loads(path.read_text(encoding='utf8'));rows=data['queries']['releases']['rows']
assert len(rows)==84 and not set(proof).intersection(x['slug'] for x in rows)
new=[]
for i,p in enumerate(profiles,85):
 slug,name,code,bpm=p[:4];e=proof[slug];page=e['page']
 new.append({'order':i,'name':name,'slug':slug,'category':'New batch 7','bpm':bpm,'midiFiles':e['midi_files'],'studies':4,'tag':'v1.0.0','repository':'https://github.com/mizcausevic-dev/'+slug,'page':page,'pagesStatus':'built','httpStatus':200,'validation':'PASS','artwork':page+'art/hero.jpg','video':e['video'],'videoStatus':'verified'})
rows[:0]=new;data['generatedAt']=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');data['buildStatus']='complete'
for a in data['queries']['next_actions']['rows']:
 a['scope']=a['scope'].replace('84','109');a['evidence']=a['evidence'].replace('All 84 motion previews are live','All 109 motion previews were verified live')
source=data['queries']['releases']['source'];source['evidenceFlow'].append({'title':'Twenty-five-pack release','detail':'Twenty-five repositories, tags and Pages sites were verified. The public video, artwork and MIDI ZIP bytes matched recorded SHA-256 values. The new local MP4 files and disposable Git publishing checkouts were removed after verification.'})
for m in source.get('metricDefinitions',[]):
 if m.get('label')=='Published release':m['definition']='One of the 109 session repositories with verified public GitHub source and Pages.'
 if m.get('label')=='Validated MIDI exports':m['definition']='Sum of recorded MIDI exports, including validated focused clips in later batches.'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('Added',len(new),'verified packs; total',len(rows))
