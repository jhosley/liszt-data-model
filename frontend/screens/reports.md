# Screen: Reports

**Route:** `#/reports`
**One sentence:** the leadership views, built from snapshots: posture, scoreboard, kill chain map, stack layers, movement.
**Reference:** `renderReports()` in `liszt/tools/build_viewer.py`. **Caution:** the reference page's reports are an illustrative mock with invented figures. Build the layouts from it; build the numbers from snapshots.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Leadership, risk | See where the program stands, what moved since last period, and why |
| Program office | See maturity and whether movement was real or a restatement |

## 2. The five reports

| Report | Shows | From |
|---|---|---|
| Posture | tiles: coverage at Have, scenarios, scored moves, Blind moves, use cases; each with the change since the prior snapshot | current and prior `snapshot.metrics`, `snapshot.library` |
| Scoreboard | the trend of Have over snapshots, with a restated bar when a baseline migration happened, both positions kept | `snapshots[]` for one org and one shape, `non_comparable_with` |
| Kill chain map | the attack path positions across scenarios, which steps are Blind at which position | `scenarios[].telemetry[].coverage` by step |
| Stack layers | coverage by infrastructure layer of the shape | `scenarios[].classification.ai_infrastructure_layer`, `counts` |
| Movement | what moved since the prior snapshot, attributed: instrumentation built, techniques the new release added, net restatement; and the anti drift ledgers: retired, added, rescored | `snapshot.library.retired_this_period`, `.ids_added_this_period`, `.ids_rescored_this_period` |

## 3. Rules

1. **Given** any figure, **when** it renders, **then** the organization, the shape, the baseline and the snapshot id are visible.
2. **Given** a prior snapshot with a different baseline, **when** a delta renders, **then** it is marked non comparable and both positions are shown.
3. **Given** `ids_rescored_this_period` is non empty, **when** Movement renders, **then** the rescores are listed separately from improvements and never folded into them.
4. **Given** no snapshot exists, **when** the screen renders, **then** it says so and shows no figures.
5. **Given** two shapes with snapshots, **when** any report renders, **then** it is for one selected shape; there is no combined view.

## 4. Data contract

`GET /snapshots?org=&shape=` list; `GET /snapshots/{id}`. Schema: `schema/snapshot.schema.json`. Example: `examples/snapshot/`.

## 5. Done when

- [ ] Every report renders from the example snapshot with the library at one published scenario.
- [ ] The five criteria pass.
