# Design tokens and components

The reference page is the behavioral specification, not the visual one. Redesign the look
freely. Keep the tokens below, because they carry meaning that the rules depend on.

## Color

| Token | Hex | Use |
|---|---|---|
| `verdict.have` | `#1E7F4B` | Have chip, bar segment, dot |
| `verdict.collectable` | `#B5852B` | Collectable |
| `verdict.blind` | `#B0463B` | Blind |
| `verdict.unscored` | `#9AA7B1` | Unscored, not scored, n/a |
| `ink` | `#1F2D38` | text |
| `ink.muted` | `#5B6B78` | secondary text |
| `accent` | `#2C6E8F` | links, primary actions, reference family |
| `rule` | `#D4D9DE` | borders |
| `surface.pale` | `#EFF2F5` | panels |
| `warn.bg` / `warn.border` | `#FAF3E2` / `#B5852B` | editorial mapping caveat, illustrative banner |
| `danger` | `#B0463B` | destructive actions, blocking findings |

The four verdict colors were validated for contrast and color vision separation on a white
surface. Do not replace them. Every use of a verdict color is paired with its word.

## Type

Sans: Calibri, Segoe UI, Helvetica, Arial. Mono: Consolas, Menlo, for identifiers, file
names and sources. Body 14 to 15 px; tables 12.5 to 13 px; chips 10.5 to 11 px uppercase
with letter spacing. Headings in a serif (Cambria, Georgia) are optional and match the
program's diagrams.

## Components

| Component | Where | Notes |
|---|---|---|
| Verdict chip | everywhere a coverage tag is shown | dot plus word; four variants plus "Research" and "agent-proposed" |
| Verdict bar with legend | scenario card, scenario record, coverage | segments in order Have, Collectable, Blind, Unscored; legend below |
| Status chip | scenario, use case | draft, in-review, published, retired; proposed, built, tuned |
| Priority chip | scenario | NOW, NEAR-TERM, BACKLOG |
| Identifier tag | frameworks, mappings, tickets | mono, small; revoked and deprecated variants |
| Score select | edit cards, session | every option carries its label text, not just the number |
| Edit card | scenario rows in Edit and Session | two scores, verdict preview, owed items, text fields, "captured" marker |
| Findings list | after any save | error and warning rows with `where` and message; clicking one focuses the field |
| Two door panel | scenario record, readiness | scoring path and discovery path, each "available" with the command or a blocker count with the list |
| Caveat box | framework mapping, illustrative records, hypothetical text | warn tokens |
| View header | every screen | organization, shape, drafts flag, baseline |
| Save dialog | every Edit | name (read only), reason (required), ticket (conditional) |

## Accessibility

WCAG 2.2 AA. Every interactive element reachable by keyboard; the session map already
uses arrow keys and Esc. Every color paired with text. Tables have headers. Findings are
announced when they appear.
