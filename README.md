# Liszt data model

This repository documents the Liszt data model: the entities, their relationships and
attributes, the rules the data must obey, and the record types that cross into the system
from outside. It exists so that anyone deciding how to build Liszt on a relational store
can read one place and know what the data is, what is derived from what, and what must
stay true. The application that enforces the model today is included under `liszt/`; the
documents here describe it and copy from it.

## What Liszt is, in one paragraph

Liszt records attack and failure scenarios against AI systems, tests whether their claims
are true, and produces a verdict on whether an attack would be seen. A scenario is three
to six adversary moves. Each move has an evidence row saying what it would make
observable. System owners score each row on two questions, would we see it and does
anything alert on it, and one rule turns the scores into a verdict: Blind, Collectable, or
Have. The verdict is computed, never typed. A second loop seals a prediction, runs the
scenario, and scores the prediction against what was observed, so the library is
calibrated against reality rather than its authors' optimism.

## The model already exists

The model is expressed as thirteen JSON Schemas, enforced by a validator that runs in
continuous integration, and exercised by twenty-one scenarios, twelve use cases, six
incidents, and one scenario carried end to end through validation, rollup, snapshot, test
specification, sealed prediction, scored runs, a discovery run, and an import from the
agentic platform. Moving it to a relational store is a port of something that works, not a
design from nothing.

The scale is small: about a hundred evidence rows. The difficulty is correctness,
derivation and integrity, which columns are generated and which are writable, how a
digest chain survives without git, and how an unscored row stays null rather than zero all
the way to a dashboard.

## Read in this order

| Step | Read | Why |
|---|---|---|
| 1 | [docs/01-data-model.md](docs/01-data-model.md) section 1 | One page on what the system has to do |
| 2 | [docs/01-data-model.md](docs/01-data-model.md) section 2 | The spine: scenario, step, evidence row, assessment, framework references, and the derivation rule |
| 3 | [diagrams/erd-spine.svg](diagrams/erd-spine.svg) | The spine as a diagram, Crow's Foot |
| 4 | [docs/02-entity-list.md](docs/02-entity-list.md) | Every entity, one line each, five families |
| 5 | [docs/01-data-model.md](docs/01-data-model.md) section 3 | The remaining entities, with keys and rules |
| 6 | [diagrams/erd-full.svg](diagrams/erd-full.svg) | The whole model, by family |
| 7 | [docs/03-constraints.md](docs/03-constraints.md) | The rules the data must obey, and what each means for a relational design |
| 8 | [docs/04-open-questions.md](docs/04-open-questions.md) | Decisions the build will encode, and design questions still open |
| 9 | [docs/05-verification-notes.md](docs/05-verification-notes.md) | Where the tools and the documentation disagreed, and how each was resolved |
| 10 | `schema/` and `examples/` | The schemas, and the records that pass them |
| 11 | [frontend/README.md](frontend/README.md) | The front end: screens, models, contract, backlog |

## Layout

```
docs/           the model document, the entity list, the constraints, the open questions,
                the verification notes, and under reference/ the program documents the
                model was derived from (measurement, framework mapping, the viewer
                contract, agent testing, discovery mode, the developer PRD)
schema/         the thirteen JSON Schemas. Every field carries a description
examples/       one worked example of every record type, all for scenario 021:
                the seven infrastructure shapes (the AI stack and six proposed estates),
                the scenario, its test spec and sealed prediction, its discovery spec,
                five run records, two environment definitions, a per organization
                overlay, two incidents, two use cases, the framework baseline and its
                checksums, two agent run imports, a metrics snapshot, the viewer data
                file, and the two record templates with their teaching comments
frameworks/     the framework index: every ATT&CK, ATLAS and OWASP identifier at
                baseline 2026.07 with its status, projected from the pinned artifacts.
                The seed of the Technique Reference, Tactic and Data Component tables
diagrams/       the two entity relationship diagrams, the script that generates them,
                and the two system diagrams
liszt/          the Liszt application: records, schemas, tools, reference page, docs.
                Installable as is; see Installing Liszt below
frontend/       everything a front end developer needs: roles, one file per screen, the
                read and write models, workflows, rules, design tokens, scope tiers, user
                stories with a tracker import file, and the OpenAPI contract
```

## Installing Liszt

The application itself is in `liszt/`: the records, the schemas, the tools, the reference
page, and its own README and documentation. It is the version the model in this repository
describes.

```bash
cd liszt
./install.sh          # a Python 3.11 virtual environment and the pinned dependencies
./liszt validate      # every record of every type, against its schema and the quality bar
./liszt viewer        # builds the reference page and liszt-data.json under build/viewer/
```

`liszt/README.md` and `liszt/docs/TUTORIAL.md` are the starting points for the application.
The pinned framework artifacts that are too large to commit (the ATT&CK bundle, the OWASP
PDFs, the DeTT&CT tree) are fetched by `python3 tools/pin_frameworks.py`; the checksums and
the identifier index are committed, so the validator works without them.

## A note on the examples

Scenario 021 carries an illustrative reference assessment. Its scores, sources, evidence
references, owners and ticket ids are invented, and the record says so in its header and
its notes. They exist so that one record exercises every path. The incident records cite
public disclosures. The environment records and the agent run imports are worked examples
and say so in their first line. Nothing here describes any organization's actual estate.
