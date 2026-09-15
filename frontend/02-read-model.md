# The read model

This page is how every screen in the application gets its data. There is one way, and
every screen uses it.

1. A screen never has data of its own. When it needs to show something, it asks the back
   end for one of the packages listed in the table below.
2. Each package is already complete. The back end has computed every number in it: the
   verdicts, the counts, the averages, the readiness blockers. The screen displays what it
   receives. It does not calculate anything from it.
3. Every request says three things: whose scores (the organization), which kind of estate
   (the shape), and whether drafts are included. The answer repeats them back, and the
   screen shows all three in its header, every time.
4. If a screen needs a number that no package carries, the package is extended on the back
   end. The screen is never changed to work it out itself.

The reason for rule 2 is the program's central promise: a coverage figure in Liszt cannot be
authored or improvised, only computed by one rule in one place. If two screens calculated
it, they would disagree, and nobody could tell which was right.

The companion page, `03-write-model.md`, is the same idea for saving: every screen saves
the same way, by sending a change set that carries a name and a reason.

---

Everything a screen reads comes from these endpoints. Each returns exactly what the current
build puts in `liszt-data.json` (contract: `../liszt/docs/07-viewer-data-contract.md`), so the
real file under `../examples/viewer/` is the response example for the whole read side.

## Endpoints

| Endpoint | Returns | Used by |
|---|---|---|
| `GET /library?org=&shape=&drafts=` | the view header (`view`, `baseline`, `library`), the shape, and the counts | every screen's header |
| `GET /scenarios?org=&shape=&drafts=` | `scenarios[]` with computed `counts`, `metrics`, `use_case_ids`, `testing`, `discovery` | Scenario list, Coverage, Scenario management |
| `GET /scenarios/{id}?org=` | one scenario with the same computed fields, for the organization's assessment | Scenario record |
| `GET /use-cases` | `use_cases[]` as committed | Use cases, Scenario chips |
| `GET /incidents` | `incidents{}` by slug | Scenario "grounded in" |
| `GET /frameworks` | `baseline`, `frameworks{}` reverse index, `owasp_names`, `frameworks_detail`, `baseline_meta` | Frameworks, Documentation |
| `GET /frameworks/index` | the identifier index: names, revoked, deprecated, replacements | Frameworks, Edit mode id chips |
| `GET /infrastructure` | `infrastructure[]` shapes | Documentation, Edit mode layer and seam pickers, Administration |
| `GET /environments` | environment definitions, every version | Scenario management, Administration |
| `GET /organizations` | organizations | header selector, Session, Administration |
| `GET /scenarios/{id}/spec`, `/prediction`, `/runs`, `/runs/{run}/scorecard` | the testing chain for one scenario | Scenario management |
| `GET /snapshots?org=&shape=`, `GET /snapshots/{id}` | metrics snapshots | Reports |

## Three parameters that travel with every read

| Parameter | Meaning | Default |
|---|---|---|
| `org` | whose assessment: the reference organization or a named one | reference |
| `shape` | which infrastructure shape's scenarios | SHAPE-AI |
| `drafts` | whether unpublished records are included | false |

The response always echoes all three in `view`, and every screen shows them. A figure
without them is a number people act on wrongly.

## Fields a screen must never compute

| Field | Why |
|---|---|
| any `coverage` tag | one rule, one place, on the server |
| `counts`, `metrics.*`, `library.*` | step weighted, unscored excluded; getting this wrong is invisible downstream |
| `use_case_ids` | the join is checked both ways on the server |
| `testing.blockers`, `discovery.blockers` | the emitter's own gate |
| the ATT&CK and ATLAS roll-up | the union of step mappings |

If a screen needs a number the read model does not carry, the read model grows. The
screen does not calculate.

## Versioning

`data_version` is the only compatibility promise: within a version, fields are added and never
removed or repurposed. A screen reads it and refuses to render an unknown version rather
than mis-display. Every record response carries a `version` (its content digest) that a change
set must quote back; see the write model.
