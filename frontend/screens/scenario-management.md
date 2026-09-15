# Screen: Scenario management

**Route:** `#/testing`
**One sentence:** four steps in a rail: readiness, design tests, design use cases, run and rescore.
**Reference:** `renderTesting()`, `readinessPane()`, `designPane()`, `usecasePane()`, `rescorePane()` in `liszt/tools/build_viewer.py`.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Detection engineer | See which scenarios can be tested today and why not; design a test; design a use case; read a scorecard; accept or reject proposed rescores |

## 2. The four steps

| Step | Shows | Reads | Writes |
|---|---|---|---|
| 1. Readiness | every scenario with its two doors: scoring path (blockers or available) and discovery path (blockers or available). Filter: ready, blocked, all. Blockers shown verbatim | `scenarios[].testing.blockers`, `.discovery.blockers` | nothing |
| 2. Design tests | pick a scenario; the test design prompt (unit and full path testing, a blocked ledger); the record as JSON to copy | `scenarios[]` | nothing |
| 3. Design use cases | pick a scenario sorted by not yet covered, then priority, then evidence; the use case design prompt | `scenarios[].use_case_ids` | nothing; the result is written on the Use cases screen |
| 4. Run and rescore | for a scenario with a spec: the spec and sealed prediction, the runs, each run's scorecard (per row verdict, totals, by class, caveats) and its proposed rescores with Accept and Reject | `GET /scenarios/{id}/spec`, `/prediction`, `/runs`, `/runs/{id}/scorecard` | `POST /runs/{id}/rescores/{n}/accept` with name, reason and the run id as ticket |

## 3. The scorecard, as shown

| Part | Shows |
|---|---|
| Header | run id, scenario, spec, environment id and version, pipeline mode, autonomy used |
| Rows | step, predicted, observed, verdict (confirmed, overestimate, severe overestimate, underestimate, unscoreable, not executed), source match |
| Totals | scored of rows, exact match rate, optimism index with its sign explained, source precision, unpredicted signals |
| By class | signal presence, source attribution, detection fires; "not under test" when the pipeline was not mirrored |
| Caveats | every environment deviation |
| Proposed rescores | step, field, from, to, reason; Accept, Reject |

## 4. Rules

1. **Given** a proposed rescore, **when** accepted, **then** the change set carries the run id as its ticket, so the change appears as a rescore in the next snapshot, and the assessment row is updated only after the server applies it.
2. **Given** a run whose prediction digest no longer matches, **when** the scorecard is requested, **then** the server refuses and the screen shows its message; nothing is scored.
3. **Given** a scratch pipeline, **when** the scorecard renders, **then** Have and Collectable rows read unscoreable at the coverage level and the note says why.
4. **Given** a blocker list, **when** it renders, **then** every string is shown verbatim.
5. **Given** a triggered stop condition on a run, **when** it renders, **then** it reads as a successful guardrail, not a failed run.

## 5. Done when

- [ ] Readiness matches the reference page for the drafts build (one scenario open on the scoring path, the rest blocked).
- [ ] The three RUN-021 scorecards render from the examples.
- [ ] Accept and Reject round trip against the mock server.
