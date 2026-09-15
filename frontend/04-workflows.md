# Workflows

Each is the sequence of screens and change sets for one job, start to finish.

## 1. Score a scenario in a meeting

1. Facilitator opens the Scenario screen, starts a Session, enters their name, selects the organization.
2. For each evidence row, cards or map: would we see it, does anything alert on it, where exactly, evidence for a Have, owner and ticket for a gap. "We don't know" leaves the row Unscored and flagged.
3. Session page: readback aloud. Every owner confirms their gap; every ticket is checked.
4. Submit session. Server applies one scenario change per scenario under the facilitator's name and returns findings.
5. The Scenario screen shows the new verdicts. Coverage shows the new numbers.

Doctrine it depends on: coverage computed never typed; unscored is absent; nothing writes itself back.

## 2. Edit a scenario at a desk

1. Scenario screen, Edit. Change authored fields or assessment rows.
2. Save: reason, and a ticket if a score changed. Findings shown by field; fix and save again.
3. Read mode shows the server's version.

## 3. Publish a scenario

1. Author finishes the record and every row is scored. Readiness on Scenario management shows the scoring path open.
2. A different person reviews on the Scenario screen and presses Publish with their name.
3. Server refuses if reviewer equals author or if any error or warning remains; otherwise sets published and the review date.

## 4. Bring in a scenario from research

1. Bring in a scenario: copy a research prompt, run it outside the application, paste the answer into Convert.
2. The pane checks the answer and flags what it could not resolve.
3. Paste and add: the server assigns an id and creates a draft with the flags attached.
4. The analyst works the draft on the Scenario screen. Workflow 2, then 3.

## 5. Test a scenario's claims

1. Scenario management, Readiness: the scoring path is open for a published, fully scored scenario.
2. The engineer emits the spec and the sealed prediction and commits the prediction (today by tool; later a button that calls the same tool).
3. The run executes, by a person or by the agentic platform. The platform's document arrives through the import endpoint and becomes a run record.
4. Run and rescore: the scorecard. Proposed rescores are accepted or rejected one at a time, each an attributed change with the run id as ticket.
5. Coverage reflects accepted rescores; the next snapshot lists them as rescores.

Doctrine: predictions sealed before the run; the environment decides what a run can prove; a run is immutable.

## 6. Get first scores from discovery

1. Readiness: the discovery path is open for an unscored draft.
2. The engineer emits the discovery spec; the platform runs it; the import creates a discovery run.
3. Run and rescore: each proposed score is accepted or rejected. Accepted ones land marked agent proposed and count nowhere.
4. A person reviews the evidence and sets provenance to human on the Scenario screen in Edit, which is a change with a reason. Now they count.

## 7. Read the numbers

1. Coverage: per scenario and aggregate, with completeness beside every figure, organization and shape in the header.
2. Reports: posture, scoreboard, movement, from snapshots. Rescores listed separately from improvements.

## 8. Migrate the framework baseline (administrator, later tier)

1. Administration, baseline: cut a new baseline, pin and index the artifacts, migrate identifiers, dual report for one cycle, switch.
2. Every screen that shows an identifier shows which baseline it speaks throughout.
