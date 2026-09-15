# Screen: Frameworks

**Route:** `#/frameworks`
**One sentence:** the pinned baseline, and for each framework, every identifier the library uses and which scenarios use it.
**Reference:** `renderFrameworks()` in `liszt/tools/build_viewer.py`.

## 1. Who uses it

| Person | Comes here to |
|---|---|
| Analyst | Check an identifier is in the baseline before mapping to it; see where it is already used |
| Reader | Answer "do we cover technique T1190" by following the identifier to its scenarios |

## 2. Sections

| Section | Shows | From | Rule |
|---|---|---|---|
| Baseline, always | baseline name; ATT&CK version and spec version; ATLAS content and format version; both OWASP editions; DeTT&CT version | `baseline.*` | Shown wherever identifiers are shown. Identifiers are not comparable across baselines |
| One panel per framework | count of identifiers used; per identifier: chip, name (for OWASP slots; for ATT&CK and ATLAS from the index), the list of scenarios using it, linked | `frameworks{}` reverse index, `owasp_names`, and the framework index for names and status | An identifier that is revoked or deprecated in the index is marked |
| Reliability note, always | there is no authoritative crosswalk between OWASP and either MITRE framework; every cross framework mapping is the program's editorial judgment | fixed text | Mandatory |

## 3. States

Empty framework panel: omitted. A baseline with no index: the identifier names are absent and a note says the index has not been built.

## 4. Rules

1. **Given** any identifier, **when** it renders, **then** the baseline it speaks is visible on the page.
2. **Given** an identifier marked revoked in the index, **when** it renders, **then** it is marked and the replacement is named.
3. **Given** the page, **when** it renders, **then** the reliability note is present.

## 5. Data contract

`baseline.*`, `frameworks{attack,atlas,owasp_llm,owasp_agentic}` (identifier to scenario ids), `owasp_names{}`, and `GET /frameworks/index` for names and status.

## 6. Done when

- [ ] Matches the reference page for the drafts build.
- [ ] Revoked and deprecated identifiers are marked when present.
