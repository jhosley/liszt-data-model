# Decisions and open questions

Two kinds. The first are decisions already taken that the model reflects, recorded so the
reasoning is visible. The second are decisions and design questions still open. A
relational build will encode an answer to each of the open ones whether or not anyone
decides it, so they are listed here to be decided rather than defaulted.

---

## 1. Decisions the model reflects

1. **The environment is a record type.** An environment definition has an id and a version, a run cites it, and the validator checks the run against it. Two runs of one spec against different environment versions are visibly not comparable.
2. **There is no lab distinction in the model.** Runs execute against infrastructure. Whether it is a disposable build or the estate is not encoded. What a run can prove is decided by the telemetry pipeline mode on the environment; what the agent may do is decided by the autonomy rung on the run.
3. **Discovery mode is part of the model.** Agent proposed scores are a separate path that never writes a scenario record directly, and a per row provenance field records whether a person or an agent produced the numbers.
4. **The agentic platform hands over one JSON document per scenario per run.** Its schema is `schema/agent-run-import.schema.json`. The importer writes an immutable run record and nothing else.
5. **`source` is organization scoped.** One estate runs one product and another runs a different one. The full per organization field list is stated once in the overlay schema.
6. **Scenario 021 carries an illustrative reference assessment.** Restored so that one record exercises every path, and labeled as invented in the record itself.
7. **No cross shape figure is reported.** Every scenario names its infrastructure shape, a snapshot reports one organization and one shape, and coverage, exposure and maturity are never blended across shapes. Comparison across shapes is a table of per shape snapshots side by side. Decided 2026-09-14.
8. **Infrastructure is reference data.** The layers, seams and emitted categories of each kind of estate are records under `infrastructure/`, with the AI stack as the catalog's shape and six further shapes carried as proposed. A scenario names its shape, which is the stack scope column. The viewer reads the records rather than carrying its own copy.

## 2. Decisions still open

1. **Rename the layer field or add a parallel one.** With layers held per shape, the scenario's objective layer is a value of its own shape's layer list. Whether the column keeps its current name (`ai_infrastructure_layer`) or is renamed to something shape neutral is a naming decision with a migration cost, not a modeling one.
2. **Whether conditions are a separate concept or an environment with a filter.** Decides whether Attack Step generalizes to failure scenarios or whether they need their own structure.
3. **Whether the autonomy rung names change.** The rungs are lab-only, production-observe, production-active. With the lab distinction gone from the environment, the first rung's name is the only place the word survives. The model treats the rung as an enum whose values can be renamed in one place.
4. **Who owns the framework baseline.** The seat is empty and the validator reports it on every run. The first migration cannot happen until someone is named.

## 3. Design questions a relational build has to answer

- Where should the boundary sit between the canonical model and the workflow views? The viewer's data file (`examples/viewer/liszt-data.json`) is the read model the current application consumes. Which of its computed fields should be views, which materialized, and which belong to the application?
- How is the digest chain preserved in a relational store? Git provides content hashing for free; PostgreSQL does not. A spec carries a digest of its scenario, a prediction a digest of its spec, a run a digest of its prediction, and the scorer refuses a mismatch. Whatever replaces git as notary has to give an equally checkable seal.
- Should the scenario level framework roll-up remain derived, as the model says, or be stored and checked, as the records do today?
- Should every run be immutable history with the record showing current state? Today the scorer writes the scorecard into the run file. The model separates them.
- What is the migration path from the YAML library, and does the repository remain the system of record during and after the transition? The records carry teaching comments that the YAML tooling preserves on rewrite.
- The agent run import arrives as JSON from an orchestrator. Is the import an endpoint, a queue consumer, or a file drop, and where does the refusal logic live so that a bad digest is refused before anything is written?
- Traces stay in the tracing platform and the record carries pointers. Should the pointers be validated against that platform at import time, and what happens when the platform's retention expires?
- The evidence behind a Have must be re-runnable by a third party. Should the model store it as structured (system, query, expected result) rather than free text, so evidence spot audits can be automated?
