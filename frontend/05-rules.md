# Rules the interface must not break

Each rule, what it means on screen, and why. They come from the viewer data contract and the
program's doctrine; breaking one produces numbers that disagree with the rest of the
program, which is worse than showing nothing.

| # | Rule | On screen | Why |
|---|---|---|---|
| 1 | Never compute the coverage label | The verdict comes from the read model. Edit mode may preview it from the two scores, and must label the preview as a preview | One rule, one place. Two implementations drift |
| 2 | Never treat an unscored row as zero | Unscored is its own state with its own color and word. Shares read "n/a" or "not scored", never 0% | Scoring nothing and scoring badly must not produce the same number |
| 3 | Every percentage travels with its completeness companion | "scored of rows" or "scored scenarios of total" beside every figure | 100% Have over one row of six and over six of six are the same number and different worlds |
| 4 | Organization, shape and drafts flag are always visible | In the header of every screen that shows a figure | A figure that silently includes drafts or one organization's view is a number people act on wrongly |
| 5 | Never blend across infrastructure shapes | Every figure is for one shape, named. No combined view exists | Blending an AI population with an endpoint population makes the AI picture look better than it is |
| 6 | Never carry state by color alone | Every verdict chip has the word; the legend pairs each color with its word | Color vision, print, screen readers |
| 7 | Never present a cross framework mapping as authoritative | The editorial caveat box appears whenever `mapping_confidence` is editorial; the Frameworks page carries the reliability note | There is no authoritative crosswalk between OWASP and either MITRE framework |
| 8 | Show status, autonomy and limits on every use case | Chips in the header, limits never collapsed | A proposed use case is a plan; autonomy above notify means a machine acts first; limits are what stop over trust |
| 9 | Never write a record except through a change set with a name and a reason | Save always asks; the platform's imports carry a service identity | Nothing writes itself back |
| 10 | Derived fields have no control in Edit mode and are marked derived | Coverage, counts, roll-up, readiness, use case chips, dates, reviewer, status | A CRUD design with an editable coverage column would destroy the product's one claim |
| 11 | A score change without a ticket is a rescore | Save refuses it; the next snapshot lists accepted rescores separately | Movement must be visible next to its cost |
| 12 | Show the server's findings verbatim, by field | Errors block, warnings do not | The messages are written to be read by people and are the same ones the validator prints |
| 13 | A run is immutable; a correction is a new run | No edit control on a run or a scorecard | The digest chain is the evidentiary basis of the calibration claim |
| 14 | A triggered stop condition is a successful guardrail | Shown as such on the scorecard, never as a failed run | The distinction survives into reporting |
| 15 | Hypothetical text is labeled | "Hypothetical, not observed." precedes `scaled_up` | The box must never read as observed fact |
| 16 | Identifiers show their baseline | Wherever an identifier is shown, the baseline is on the page | Identifiers are not comparable across baselines |
| 17 | No network calls the application does not own | Fonts, scripts and data are served by the application; nothing loads from a third party | The application runs in an environment with no internet |
