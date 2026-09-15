# Screen: Session

**Route:** `#/session`, plus the session bar on every screen while a session is active
**One sentence:** a facilitated scoring meeting: a facilitator's name, the scenario's evidence rows as cards or as a map, a readback, and a submit or export.
**Reference:** `toggleSession()`, `telemetryBlock()` in session mode, `editCard()`, `mapPanel()`, tabletop mode, `renderSession()`, `proposalsPanel()` in `liszt/tools/build_viewer.py`.

Session reuses the Scenario screen's Edit controls for evidence rows. What it adds is the meeting: one name for everything captured, a capture counter, the map view, tabletop mode, proposals, a readback, and one submission at the end.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Facilitator | Run the hour: start the session, walk the rows, read back, submit |
| System owners | Answer the two questions per row, name the source, own the gap, give the ticket |

## 2. What it looks like

```
[Session bar]  Facilitator: ____   Captured: 7 rows on 2 scenarios   [Propose a scenario] [Session] [Leave]

Scenario screen, evidence section replaced by:
  [Score as cards] [Score as map] [Reset captured answers]
  Cards: one per row, two score selects, verdict preview, source, evidence, owner, ticket, notes
  Map:   the attack path as a strip; one step in focus; questions cascade:
         would we see this -> how completely -> where -> does anything alert -> evidence or owner + ticket
         Branch end: "still owes: ..." or "Branch complete, verdict Have"
  Tabletop: the map full screen, projector scale, arrow keys move between steps, Esc exits

Session page:
  Readback: per scenario, per step, "scores unscored to v3 d2, coverage now Have; source ...; owner ..."
  Proposals: new scenarios the room said are missing (title, mode, layer, priority, one liner)
  [Submit session] [Export session file] [Import a session file] [Discard everything]
```

## 3. Behavior

| Behavior | Rule |
|---|---|
| Starting | Sets the facilitator's name. Everything captured from then on is attributed to it |
| Capture | Held locally until submitted. A page reload keeps it. Leaving the session loses nothing |
| Half a score pair | A row with only one of the two scores stays Unscored; the picked value is held until the other arrives. The map's "no" path commits both numbers at once so a branch can never strand half a pair |
| We don't know | A real answer. The row stays Unscored and is flagged needs research with an owner. The flag clears when the row is scored |
| Reset captured answers | Clears one scenario's capture only, after confirmation |
| Readback | Read aloud at the end. Every owner confirms their gap; every ticket is checked while the room is together |
| Submit | One change set per scenario, all under the facilitator's name, the reason "scoring session <date>", through the same endpoint as Edit. The server applies them and answers with findings per scenario |
| Export and import | The session file, for a room with no connection. Applied later by a person through the tools or through the import endpoint |
| Organization | A session is for one organization. The page says which. Captures write to that organization's assessment |

## 4. Rules, as acceptance criteria

1. **Given** only one of the two scores is picked, **when** the row renders, **then** it is Unscored and the picked value is still shown.
2. **Given** the map's "would we see it: no" path, **when** taken, **then** visibility 0 and detection minus 1 are committed together.
3. **Given** a Have with no source or no evidence, **when** the branch ends, **then** "still owes" names what is missing.
4. **Given** a submit, **when** the server answers, **then** findings are shown per scenario and per row, and nothing is marked applied until the server says so.
5. **Given** a reload mid session, **when** the page returns, **then** every capture is still there.
6. **Given** tabletop mode, **when** active, **then** arrow keys move focus and Esc exits, and captures land in the same place as the cards.

## 5. Data contract

Writes: `POST /sessions` with a session file body (`liszt/docs/07-viewer-data-contract.md` section 4b); or per scenario `POST /scenarios/{id}/changes`. Reads: the same as the Scenario screen.

## 6. Done when

- [ ] Cards and map produce identical captures for the same answers.
- [ ] The six criteria pass.
- [ ] A submitted session against the mock server returns findings and the screen shows them.
