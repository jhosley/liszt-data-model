# Screen: Use cases

**Route:** `#/usecases`, `#/usecase/<id>`
**One sentence:** every use case on the left, the selected record on the right, editable in Edit mode, with an Add action for a new one.
**Reference:** `renderUCList()`, `renderUCDetail()`, `ucNewForm()` in `liszt/tools/build_viewer.py`.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Detection engineer | Write a use case, move it through its engineering phases, set its operating status, keep its limits honest |
| Reader | See what is done with a scenario's evidence, who receives it, and what it cannot tell you |

## 2. What it looks like

```
+-------------------------+-------------------------------------------------+
| 12 use cases  [Add]     | UC-006  built  in-testing  notify   [Edit]      |
| +---------------------+ | Downstream sink exploit traced back to model    |
| | built  in-testing   | | output                                          |
| | alert               | | Why it exists (rationale)                       |
| | UC-006 Downstream...| | Serves scenario 009, steps 1, 2   + framework ids|
| | serves scenario 009 | | Trigger: signal / source                        |
| +---------------------+ | Composes: role  signal / source                 |
| ...                     | Delivery: strategy -> destination               |
|                         | Outcome: kind, action                            |
|                         | Who: builds, operates, receives                  |
|                         | Read more (sources)                              |
|                         | Delivery state: phase since, ticket              |
|                         | What it cannot tell you (limits)                 |
+-------------------------+-------------------------------------------------+
```

## 3. The list

| Card shows | From |
|---|---|
| Status chip (proposed, built, tuned, retired) | `status` |
| Phase chip | `phase.value` |
| Outcome kind tag | `outcome.kind` |
| Id and title | `id`, `title` |
| "serves scenarios 009" | `covers[].scenario` |

Empty state: "No use case records yet."

## 4. The record, section by section

| Section | Shows | From | Rule |
|---|---|---|---|
| Header, always | id, status, phase, autonomy chip with a tooltip explaining notify, assisted, autonomous | `status`, `phase.value`, `outcome.autonomy` | Status and autonomy always visible. A proposed use case is a plan; autonomy above notify means a machine acts first |
| Illustrative banner | when set | `provenance.illustrative` | Mandatory when true |
| Why it exists | the rationale paragraph | `rationale` | |
| Serves | one line per covered scenario: id, title, steps, linking to the scenario; then the framework ids derived from those steps; a "thin" note when the steps carry no ids | `covers[]`, resolved through `scenarios[]` | Derived; not editable |
| Trigger | signal, source | `trigger.signal`, `.source` | |
| Composes | role, signal, source per item; or "nothing; a single signal use case" | `composes[]` | The empty list is an answer, not a gap |
| Delivery | strategy tag, destination | `pipeline.strategy`, `.destination` | |
| Outcome | kind tag, the action | `outcome.kind`, `.action` | |
| Who | builds and tunes, operates, receives | `pipeline.owner`, `operates`, `outcome.consumer` | "not named" when absent |
| Promotion | when autonomy is above notify: from, evidence (rate, window, volume), action consistency, blast radius, reversible, approved by and when, review, disable | `promotion.*` | Mandatory when autonomy is assisted or autonomous |
| Read more | tiered source links | `sources[]` | |
| Delivery state | phase since, ticket | `phase.since`, `backlog_ref` | |
| What it cannot tell you, always | the limits paragraph | `limits` | Never hidden. It is what stops over trust |

## 5. Edit mode

Editable: everything a person authors: title, status, phase and since, covers (scenario and steps, chosen from the library, steps checked against the scenario's attack path), trigger, composes, pipeline, outcome, promotion (required when autonomy is above notify; the form appears when autonomy changes), limits, rationale, operates, backlog reference, sources, notes.

Not editable: id, the derived framework ids, the illustrative flag (cleared by a change set that also replaces the content), provenance dates.

Save: one change set, `POST /use-cases/{id}/changes`, with name and reason. The server validates against the use case schema and the join to the scenario library, and refuses autonomy above notify without a promotion block.

Add: a form with the required fields only (title, covers, trigger, pipeline, outcome, limits). Creates a proposed use case with the next free id through `POST /use-cases`.

## 6. Rules, as acceptance criteria

1. **Given** a use case with autonomy assisted or autonomous, **when** it renders, **then** the promotion section is shown; **when** edited to that autonomy with no promotion block, **then** Save is refused with the server's message.
2. **Given** any use case, **when** it renders, **then** status, autonomy and limits are visible without scrolling past them.
3. **Given** covers naming a step the scenario does not have, **when** saved, **then** the server refuses and the message names the step.
4. **Given** an illustrative record, **when** it renders, **then** the banner is shown.
5. **Given** the derived framework ids, **when** Edit is on, **then** they have no control and are marked derived.

## 7. Data contract

`use_cases[]` as committed, plus `scenarios[]` for titles and steps. Schema: `schema/use-case.schema.json`.

## 8. Done when

- [ ] Every section renders for UC-006 and UC-009 from the examples.
- [ ] Add creates a valid proposed record against the mock server.
- [ ] The five criteria pass.
