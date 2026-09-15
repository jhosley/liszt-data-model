# Screen: Documentation

**Route:** `#/docs`
**One sentence:** four pages, overview, environments, frameworks, how to, with everything derived from records where records exist.
**Reference:** `renderDocs()`, `docOverview()`, `docEnvs()`, `docLayerPage()`, `docEnvPage()`, `docFrameworks()`, `docHow()` in `liszt/tools/build_viewer.py`.

## 1. The four pages

| Page | Shows | From |
|---|---|---|
| Overview | what Liszt is and does, in plain language, with the live counts of scenarios and use cases | `library.records`, `use_cases[]`, fixed text |
| Environments | the infrastructure shapes: for the catalog shape, one card per layer; for proposed shapes, one card per shape marked proposed. A layer page shows what sits here, components, seam tags, why it matters, and the ATT&CK, ATLAS and OWASP ids and scenarios found at that layer. A shape page shows where it runs, owners, layers, seams, what it emits, the gap | `infrastructure[]`; ids and scenarios derived from `scenarios[]` at that layer |
| Frameworks | one page per framework from the baseline: version, cadence, id stability, how it is used here | `frameworks_detail`, `baseline_meta` |
| How to | nine procedures, each collapsible: steps, commands, things to watch | fixed text today; a record type later |

## 2. Rules

1. **Given** a layer page, **when** it renders, **then** the identifiers and scenarios on it are read from the records, never typed.
2. **Given** a proposed shape, **when** it renders, **then** it is marked proposed and the note says nothing is classified against it.
3. **Given** a layer with no scenarios, **when** it renders, **then** it says "None classified at this layer. That is itself a finding rather than proof the layer is unreachable."

## 3. Data contract

`infrastructure[]` (schema `schema/infrastructure-shape.schema.json`), `frameworks_detail`, `baseline_meta`, `scenarios[]`.

## 4. Done when

- [ ] Five layer cards and six shape cards render from the example shapes.
- [ ] The layer page for L3 lists scenario 021.
