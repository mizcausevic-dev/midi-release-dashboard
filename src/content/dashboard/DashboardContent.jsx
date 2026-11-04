import React, { useState } from 'react';
import { DataComponent, useDataApp, useDashboardTabs } from '../../data-app-public.jsx';
import './example.css';
export function DashboardContent() {
  useDashboardTabs([{id:'dashboard',label:'Release ledger'}]);
  const { queries } = useDataApp();
  const rows = queries.releases.rows, actions = queries.next_actions.rows;
  const [family,setFamily] = useState('All'), [search,setSearch] = useState(''), [selected,setSelected] = useState(rows[0].slug);
  const shown = rows.filter(r => (family === 'All' || r.category === family) && r.name.toLowerCase().includes(search.toLowerCase()));
  const active = rows.find(r => r.slug === selected) || rows[0];
  return <article className="release-page">
    <header><h1>MIDI Release Control</h1><p>Explore the session releases and the work that comes next.</p><p className="asof">Snapshot: November 4, 2026. This is not a live monitor.</p></header>
    <DataComponent variant="plain" id="release-total" queryId="releases" kind="metric" title="Release snapshot" sourceRows={rows} displayRows={rows}><div className="metrics"><div><strong>{rows.length}</strong><span>Published releases</span></div><div><strong>{rows.reduce((sum,r)=>sum+r.midiFiles,0)}</strong><span>MIDI exports</span></div><div><strong>{rows.filter(r=>r.pagesStatus==='built' && r.httpStatus===200).length}/{rows.length}</strong><span>Pages checked</span></div><div><strong>{rows.filter(r=>r.tag==='v1.0.0').length}</strong><span>v1.0.0 tags</span></div></div></DataComponent>
    <nav className="section-nav"><a href="#ledger">Release ledger</a><a href="#next">Next work</a><a href="#evidence">Evidence</a></nav>
    <section id="ledger"><h2>Release ledger</h2><div className="filters-local"><label>Family <select value={family} onChange={e=>setFamily(e.target.value)}><option>All</option>{[...new Set(rows.map(r=>r.category))].map(x=><option key={x}>{x}</option>)}</select></label><label>Search packs <input value={search} onChange={e=>setSearch(e.target.value)} placeholder="Search by name" /></label><span>Showing {shown.length} of {rows.length}</span></div>
      <DataComponent variant="plain" id="release-ledger" queryId="releases" kind="table" title="Published packs" sourceRows={shown} displayRows={shown}><div className="ledger"><div className="table-scroll"><table><thead><tr><th>Pack</th><th>Family</th><th>BPM</th><th>MIDI</th><th>Links</th></tr></thead><tbody>{shown.map(r=><tr key={r.slug} className={selected===r.slug?'selected':''}><td><button onClick={()=>setSelected(r.slug)} aria-pressed={selected===r.slug}>{r.name}</button></td><td>{r.category}</td><td>{r.bpm}</td><td>{r.midiFiles}</td><td><a href={r.repository}>Source</a> · <a href={r.page}>Page</a></td></tr>)}</tbody></table>{shown.length===0 && <p>No packs match this filter.</p>}</div><aside><h3>{active.name}</h3><dl><dt>Family</dt><dd>{active.category}</dd><dt>Tempo</dt><dd>{active.bpm} BPM</dd><dt>Studies</dt><dd>{active.studies}</dd><dt>Tag</dt><dd>{active.tag}</dd><dt>Pages</dt><dd>{active.pagesStatus}, HTTP {active.httpStatus}</dd><dt>Validation</dt><dd>{active.validation}</dd></dl><p><a href={active.page}>Open pack page ↗</a></p><p><a href={active.repository}>View source ↗</a></p></aside></div></DataComponent>
    </section>
    <section id="next"><h2>What should happen next</h2><p>Priorities are recommendations, not completed work.</p><DataComponent variant="plain" id="next-actions" queryId="next_actions" kind="table" title="Recommended work" sourceRows={actions} displayRows={actions}><ol className="actions-list">{actions.map(a=><li key={a.title}><b>{a.priority}</b><div><h3>{a.title}</h3><p>{a.why}</p><small>{a.evidence} {a.gate}</small></div><span>{a.scope}</span></li>)}</ol></DataComponent></section>
    <section id="evidence"><h2>What the snapshot proves</h2><p>During the release run, GitHub Pages deployment state, root HTTP responses, and v1.0.0 tags were checked. The ledger records each result as observed. Technical checks do not establish musical quality, rights clearance, or commercial readiness.</p></section>
  </article>;
}
