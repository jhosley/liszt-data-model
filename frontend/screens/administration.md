# Screen: Administration

**Route:** `#/admin`
**One sentence:** the reference data an administrator maintains: organizations, environments, infrastructure shapes, the framework baseline.
**Reference:** none. The reference page has no administration screen; these are edited as files today. Build from the schemas.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Administrator | Add an organization; define or version an environment; maintain a shape's layers, seams and emitted categories; see the baseline and its pin status; start a migration |

## 2. The four panels

| Panel | Shows | Edit |
|---|---|---|
| Organizations | id, name, count of scenarios assessed | Add. Never delete; an organization with assessments is retired |
| Environments | id, version, name, shape, lifetime, pipeline mode, status, targets, components, teardown, known deviations; the runs that cite each version | Edit creates a new version; the old one is never changed. Schema `schema/environment.schema.json` |
| Infrastructure shapes | id, family, status, layers with their text, seams with their layer, emitted categories | Edit for proposed shapes; for the catalog shape, seam and category additions only, because the layers are the vocabulary every record speaks. Schema `schema/infrastructure-shape.schema.json` |
| Framework baseline | baseline, status, owner (with a warning while unassigned), review due, per framework versions, pin status (which artifacts are vendored and checksummed, whether the index is built) | Owner and review date. Cutting a new baseline is a guided procedure, not a form: it follows the migration checklist and reports each step |

## 3. Rules

1. **Given** an environment edit, **when** saved, **then** a new version is created and every run keeps citing the version it ran in.
2. **Given** the catalog shape's layers, **when** Edit is on, **then** they have no control.
3. **Given** the baseline owner reads UNASSIGNED, **when** the panel renders, **then** a warning says the first migration cannot happen until someone is named.
4. **Given** a delete, **when** attempted on anything cited by a record, **then** it is refused.

## 4. Done when

- [ ] The two example environments and seven shapes render and validate through the mock server on edit.
- [ ] The baseline panel shows the pin status from the checksum lock.
