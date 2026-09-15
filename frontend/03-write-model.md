# The write model

This page is how every screen in the application saves anything. There is one way, and
every screen uses it.

1. A screen never writes to a record directly. When a person saves, the screen sends the
   back end a change set: who made the change, why, and what changed.
2. The back end checks the change set against the same rules the validator enforces today,
   recomputes every derived value, and either applies all of it or none of it.
3. The back end answers with either the new version of the record, which the screen then
   shows, or a list of findings, which the screen shows next to the fields they name.
   Errors block the save; warnings do not.
4. Some fields can never be in a change set because a tool derives them: the verdict, the
   counts, the roll-up, readiness. The back end refuses a change set that contains one.

The reason is the doctrine that nothing writes itself back. A tool, a scorer, or an agent
can propose; only a person, with a name and a reason, applies. Building it this way is what
keeps every change attributable after the fact.

The companion page, `02-read-model.md`, is the same idea for reading.

---

Every write is a change set: a document that says who, why, and what, applied by the server
under the same rules the validator enforces. The server recomputes every derived value and
answers with either the new version of the record or a list of findings. Nothing is applied
partially. The screen never writes a field directly.

## The envelope every change set carries

```json
{
  "author": "the signed in person, set by the server from the session",
  "reason": "required, free text, why this change",
  "backlog_ref": "optional; required when a score on an already scored row changed",
  "base_version": "the record version the change was made from; refused if it moved"
}
```

## The change sets

| Change set | Endpoint | Body | The server |
|---|---|---|---|
| Scenario change | `POST /scenarios/{id}/changes` | envelope + `record` (a partial scenario, authored fields only) + `assessment` (`org`, rows keyed by step with the org scoped fields) | validates the whole record against `schema/scenario.schema.json` and the quality bar, and the assessment against `schema/coverage-overlay.schema.json`; recomputes coverage tags; refuses derived fields in the body; returns findings or the new version |
| New scenario | `POST /scenarios` | envelope + a draft scenario (from intake, or the five field proposal: title, mode, layer, priority, one liner) | assigns the next free id, sets status draft, keeps `needs_review`, returns the record and findings |
| Publish | `POST /scenarios/{id}/publish` | envelope + `reviewed_by` | refuses when reviewer equals author; runs the strict gate (zero errors, zero warnings); sets status and review date |
| Retire | `POST /scenarios/{id}/retire` | envelope + `reason` + optional `superseded_by` | sets status retired; the record stays forever |
| Use case change | `POST /use-cases/{id}/changes` | envelope + a partial use case | validates against `schema/use-case.schema.json` and the join; refuses autonomy above notify without promotion |
| New use case | `POST /use-cases` | envelope + the required fields | assigns UC id, status proposed |
| Session | `POST /sessions` | a session file (`liszt/docs/07-viewer-data-contract.md` 4b) with the facilitator as author | applies as one scenario change per scenario, for the session's organization; returns findings per scenario |
| Accept a rescore | `POST /runs/{run}/rescores/{n}/accept` | envelope, with `backlog_ref` set to the run id by the server | applies one assessment change; marks the proposal accepted |
| Reject a rescore | `POST /runs/{run}/rescores/{n}/reject` | envelope | marks the proposal rejected with the reason |
| Agent run import | `POST /runs/imports` | an agent run import (`schema/agent-run-import.schema.json`); author is the platform's service identity | validates; refuses a moved digest, an unknown environment, a disagreeing pipeline; writes one immutable run record; nothing else. Then scores it (test mode) |
| Environment | `POST /environments` | envelope + an environment definition | creates a new version; never edits an old one |
| Shape | `POST /infrastructure/{id}/changes` | envelope + a partial shape | for the catalog shape, seams and categories only |
| Organization | `POST /organizations` | envelope + id and name | |
| Baseline | `POST /frameworks/baseline/changes` | envelope + owner, review due | cutting a new baseline is the migration procedure, out of scope for the first build |

## What a refusal looks like

```json
{
  "applied": false,
  "findings": [
    {"level": "error", "where": "telemetry[2]", "message": "coverage is 'Have' but DeTT&CT scores derive 'Collectable' (visibility=2, detection=0)"},
    {"level": "warn",  "where": "provenance.sources", "message": "no Tier 0 primary source"}
  ]
}
```

`where` is the path the validator uses today. The screen maps it to a field and shows the
message there. Errors block; warnings do not. The messages are written to be read by people;
show them verbatim.

## What a success looks like

```json
{ "applied": true, "version": "<new digest>", "record": { ... the full record, recomputed ... }, "findings": [ ...warnings, if any... ] }
```

The screen replaces what it shows with `record`. It does not merge.

## Rules

1. A body that contains a derived field (coverage, counts, metrics, roll-up, readiness) is refused. The screen must not send them.
2. A body without `reason` is refused.
3. A score change on a row that already had scores, with no `backlog_ref`, is refused with the message "a score change without a ticket is a rescore".
4. `base_version` that does not match the current record is refused with a conflict; the screen reloads and keeps the person's edits.
5. Agent proposed scores never arrive through a scenario change. They arrive through an import, are reviewed on the Scenario management screen, and are accepted one by one.
