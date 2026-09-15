# Screen: Coverage

**Route:** `#/coverage`
**One sentence:** the three numbers for the library, coverage, exposure and maturity, per scenario and in aggregate, always with their completeness companion.
**Reference:** `renderCoverage()` in `liszt/tools/build_viewer.py`.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Detection engineer | See the work queue: Collectable rows are cheap wins, Blind rows are instrumentation asks |
| Reader, risk | See which urgent scenarios still have a Blind step, and which gaps have no owner |
| Program office | See maturity: is the process working, not is the news good |

## 2. What it looks like

```
+-------------------------------------------------------------------+
| Organization: reference assessment   Shape: SHAPE-AI   Drafts: no |
| Filters (same as the scenario list)                               |
+-------------------------------------------------------------------+
| Coverage by scenario                      [Show as table]         |
|   021  Agent sandbox escape ...  [=====Have==|=Coll=|Blind]  50%  |
|   001  ...                        not scored                  n/a |
| Legend: Have  Collectable  Blind  Unscored (color and word)       |
+-------------------------------------------------------------------+
| Exposure: NOW scenarios with a Blind step                          |
|   021 ... blind at step 1                                          |
+-------------------------------------------------------------------+
| Unowned gaps: Blind or Collectable rows with no owner              |
+-------------------------------------------------------------------+
| How these are calculated (the rule, in words)                      |
+-------------------------------------------------------------------+
```

Read only. Nothing on this screen is editable in any mode.

## 3. Sections

| Section | Shows | From | Rule |
|---|---|---|---|
| Header, always | organization, infrastructure shape, whether drafts are included | `view.org`, `view.shape`, `view.includes_drafts` | All three always visible. A figure without them is a number people act on wrongly |
| Coverage by scenario | one row per scenario, sorted by Have share descending then id: id, title, verdict bar, Have share or "n/a" | `scenarios[].counts`, `.metrics.have` | Unscored scenarios show a gray bar and "n/a". Never 0% |
| Table view | id, title, priority, scored of rows, Have, Collectable, Blind, maturity score | `metrics.scored`, `.rows`, `.have`, `.collectable`, `.blind`, `.maturity.score` | "Scored" is the completeness companion and must sit next to the percentages |
| Exposure | NOW priority scenarios with at least one Blind step, with the step numbers | `metrics.exposed`, `.blind_steps` | Empty state: "No NOW priority scenario has a Blind step in this view." |
| Unowned gaps | scenarios with Blind rows that have no owner, with the step numbers | `metrics.orphaned_gaps` | Empty state: "Every gap in this view has an owner." |
| How these are calculated, always | the derivation rule in words, and "Mean Have is taken across the n scored scenarios only" | `library.scored` | The sentence with the count is mandatory |

## 4. Aggregate figures

Shown above the per scenario list, from `library`:

| Figure | From | Companion that must sit beside it |
|---|---|---|
| Mean Have | `library.mean_have` (null when nothing scored) | `library.scored` of `library.records` |
| Exposed | `library.exposed` | count of NOW scenarios |
| Fully mature | `library.full_maturity` | `library.scored` |

When `mean_have` is null the tile reads "nothing scored yet", not 0%.

## 5. States

| State | What the screen does |
|---|---|
| Nothing scored in the library | Bars are all gray, every share is n/a, the aggregate tiles read "nothing scored yet", the exposure and gaps panels show their empty states |
| Organization view | Header names the organization. Rows the organization has not assessed are Unscored, even where the reference record has scores |
| Filters exclude everything | "No scenario matches these filters." |

## 6. Rules, as acceptance criteria

1. **Given** a scenario with no scored rows, **when** the list renders, **then** its Have share reads "n/a" and it is absent from the mean.
2. **Given** any percentage on this screen, **when** it renders, **then** its completeness companion (scored of rows, or scored scenarios of total) is visible beside it.
3. **Given** the page, **when** it renders, **then** organization, shape and drafts flag are visible in the header.
4. **Given** `library.mean_have` is null, **when** the tile renders, **then** it reads "nothing scored yet".
5. **Given** any verdict in a bar, **when** it renders, **then** the legend pairs each color with its word.
6. **Given** two shapes exist, **when** figures render, **then** they are for one shape and the shape is named; no figure combines shapes.

## 7. Data contract

```
view.org, view.shape, view.includes_drafts
library.records, .published, .scored, .unscored_ids[], .mean_have, .exposed, .full_maturity
scenarios[].id, .title, .classification.priority, .counts, .metrics.*
```

## 8. Done when

- [ ] Matches the reference page for the published-only build (one scenario, 021) and the drafts build (21 scenarios, nothing scored).
- [ ] Table and chart views show the same numbers.
- [ ] The six criteria pass.
