# Verification notes

**What this is.** The model in this repository was checked line by line against the Liszt
repository: the schemas, the records, the tools, and the documentation. Where the tools
disagreed with the documentation, or the documentation with the records, the disagreement
was resolved in code and the resolution is recorded here, with the reasoning, so that a
later reader can see why the model says what it says. **Application state:** the version under `liszt/`, 2026-09-14.

---

## 1. Library state

All 21 scenarios are drafts and none carries a DeTT&CT block, by decision on 2026-08-13:
invented scores made the library read as measured when nothing had been measured. The
model's structure is proven by the schemas, the validator, and records that pass it. To
exercise the scoring path, scenario 021's earlier reference scores were restored from
history, labeled in the file as an illustrative assessment, and the record returned to
`published`. Its spec and sealed prediction were re-emitted on the current code, the run
records were re-bound to the new prediction digest and re-scored. Its author and reviewer
are still placeholders; a real person has to stand behind it before it is cited outside
the program.

## 2. The organization scoped fields, and `source`

The three tools that handle per organization overlays disagreed on what an organization
may override. `tools/coverage.py` ignored `source`, `tools/emit_testspec.py` copied every
overlay field, and `tools/apply_session.py --org` wrote `source` into the overlay. The
measurement doc listed five org scoped fields; the session tool listed eight.

Resolved as: `source` is organization scoped, because one estate runs one product and
another runs a different one. The full list is `dettect`, `coverage`, `source`, `owner`,
`evidence`, `backlog_ref`, `notes`, `research_needed`, `score_provenance`, stated once in
`schema/coverage-overlay.schema.json` and used identically by all three tools and the doc.

Two further overlay defects. The doc's example used a `rows:` key with a mandatory
`baseline`; the real file and every tool use `telemetry:` and no baseline. The doc now
matches the file, and `baseline` is optional but checked when present. And the doc said an
inherited or absent row is unscored for the org; both tools kept the reference scores
instead, so an org that assessed two rows of six was reported as fully scored. Both tools
now follow the doc. The example org's view of 021 reports completeness 0.33.

## 3. Record types that had no schema

| Record | Before | Now |
|---|---|---|
| Incident | Six YAML files, no schema. The validator checked only that a cited slug existed. | `schema/incident.schema.json`, validated. Referential integrity both ways: an incident's `scenarios` must exist, and a scenario that cites an incident is warned when the incident does not list it back. |
| Framework baseline | One YAML file, no schema. | `schema/framework-baseline.schema.json`, validated. Warns while `owner` reads UNASSIGNED and while `frameworks/pinned/` has no checksums. |
| Coverage overlay | One example file, no schema, format described inconsistently. | `schema/coverage-overlay.schema.json`, validated, including the derived coverage tag, step existence, org and filename agreement. |
| Snapshot | Specified in docs/04 section 5; `tools/coverage.py` emitted a smaller, different shape. | `schema/snapshot.schema.json`; the tool emits the specified shape and validates before writing. |
| Environment | Not a record type. Runs described their environment in prose. | `schema/environment.schema.json`, records under `environments/`, an optional `environment.definition` on the run record that the validator cross-checks. |
| Agent run import | Did not exist. | `schema/agent-run-import.schema.json` and `tools/import_agent_run.py`. |

The validator's default run covers scenarios, use cases, incidents, baselines, overlays,
environments, run records and discovery runs. CI picks this up with no workflow change.

## 4. The snapshot and the measurement doc

`tools/coverage.py` diverged from docs/04 in four places, all aligned to the doc:

- The aggregate coverage was a mean of per scenario rates. The doc says step weighted, and
  says why: a mean makes splitting a scenario a lever on the number.
- The seven maturity gates were a different seven from the doc's M1 to M7. The tool now
  computes M1 reviewed, M2 scored in depth, M3 evidenced, M4 owned, M5 closed loop, M6
  remediable, M7 sourced, and only counts scenarios with every row scored.
- The snapshot lacked `snapshot_id`, `repo_commit`, `supersedes`, `retired_this_period`,
  `ids_added_this_period`, `ids_rescored_this_period` and `non_comparable_with`. All
  present. `--prior` fills the period ledgers from the previous snapshot; `--supersedes`
  records a correction. A first scoring is not counted as a rescore.
- The version tuple was read from the baseline file. It is now read from the pinned
  artifacts' checksum lock, and the snapshot records which source it used.

## 5. Two copies of the derivation rule

`derive_coverage()` existed in `tools/validate.py` and again in `tools/emit_testspec.py`.
There must be exactly one. The emitter now imports it.

## 6. Source tiers were off by one

The schema grades sources "0" first party, "1" secondary, "2" press, on every record type.
The intake prompts asked the model for 1, 2, 3, and the importer wrote those numbers
straight into the record, so an imported first party source landed as secondary and an
unreadable tier defaulted to 3, which the schema rejects. All of it now speaks the schema's
scale, and an unreadable tier lands as "2" with a review note rather than being guessed
upward.

## 7. Frameworks pinned and indexed

`tools/pin_frameworks.py` vendored ATT&CK 19.1, ATLAS 2026.07, the OWASP LLM 2025 PDF and
the DeTT&CT 2.2.0 tree with checksums. The OWASP Agentic PDF has no fetchable URL and is
still to be downloaded by hand. `tools/index_frameworks.py` projects the pins into
`frameworks/pinned/2026.07/index/`, a small committed set of tables: 858 ATT&CK
techniques with revoked and deprecated flags and the revoked-by walk, 15 tactics, 109
data components, 178 ATLAS techniques with the 37 attack references, 16 ATLAS tactics, 37
mitigations, 20 OWASP slots. The validator verifies every framework id on every record
against the index: unknown and revoked ids are errors on a published record, deprecated
ids warn. The snapshot reads its version tuple and artifact hashes from the pins.

## 8. The lab distinction

Runs execute against infrastructure, which will usually be a disposable build but is not
encoded as such. The `kind` field (lab-ephemeral, lab-persistent, production) was removed
from the environment definition, its targets, the run record, the discovery run record,
and the test spec's target allowlist. The environment carries `lifetime` (ephemeral or
persistent), which decides whether teardown must be proven, and `telemetry_pipeline`,
which decides what a run can prove. What the agent may do stays on the autonomy rung of
the run and the spec. The rung names were not renamed; that is an open decision. The word
lab remains in the older prose of docs/12 and the lab notes.

## 9. The agent run import

The agentic platform's orchestrator dispatches single purpose sub-agents, one per
scenario, which collect traces and hand Liszt one JSON document per scenario per run.
`schema/agent-run-import.schema.json` defines that document. `tools/import_agent_run.py`
validates it, checks the scenario and its steps, in test mode refuses a spec or prediction
digest that does not match disk, checks the cited environment and its pipeline mode, and
writes one immutable run record under `runs/`. It writes nothing else. Trace and
observation ids travel into the record as `trace_refs` on each observation and an
`imported_from` block on the run; the traces themselves stay in the tracing platform. Two
worked examples under `examples/agent-run-import/` were imported, scored and validated;
the discovery example correctly stops at the bridge because 021 carries a person's scores.

## 10. Entity inventory notes

- Three layer vocabularies, not two: `primary_layer_component` (12 value enum),
  `ai_infrastructure_layer` (5 value enum), and the step `layer` seam tag (free text, 18
  characters).
- Scenario carries a `retired` block: date, reason, optional superseded_by.
- Source citation is one shape with three parents: scenario provenance, use case sources,
  incident references.
- The scorecard is written into the run record file by `score_run.py --write`; the run is
  not immutable in the prototype. In the model, scorecard is a separate computed entity
  keyed to the run.
- Both promotion blocks share a shape and differ only in the evidence fields: use case
  evidence is true positive rate, window, volume; spec evidence is clean runs, window,
  environment faults.
- The viewer's `liszt-data.json` is the read model: scenarios with computed metrics,
  readiness blockers and use case ids, use cases, incidents, and a reverse index from
  technique id to scenario ids.

## 11. Known defects, checked

| Claim | Result |
|---|---|
| Use case template lists six outcome kinds, schema has seven | Confirmed, fixed |
| Intake doc grades tiers 1, 2, 3 against a schema of 0, 1, 2 | Confirmed, and deeper than the doc (section 6), fixed |
| Architecture diagram undercounts the stores | Confirmed, redrawn 2026-09-14 with every store, the platform input, and the scoring, import and viewer tools |
| `status` and `phase` on a use case overlap | The schema argues they are deliberately separate axes. A decision to reaffirm, not a defect |
| Baseline owner seat is empty | Confirmed; the validator says so on every run |

## 12. Findings for an analyst, not fixed here

- Scenario 021 rows 2 and 6 cite data component `DC0074`, which the pinned bundle names
  "Driver Metadata". Both rows describe network egress; the components that fit are
  `DC0078` Network Traffic Flow, `DC0085` Network Traffic Content, or `DC0082` Network
  Connection Creation. The id exists, so the validator accepts it; the mapping is an
  analyst's call and the record is illustrative.
- Scenario 021 row 5 cites `DC0057`, "Snapshot Creation", on a row about container escape
  and credential use read from Kubernetes audit and CloudTrail. `DC0019` Pod Creation,
  `DC0072` Container Creation or `DC0069` Cloud Service Modification fit better.
- Two incidents have no tier 0 source and now say so on every validator run.
- `score_run.py --write` reflows long strings in the run record on rewrite. Comments
  survive; line breaks inside folded scalars do not. Cosmetic, worth knowing before
  reading a diff.

## 13. Infrastructure shapes (2026-09-14)

The viewer's Environments page carried the five AI layer cards (what sits at each layer, its
components, its seam tags, why it matters) and six environment shapes from the beyond-AI
proposal as text inside the page's JavaScript. None of it was a record. The model had rolled
the layers up into a five row code and name vocabulary and dropped the rest.

Now `schema/infrastructure-shape.schema.json` defines a shape with its layers, seam
vocabulary and emitted categories; `infrastructure/` holds the AI stack (catalog) and the six
proposed shapes, seeded from the cards; the scenario gains an optional `classification.stack`
defaulting to the AI stack; the environment definition names the shape it instantiates; and
the validator checks that the AI stack's canonical layer strings equal the scenario schema's
enum, that a scenario's shape exists and is catalog, and that a published scenario's step
seam tags are in its shape's vocabulary. The viewer reads the records for its layer pages,
its beyond-AI cards and its seam consistency check, so the page can no longer drift from the
library. Emitted categories for the AI stack were harvested from the evidence rows of the
twenty-one scenarios.

## 14. One shape per snapshot (2026-09-14)

Decided: no cross shape coverage figure is ever reported. The snapshot carries `shape` in
its identity and its body, `tools/coverage.py` reports one shape per run (`--shape`, the AI
stack by default) and excludes scenarios classified against any other shape from the
population, and the measurement doc's resolution rules gain rule 7 saying so.
