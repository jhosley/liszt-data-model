# Screen: Bring in a scenario

**Route:** `#/intake`
**One sentence:** three panes that take a scenario from research to a draft record: a research prompt library, a conversion pane that turns a model's answer into a record, and paste and add.
**Reference:** `intakePanel()` and the `P_*` prompt constants in `liszt/tools/build_viewer.py`.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Analyst | Start a new scenario from an incident or a research finding without hand writing YAML |
| Threat modeler | Propose a hypothesis scenario |

## 2. The three panes

| Pane | What it does | Writes |
|---|---|---|
| Research library | Three research prompts (incident, research, hypothesis), each shown as a one line summary with Read and Copy. A person runs one in their model of choice outside the application | nothing |
| Convert to JSON | The conversion prompt, with the incident or hypothesis switch. The person pastes the model's JSON answer. The pane runs the self checks: the seam tag lands on the chain, three to six steps, the branch fields, source tiers on the schema scale ("0", "1", "2"), framework ids shaped correctly. Anything unreadable is flagged for review, never guessed | nothing until the person adds it |
| Paste and add | The checked JSON becomes a draft scenario proposal, with the next free id, and every review flag attached | `POST /scenarios` as a proposal with `needs_review[]` |

## 3. Rules

1. **Given** a converted scenario with a canonical layer string in a step tag, **when** checked, **then** it is shortened to fit and flagged for rewriting as a seam tag.
2. **Given** more than six steps, **when** checked, **then** the extra steps are dropped, the drop is flagged loudly, and the rest are renumbered.
3. **Given** a source tier the pane cannot read, **when** checked, **then** it lands as "2" with a review note, never guessed upward.
4. **Given** an unresolved layer, **when** added, **then** the layer is left empty and flagged, because a guessed layer is indistinguishable from a real one.
5. **Given** any imported record, **when** it lands, **then** it is a draft with `needs_review` attached and its origin recorded.

## 4. Data contract

`POST /scenarios` with a draft scenario body; the server assigns the id, keeps the template's teaching comments, sets status draft, and returns the validator's findings.

## 5. Done when

- [ ] The three prompts are readable and copyable.
- [ ] A pasted sample converts, is checked, and lands as a draft against the mock server with its flags.
