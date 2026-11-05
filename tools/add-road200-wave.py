import json,sys
from datetime import datetime,timezone
from pathlib import Path
project=Path(__file__).resolve().parents[1];folder=sys.argv[1];category=sys.argv[2];base=project.parent/'midi-release-train'/folder
profiles=json.loads((base/'batch-profiles.json').read_text(encoding='utf8'));proof={x['slug']:x for x in json.loads((base/'live-evidence.json').read_text(encoding='utf8'))};cleanup=json.loads((base/'cleanup-evidence.json').read_text(encoding='utf8'))
assert len(profiles)==len(proof)==len(cleanup) and all(x['ok'] for x in proof.values())
path=project/'src'/'data.json';data=json.loads(path.read_text(encoding='utf8'));rows=data['queries']['releases']['rows'];old=len(rows);assert not set(proof).intersection(x['slug'] for x in rows)
new=[]
for i,p in enumerate(profiles,old+1):
 slug,name,code,bpm=p[:4];e=proof[slug];page=e['page'];new.append({'order':i,'name':name,'slug':slug,'category':category,'bpm':bpm,'midiFiles':e['midi_files'],'studies':4,'tag':'v1.0.0','repository':'https://github.com/mizcausevic-dev/'+slug,'page':page,'pagesStatus':'built','httpStatus':200,'validation':'PASS','artwork':page+'art/hero.jpg','video':e['video'],'videoStatus':'verified'})
rows[:0]=new;total=len(rows);data['generatedAt']=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ');data['buildStatus']='complete'
for a in data['queries']['next_actions']['rows']:
 a['scope']=a['scope'].replace(str(old),str(total));a['evidence']=a['evidence'].replace('All '+str(old)+' motion previews were verified live','All '+str(total)+' motion previews were verified live')
source=data['queries']['releases']['source'];source['evidenceFlow'].append({'title':category,'detail':str(len(new))+' additional public repositories, version tags, Pages sites, video files, artwork and MIDI archives were verified; new local MP4s and disposable publishing checkouts were removed afterward.'})
for m in source.get('metricDefinitions',[]):
 if m.get('label')=='Published release':m['definition']='One of the '+str(total)+' session repositories with verified public GitHub source and Pages.'
path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n');print('Added',len(new),'verified packs; total',total)
