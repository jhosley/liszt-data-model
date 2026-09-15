# Constraints the data model must satisfy

These are the rules the data must obey for the result to still be Liszt. They come from two
program documents: the doctrine from the program primer, and the invariants from the
developer product requirements (`docs/reference/Liszt-PRD-Developer.md`, section 4). The
doctrine is the short form. The invariants are the same rules stated for an engineer, each
with why it exists and what breaks if it is violated. The last section says what each means
for a relational design.

---

## The doctrine, eight points

1. Coverage is computed from scores, never typed by anyone.
2. Nothing writes itself back. Every change to a record is applied by a person, with
   attribution and a ticket reference. Model output is always a proposal.
3. An author cannot publish their own record; an independent reviewer is required.
4. Test predictions are sealed before the run; the scorer refuses to score if the
   prediction moved afterward.
5. An unscored row is absent, never zero, and is never averaged in.
6. The environment decides what a test can prove; only the lab rung of the autonomy ladder
   is enabled, and the executor refuses anything above it.
7. Per organization coverage lives in overlays, so the shared scenario library stays
   publishable while each organization's gaps stay private.
8. Framework identifiers are pinned to a named baseline and never mixed across baselines.

---

## The twelve invariants, from the developer product requirements

Each invariant states the rule, why it exists, and what breaks if a production design violates it.

**I-1. Coverage is computed, never typed.** The Have, Collectable, Blind tag is derived from two scores by one rule in one place, and every stored tag is a cache that the validator recomputes and errors on. Why: this is the product's core claim, the difference between an evidence-backed determination and analyst optimism with a number attached. What breaks: any UI with an editable coverage dropdown, any second implementation of the rule that can drift, any import path that trusts an incoming tag. The production system must keep exactly one implementation of the derivation and route every consumer through it or its output.

**I-2. Nothing writes itself back. A human applies every change, with attribution and a backlog reference.** The viewer captures edits in the browser session only; the session file is applied by a tool while a person reads the diff; the run scorer emits proposals, never edits; the conversion prompt emits a draft the importer re-checks. Why: the records get quoted to auditors and boards, and every change must have a person who stands behind it and a ticket that explains it. What breaks: any "sync" feature, any model output that lands directly in a record, any bulk update without per-change attribution. In production, "a human applies" may become "a human approves a change set in a governed workflow," but the approval must be per change set, attributable, and produce the same review artifacts.

**I-3. An author cannot publish their own record; an independent reviewer is required.** `reviewed_by` must exist and differ from `authored_by` before status may become published; the validator errors when they match. Why: independence is the only real control over content quality; the validator checks structure and arithmetic, not truth. What breaks: role models that let one identity hold both ends, bulk publish operations, any workflow where review is a checkbox the author sets.

**I-4. Predictions are sealed before runs.** The prediction is a separate artifact, committed before execution and bound by digest; the scorer refuses a moved digest; observations are authored before the prediction is opened. Why: an editable prediction measures hindsight, and the calibration loop is the product of the testing phase. What breaks: storing predictions and observations as mutable rows in one table with no tamper evidence. Production may replace git as notary, but only with something that gives an equally checkable seal.

**I-5. Unscored is absent, never zero.** A row without scores has no coverage value, is excluded from every numerator and denominator, and pushes its scenario out of maturity reporting; every published figure carries its completeness companion. Why: scoring nothing and scoring badly must never produce the same number; treating unknown as zero manufactures precision, sells the same improvement twice, and hides orphans. What breaks: any aggregation layer, BI export, or dashboard that defaults nulls to zero. This is the invariant most likely to be violated accidentally by a reporting stack.

**I-6. The environment decides what a run can prove.** The pipeline mode recorded on the run, not the spec's request and not anyone's intent, gates which claims are scoreable; a detection claim in a scratch lab is unscoreable, not failed and not passed. Why: a cheap lab producing a confident detection verdict is a wrong number wearing a lab coat. What breaks: schemas or scorers that collapse "unscoreable" into "absent," or reporting that quotes a scratch run as a detection test.

**I-7. The autonomy ladder is enforced by refusal.** Rungs are lab-only, production-observe, production-active. Only lab-only is enabled; the production rungs are fully specified and switched off; the executor must refuse anything above the enabled rung even when a spec asks. Promotion moves one rung at a time with measured evidence, a named approver, a review loop, and an off switch, on both the test loop and the use case ladder (notify, assisted, autonomous). Why: this is what makes a production rung approvable later, and it is the record that gets pulled the day an automated action misbehaves. What breaks: configuration flags that let an operator skip a rung, or promotion blocks filled retroactively.

**I-8. Org overlays keep the library publishable.** The shared record carries everything org independent; coverage lives per org in overlays; there is no cross-org aggregate coverage number because there is no such estate. Why: adopting the library must cost a team nothing politically; coupling adoption to gap disclosure kills adoption. What breaks: multi-tenant designs that store scores on the shared record, or any rollup that averages across orgs.

**I-9. Framework identifiers are pinned to a named baseline, edition qualified, never mixed.** Every record names exactly one baseline; OWASP IDs always carry their edition; migration is deliberate, with a dual report cycle; tactic-level metrics across the ATT&CK v19 split are flagged non-comparable. Why: without pinning, a coverage trend line measures MITRE's release schedule. What breaks: storing bare IDs, auto-updating framework data, or letting two baselines coexist inside one record or one snapshot.

**I-10. Evidence must be re-runnable by a third party.** A Have claim is backed by an artifact someone else can execute: a saved search that returns rows, a rule id, a ticket. "We have EDR" is not evidence; stale evidence downgrades the row rather than being refreshed with an excuse. Why: an unverified Have is worse than a Blind, because it removes the gap from the backlog without closing it. What breaks: evidence as free text nobody audits; production should make evidence a first class, spot-auditable reference.

**I-11. Specs carry no payloads and bind by technique id.** The test spec is an abstract, engine agnostic action set; an adapter resolves technique ids to a published emulation library at run time; no exploit code anywhere in the records or generated material. Why: an abstract spec is the only form reviewable for safety before a tool is chosen, and specs outlive runners. What breaks: embedding runner commands or payloads in specs, or coupling the spec format to one vendor's test library.

**I-12. Model output is always a proposal; machine checkable facts are recomputed by tooling and never trusted from a model.** The conversion prompt runs three self checks, and the importer re-checks everything mechanically anyway; the readiness prompt's judgment JSON supplements, never replaces, the mechanical gate; no metric is ever produced by asking a model to count. Why: a model's count is plausible and uncheckable; the program's credibility rests on every number being reproducible by a script. What breaks: shipping model-derived fields without a deterministic re-check, or any metric path with a probabilistic step in it.

---

## What these mean for a relational design, in one paragraph each

**Generated columns are not writable.** Doctrine 1 and invariant I-1. The coverage tag is a derived column or a view over the two scores, and the derivation exists once. No interface offers a coverage dropdown.

**Every write is a person's act with a reason.** Doctrine 2 and invariant I-2. Model output, scorer output and agent proposals land in their own tables with a status, never as updates to a scenario's row. The application applies a change set on a person's behalf, attributed, with a backlog reference.

**Reviewer differs from author, enforced.** Doctrine 3 and invariant I-3. A check constraint or a trigger, not a convention.

**The digest chain is preserved on purpose.** Doctrine 4 and invariant I-4. Git supplies content hashing for free; PostgreSQL does not. Specs, predictions and runs carry digests of what they were derived from and bound to, and the scorer refuses a mismatch. Whatever replaces git as notary has to give an equally checkable seal.

**Unscored is null, never zero.** Doctrine 5 and invariant I-5. Every aggregate excludes nulls and reports its completeness companion. This is the invariant a reporting layer breaks by accident.

**The pipeline mode gates what may be scored.** Doctrine 6 and invariant I-6. Recorded on the run, read by the scorer.

**The autonomy ladder is enforced by refusal.** Invariant I-7. Rung and promotion are data the executor reads, not configuration an operator flips.

**Coverage is per organization and per infrastructure shape.** Doctrine 7 and invariant I-8. The shared row and the per organization assessment are two tables. There is no cross organization aggregate, and no cross shape aggregate: a snapshot reports one organization and one shape.

**Framework ids carry their baseline.** Doctrine 8 and invariant I-9. Every technique reference is keyed by baseline as well as id, and OWASP ids carry their edition.

**Evidence is a re-runnable reference.** Invariant I-10. A first class, spot auditable field, not free text nobody reads.

**Specs carry no payloads.** Invariant I-11. Technique ids, resolved by an adapter at run time.

**Machine checkable facts are recomputed.** Invariant I-12. No metric path has a probabilistic step.
