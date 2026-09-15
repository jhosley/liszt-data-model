# Screen: Scenario

**Route:** `#/scenario/<id>`, for example `#/scenario/021`
**One sentence:** a list of every scenario on the left, and the full record of the selected one on the right.
**Reference:** the working version of this screen is the Scenarios tab of `liszt/build/viewer/liszt-viewer.html` (build it with `./liszt viewer`). Its code is `renderList()` and `renderDetail()` in `liszt/tools/build_viewer.py`. Match its behavior; the look is yours.

---

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Analyst | Read a record end to end while writing or reviewing it |
| System owner, in a scoring session | Find their scenario and read the evidence rows before scoring them (scoring itself is the Session screen) |
| Detection engineer | See which evidence rows exist so a use case can point at them |
| Leadership, risk | Read one scenario in plain language: what happens, what we would see, what we would not |

## 2. What it looks like

```
+---------------------------+------------------------------------------------------+
| Filters                   |  NOW   Seen in the wild   published   L3 · Orch...   |
| [search.............]     |  Scenario 021 · Agent sandbox escape → autonomous    |
| priority v  evidence v    |  intrusion                                           |
| layer v  status v  cov v  |  one_liner in plain language                         |
|                           |                                                      |
| 21 of 21                  |  Why this priority          (2 to 4 bullets)         |
| +-----------------------+ |  Attack path                (3 to 6 numbered steps)  |
| | 021  NOW  wild        | |  Evidence and detection map (table, one row a step)  |
| | Agent sandbox escape  | |  Operational use cases      (chips, link out)        |
| | [====verdict bar====] | |  Analysis                   (three notes)            |
| | L3 · Orch  6 steps    | |  If this scaled up          (note, always hypothet.) |
| +-----------------------+ |  Hardening                  (table)                  |
| | 020  BACKLOG ...      | |  Framework mapping          (id chips + caveat)      |
| ...                       |  Grounded in                (incidents)              |
|                           |  Sources                    (tiered links)           |
|                           |  Testing paths              (two doors, blockers)    |
|                           |  Record                     (file, author, reviewer) |
+---------------------------+------------------------------------------------------+
```

The screen has two modes, switched by an **Edit** toggle in the record header. Read is the default. Edit is available to any signed in person; no session is needed. Section 10 says what Edit changes.

## 3. The list (left)

One card per scenario. Data comes from `scenarios[]` in `liszt-data.json`.

| Card shows | From | Example, scenario 021 |
|---|---|---|
| Id | `id` | `021` |
| Priority chip | `classification.priority` | `NOW` |
| Evidence tier chip | `classification.evidence` | `seen-in-the-wild`, shown as "Seen in the wild" |
| Status chip, only when not published | `status` | hidden for 021; `draft` for the other twenty |
| Title | `title` | Agent sandbox escape → autonomous intrusion |
| Verdict bar | `counts.Have`, `counts.Collectable`, `counts.Blind`, `counts.Unscored` | 3 Have, 2 Collectable, 1 Blind, 0 Unscored |
| Layer | `classification.ai_infrastructure_layer` | `L3 · Orchestration & Agent` |
| Step count | length of `telemetry[]` | 6 steps |
| Have share, or "not scored" | `metrics.have` (null when nothing is scored) | 50% Have |

**Filters:** free text over id and title; priority; evidence tier; layer; status; coverage (scored or unscored); testable (readiness has no blockers). A count reads "n of total". Filters combine with AND.

**Empty state:** "No scenario matches these filters." Never an empty white panel.

**Selecting a card** sets the route and renders the record on the right. The selected card is marked.

## 4. The record (right), section by section

Sections appear in this order. A section with nothing to show is omitted, not shown empty, except the ones marked always.

| # | Section | Shows | From | Rule |
|---|---|---|---|---|
| 1 | Header chips, always | priority, evidence tier, status, layer | `classification.*`, `status` | Status must be visible. A draft is a plan, not a claim |
| 2 | Title and one liner, always | "Scenario 021 · title", then the plain language paragraph | `id`, `title`, `one_liner` | |
| 3 | Why this priority, always | 2 to 4 bullets | `classification.priority_rationale[]` | |
| 4 | Attack path, always | numbered steps: `[seam tag]` text, "a control held here" marker, technique id chips | `attack_path[].step`, `.layer`, `.text`, `.control_held`, `.attack[]`, `.atlas[]` | Order by `step`. The number is a label, never a key |
| 5 | Evidence and detection map, always | one row per evidence row, see section 5 | `telemetry[]` | See section 5 |
| 6 | Verdict bar and legend, always | Have, Collectable, Blind, Unscored, each with color **and** word | `counts` | Never color alone |
| 7 | Operational use cases | one chip per use case, linking to `#/usecase/<id>` | `use_case_ids[]` | Omit when empty |
| 8 | Analysis | three notes: what we can already see, where we are blind, how we detect it | `commentary.already_see`, `.blind`, `.how_detect` | Omit missing notes |
| 9 | If this scaled up | one note prefixed "Hypothetical, not observed." | `scaled_up` | The prefix is mandatory |
| 10 | Hardening | table: action, breaks step, leverage, owner, ticket | `hardening[]` | Omit when empty |
| 11 | Framework mapping, always | four rows of id chips: ATT&CK, ATLAS, OWASP LLM, OWASP Agentic; then a caveat box when editorial | `framework_mapping.attack[]`, `.atlas[]`, `.owasp_llm[]`, `.owasp_agentic[]`, `.mapping_confidence`, `.mapping_notes` | When `mapping_confidence` is `editorial`, show "This mapping is our own judgment, not upstream endorsed." plus the notes. Never present a mapping as authoritative without that field saying so |
| 12 | Grounded in | incident title, what happened, source | `incidents[]` slugs, resolved through top level `incidents{}` | Omit when empty |
| 13 | Sources | tier chip, linked title, note; sorted by tier, 0 first | `provenance.sources[]` | Tier is "0", "1", "2" as strings |
| 14 | Testing paths, always | two doors, "Scoring path" and "Discovery path". Each shows either "available" and the command, or a count of blockers and the blockers verbatim | `testing.blockers[]`, `discovery.blockers[]` | Show blockers word for word; they are written to be read |
| 15 | Record, always | file name, authored by, reviewed by, last updated, baseline | `slug`, `provenance.authored_by`, `.reviewed_by`, `.last_updated`, `framework_mapping.baseline` | "not yet reviewed" when reviewer is absent |

## 5. The evidence table, one row per evidence row

| Column | From | Example, row 2 of 021 |
|---|---|---|
| # | `telemetry[].step`, or `c` when `kind` is `control` | 2 |
| Signal emitted, with evidence underneath in small text | `.signal`, `.evidence` | Egress from a sandboxed workload; SIEM saved search NET-EGRESS-ANOM-07 |
| Where it is emitted | `.emitted_at` | Egress FW / proxy · NDR · package-registry logs |
| Exact source | `.source` | Palo Alto NGFW traffic logs + Zscaler proxy, index=net_egress; Artifactory access.log |
| Collected | verdict chip from `.coverage`; scores `v3 d2` from `.dettect.visibility` and `.dettect.detection`; "Research" chip when unscored and `.research_needed`; "agent-proposed" chip when `.score_provenance` is `agent-proposed` | Have, v3 d2 |
| Detection opportunity | `.detection_opportunity` | Sandbox reaching the internet through its one allowed egress path |
| Owner, ticket underneath | `.owner`, `.backlog_ref` | Network Security |

The verdict comes from the file. **Do not compute it.** If a row has no `dettect`, it is Unscored: show the word "not scored" in the scores line and the Unscored chip.

## 6. States

| State | When | What the screen does |
|---|---|---|
| Nothing selected | first load, no route | Right panel reads "Select a scenario." |
| Draft record | `status` is not `published` | Status chip shows the status. Everything else renders normally |
| Unscored rows | any row without `dettect` | Row shows Unscored. Bar counts it as Unscored. Have share shows "not scored" when every row is unscored |
| Illustrative record | header comment in the record says so; 021 today | No special treatment on this screen. The reference page shows it on use cases only. Acceptable to add a chip later |
| Retired record | `status` is `retired` | Not in `liszt-data.json`; never shown |
| Organization view | the file was built with `--org` | `view.org` is not "reference assessment". Show the organization name in the page chrome, always. Rows the organization has not assessed are Unscored, even if the reference record has scores |
| Includes drafts | `view.includes_drafts` is true | Say so in the page chrome, always |

## 7. Rules, as acceptance criteria

1. **Given** a row with `dettect.visibility` 0, **when** it renders, **then** the chip reads Blind and no control on this screen can change it.
2. **Given** a row with no `dettect`, **when** it renders, **then** it reads Unscored, and the Have share for the scenario excludes it rather than counting it as Blind.
3. **Given** a scenario where every row is unscored, **when** the card renders, **then** the Have share reads "not scored", not 0%.
4. **Given** any verdict chip, **when** it renders, **then** the word is present next to the color.
5. **Given** `mapping_confidence` is `editorial`, **when** the framework section renders, **then** the caveat box is shown with the mapping notes.
6. **Given** `scaled_up` is present, **when** it renders, **then** it is prefixed "Hypothetical, not observed."
7. **Given** a scenario with `testing.blockers` non empty, **when** the testing section renders, **then** every blocker string is shown verbatim and no command is shown for that door.
8. **Given** the file was built for an organization, **when** any part of this screen renders, **then** the organization name is visible.
9. **Given** the file includes drafts, **when** any part of this screen renders, **then** that is visible.
10. **Given** read mode, **when** the user interacts, **then** nothing is written to any record.
11. **Given** edit mode and a changed score on a row that already had scores, **when** Save is submitted without a ticket, **then** the dialog refuses with "a score change without a ticket is a rescore" and nothing is sent.
12. **Given** a change set the server refuses, **when** the response arrives, **then** every message is shown next to the field it names and the person's edits are kept.
13. **Given** Publish with a reviewer name equal to the author's, **when** submitted, **then** the server refuses and the screen shows the validator's message.
14. **Given** edit mode, **when** the verdict chip, the counts, the roll-up or the readiness section render, **then** each is marked derived and has no control.

## 10. Edit mode

**Entering.** The Edit toggle in the record header. The signed in person's name is shown next to it. Nothing changes on screen until a field is touched.

**What becomes editable.** Two kinds of field, saved as two parts of one change set.

| Kind | Fields | Scoped to |
|---|---|---|
| Assessment, per evidence row | would we see it (0 to 4), does anything alert (minus 1 to 5), the five quality dimensions, exact source, evidence, owner, ticket, notes, needs research | the organization the page is viewing. The reference organization when none is selected |
| Record, shared | title, one liner, priority and its rationale lines, mode, infrastructure shape, objective layer, each attack step's text, seam tag, control held and technique ids, each evidence row's signal, where emitted, detection opportunity and data components, the three analysis notes, if this scaled up, hardening rows, incident citations, source citations, OWASP mappings, mapping confidence and notes, working notes | everyone |

**What never becomes editable, and is marked "derived" when Edit is on.** The verdict chip and the scores line it comes from (the verdict recomputes live on screen from the two scores as a preview, but the stored one is the server's), the counts and the bar, the ATT&CK and ATLAS roll-up, the use case chips, the testing paths, the status, the reviewer, the dates, the baseline.

**Row controls in Edit.** Each evidence row becomes a card with the two score selects (each option carries its label, "0  None. Nothing produces this"), the verdict preview, and the text fields. The card shows what the row still owes for its verdict: a Have owes a source and evidence; a Collectable owes a source and an owner; a Blind owes an owner. Owed items are shown, not enforced, until Save.

**Save.** One button. It opens a short dialog: your name (prefilled, read only), reason (required, free text), ticket (optional; required when a score on an already scored row changed, because a score change with no ticket is a rescore and is reported as one). Submit sends one change set, `POST /scenarios/{id}/changes`, see `03-write-model.md`. The server validates the whole record and the assessment, recomputes every derived value, and answers with either the new version or a list of messages. Messages are shown next to the field they name; errors block the save, warnings do not. The record on screen is replaced by the server's version after a successful save.

**Discard.** Returns to read mode and drops every unsaved edit, after a confirmation when anything was touched.

**Conflict.** The change set carries the version it was made from. If the record changed underneath, the server refuses; the screen says so, reloads the record, and keeps the person's edits in the cards so they can be reapplied.

**Publish, Retire.** Separate actions in the header, in Edit mode only, each its own request. Publish asks for the reviewer's name, which must differ from the author's, and runs the strict gate; a refusal shows every message. Retire asks for a reason and an optional successor.

**Illustrative data.** When the record is marked illustrative, Edit shows a banner saying the scores are invented reference material and a real assessment replaces them.

## 11. Data contract, the keys this screen reads

From `liszt-data.json` (`examples/viewer/liszt-data.json` is a real one; `liszt/docs/07-viewer-data-contract.md` is the contract):

```
data_version                      integer, must be 1; refuse to render otherwise
view.org                          string
view.includes_drafts              boolean
scenarios[]                       the records, plus computed fields:
  counts                          {Have, Collectable, Blind, Unscored}
  metrics.have                    number or null
  metrics.completeness            number
  use_case_ids[]                  strings
  testing.blockers[]              strings
  discovery.blockers[]            strings
incidents{}                       slug to incident record
use_cases[]                       for chip titles only
```

Everything else the screen shows is a field of the scenario record exactly as committed. Field by field definitions, with a description on every field, are in `schema/scenario.schema.json`.

## 12. Done when

- [ ] Every section in section 4 renders for scenario 021 with the example values above.
- [ ] Every row of 021's evidence table matches section 5.
- [ ] The fourteen acceptance criteria pass.
- [ ] Edit mode: every field in section 10's editable table has a control; every field in the never editable list has none.
- [ ] Save round trip against the mock server: success replaces the record; refusal shows messages by field.
- [ ] The list filters combine and the count updates.
- [ ] The empty state and the nothing selected state render.
- [ ] A file built with `--org _example-org` shows the organization name and marks rows 1, 3, 4 and 6 of 021 Unscored.
- [ ] Color contrast meets WCAG AA using the house colors: Have `#1E7F4B`, Collectable `#B5852B`, Blind `#B0463B`, Unscored `#9AA7B1`.
