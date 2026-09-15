# Scope, in four tiers

Build in this order. Each tier is usable on its own and is an epic in the tracker.

| Tier | Name | What it delivers | Screens | Writes |
|---|---|---|---|---|
| 1 | Read the library | Everything the read model carries, exactly as the reference page shows it | Scenario (read), Coverage, Use cases (read), Frameworks, Documentation, Reports (from snapshots) | none |
| 2 | Change a record | Edit mode on Scenario and Use cases; Publish and Retire; Session with submit; intake | Scenario (edit), Use cases (edit, add), Session, Bring in a scenario | scenario change, new scenario, publish, retire, use case change, new use case, session |
| 3 | Test and calibrate | Readiness, the testing chain, scorecards, rescore acceptance, agent imports, discovery acceptance | Scenario management | accept and reject rescore, agent run import |
| 4 | Administer | Organizations, environments, shapes, baseline status | Administration | environment, shape, organization, baseline owner |

## What tier 1 needs from the back end

Only the read endpoints, and they can be a static file to begin with: `liszt-data.json`
served as is, with `org`, `shape` and `drafts` selecting between pre-built files. That is how
the reference page works today and it is enough to build and demonstrate the whole read
side.

## What tier 2 needs

The change set endpoints and the validator behind them. The validator exists; the endpoint
wraps it.

## Out of scope for the first build

Cutting a new framework baseline from the interface; emitting a spec from the interface;
executing a run from the interface. All three stay as tools until the workflows have run
by hand a few times.
