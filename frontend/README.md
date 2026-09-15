# Liszt front end

This folder is everything a front end developer needs to scope and build the Liszt web
application. It is written to be read in order, top to bottom, in about an hour.

## The one idea

The application shows records and captures changes to them. It never owns the data. Every
number on a screen was computed by the back end from the records, and every edit a person
makes becomes a **change set** that carries the person's name and reason and is applied by
the back end under the same rules the validator enforces today. The screen has no
calculation of its own and no direct write. If a design remembers only this, it will be
right.

## Two modes on every screen that shows a record

- **Read.** The default. Everything visible, nothing editable.
- **Edit.** A toggle in the page header, available to any signed in person, no session
  needed. Fields that people author become editable. Fields that tools derive stay read
  only and are marked as such. Save submits one change set and the server answers with
  either the new version or the validator's messages, shown next to the fields they concern.

**Session** is a third thing, not a mode: a facilitated scoring meeting with a facilitator's
name, a readback, and an export. It uses the same edit controls and produces the same
change sets, bundled. It is its own screen.

## Read in this order

| # | File | What it gives you |
|---|---|---|
| 1 | [00-roles-and-jobs.md](00-roles-and-jobs.md) | Who uses the application and what each person comes to do |
| 2 | [screens/](screens/) | One file per screen: what it shows, what it reads, what it writes, its states, its rules. Start with `scenario.md` |
| 3 | [02-read-model.md](02-read-model.md) | The data the screens read, endpoint by endpoint |
| 4 | [03-write-model.md](03-write-model.md) | The change sets the screens submit, one by one |
| 5 | [04-workflows.md](04-workflows.md) | The end to end sequences: scoring, publishing, testing, importing |
| 6 | [05-rules.md](05-rules.md) | The rules the interface must not break, each with why |
| 7 | [06-design-tokens.md](06-design-tokens.md) | Colors, type, the reusable components |
| 8 | [07-scope-tiers.md](07-scope-tiers.md) | Four tiers to build in, so it can be estimated and phased |
| 9 | [08-user-stories.md](08-user-stories.md) and [stories.csv](stories.csv) | The backlog with acceptance criteria; the CSV imports into Jira |
| 10 | [openapi.yaml](openapi.yaml) | The API contract the front end and back end both build to |

## What to build against

Build against `openapi.yaml`. Its response examples are the real data file the current build
produces (`../examples/viewer/liszt-data.json`), so a mock server can be generated from it on
day one and the screens built before the database exists. Its request bodies are the JSON
Schemas under `../schema/`. The back end team implements the same contract over the
database the data model describes.

## Where the working version is

Every screen already exists, working, in the reference page: build it with `./liszt viewer`
inside `../liszt/` and open `build/viewer/liszt-viewer.html`. Match its behavior. The look
is yours to redesign.

## Definition of done, for the whole application

- Every acceptance criterion in `08-user-stories.md` passes.
- For any record, the application shows the same numbers as `liszt-data.json`.
- No screen computes a coverage tag, a roll-up, or a metric.
- No screen writes to a record except through a change set with a name on it.
