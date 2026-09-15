#!/usr/bin/env python3
"""
Generate the two entity relationship diagrams for the Liszt data model, in the same
style as the program's system diagrams (docs/diagrams/make_diagrams.py in the Liszt
repository), so they version control and match visually.

    python3 diagrams/make_erd.py

Outputs, next to this script:
    erd-spine.svg / .png    the spine, with attributes
    erd-full.svg / .png     every entity that has a relationship, grouped by family

Crow's Foot notation. Parent end carries a bar (one); child end carries a crow's foot
(many). A circle marks optional (zero or). Edit the tables below, not the SVG.
"""
from __future__ import annotations

import pathlib

INK = "#1F2D38"; BLUE = "#2C6E8F"; RED = "#B0463B"; GREEN = "#2F7D57"; AMBER = "#B5852B"
GRAY = "#5B6B78"; RULE = "#D4D9DE"; PALE = "#EFF2F5"; PALEB = "#E7EEF3"; PALER = "#FBEEEC"
PALEG = "#EAF2ED"; PALEA = "#FAF3E2"; WHITE = "#FFFFFF"; PURPLE = "#6B4E8F"; PALEP = "#EFEAF5"
SANS = "Calibri, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "Consolas, Menlo, monospace"
HERE = pathlib.Path(__file__).resolve().parent

FAMILY = {
    "reference": (BLUE, PALEB, "REFERENCE"),
    "authored": (INK, WHITE, "AUTHORED"),
    "observed": (AMBER, PALEA, "OBSERVED"),
    "computed": (GREEN, PALEG, "COMPUTED"),
    "interface": (PURPLE, PALEP, "INTERFACES"),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=13, color=INK, weight="normal", anchor="start", font=SANS, spacing=0):
    ls = f' letter-spacing="{spacing}"' if spacing else ""
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{ls}>{esc(s)}</text>')


def box(x, y, w, h, fill=WHITE, stroke=RULE, rx=6, sw=1.5):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>')


DEFS = f'''<defs>
  <marker id="one" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse">
    <line x1="7" y1="1" x2="7" y2="11" stroke="{GRAY}" stroke-width="1.6"/>
  </marker>
  <marker id="many" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="12" markerHeight="12" orient="auto-start-reverse">
    <path d="M 1 6 L 11 1 M 1 6 L 11 6 M 1 6 L 11 11" fill="none" stroke="{GRAY}" stroke-width="1.4"/>
  </marker>
  <marker id="zeromany" viewBox="0 0 16 12" refX="15" refY="6" markerWidth="16" markerHeight="12" orient="auto-start-reverse">
    <circle cx="3" cy="6" r="2.4" fill="{WHITE}" stroke="{GRAY}" stroke-width="1.3"/>
    <path d="M 5 6 L 15 1 M 5 6 L 15 6 M 5 6 L 15 11" fill="none" stroke="{GRAY}" stroke-width="1.4"/>
  </marker>
  <marker id="zeroone" viewBox="0 0 16 12" refX="15" refY="6" markerWidth="16" markerHeight="12" orient="auto-start-reverse">
    <circle cx="4" cy="6" r="2.4" fill="{WHITE}" stroke="{GRAY}" stroke-width="1.3"/>
    <line x1="11" y1="1" x2="11" y2="11" stroke="{GRAY}" stroke-width="1.6"/>
  </marker>
</defs>'''

MARK = {"1": "one", "N": "many", "0N": "zeromany", "01": "zeroone"}


def edge(ax, ay, bx, by, a_card, b_card, label=""):
    """A curve from A (parent side) to B (child side) with a marker at each end."""
    dx = (bx - ax) * 0.45
    d = f"M {ax} {ay} C {ax + dx} {ay}, {bx - dx} {by}, {bx} {by}"
    s = (f'<path d="{d}" fill="none" stroke="{GRAY}" stroke-width="1.4" '
         f'marker-start="url(#{MARK[a_card]})" marker-end="url(#{MARK[b_card]})"/>')
    if label:
        mx, my = (ax + bx) / 2, (ay + by) / 2 - 5
        s += (f'<rect x="{mx - len(label) * 3.2 - 4}" y="{my - 11}" width="{len(label) * 6.4 + 8}" '
              f'height="15" fill="{WHITE}" opacity="0.92"/>')
        s += text(mx, my, label, 11, GRAY, anchor="middle")
    return s


def entity_box(x, y, w, name, family, attrs=(), key_attrs=()):
    color, fill, _ = FAMILY[family]
    ah = 17
    h = 34 + (len(attrs) * ah + 8 if attrs else 0)
    s = [box(x, y, w, h, WHITE, color, sw=2),
         f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="6" fill="{fill}"/>',
         f'<rect x="{x}" y="{y + 22}" width="{w}" height="8" fill="{fill}"/>',
         f'<line x1="{x}" y1="{y + 30}" x2="{x + w}" y2="{y + 30}" stroke="{color}" stroke-width="1.5"/>',
         text(x + 12, y + 20, name, 13.5, color, "bold", spacing=0.6)]
    for i, a in enumerate(attrs):
        yy = y + 30 + 14 + i * ah
        bold = "bold" if a in key_attrs else "normal"
        s.append(text(x + 12, yy, a, 11.5, INK, bold, font=MONO))
    return "".join(s), h


def frame(W, H, title, subtitle):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
            f'<rect width="{W}" height="{H}" fill="{WHITE}"/>', DEFS,
            text(60, 58, "LISZT", 24, BLUE, "bold", spacing=4),
            text(60, 92, title, 27, INK, "bold", font="Cambria, Georgia, serif"),
            text(60, 118, subtitle, 14, GRAY),
            f'<line x1="60" y1="132" x2="{W - 60}" y2="132" stroke="{RULE}" stroke-width="2"/>']


def legend(x, y):
    s = [box(x, y, 560, 54, PALE, RULE, rx=6)]
    s.append(text(x + 14, y + 22, "CROW'S FOOT", 11, INK, "bold", spacing=1.2))
    s.append(edge(x + 120, y + 18, x + 200, y + 18, "1", "N"))
    s.append(text(x + 210, y + 22, "one to many", 11, GRAY))
    s.append(edge(x + 310, y + 18, x + 390, y + 18, "1", "0N"))
    s.append(text(x + 400, y + 22, "one to zero or many", 11, GRAY))
    s.append(edge(x + 120, y + 42, x + 200, y + 42, "1", "1"))
    s.append(text(x + 210, y + 46, "one to exactly one", 11, GRAY))
    s.append(edge(x + 310, y + 42, x + 390, y + 42, "1", "01"))
    s.append(text(x + 400, y + 46, "one to zero or one", 11, GRAY))
    return "".join(s)


# ═════════════════════════════════════════════════════════════════════════════
# Diagram 1: the spine
# ═════════════════════════════════════════════════════════════════════════════

def spine() -> str:
    W, H = 1760, 1090
    s = frame(W, H, "The spine of the data model",
              "Scenario, attack step, evidence row, coverage assessment, the infrastructure shape and the framework "
              "references. Bold attributes are keys. The coverage tag is generated, never written.")
    E = {}

    def place(name, x, y, fam, attrs, keys=()):
        svg, h = entity_box(x, y, 300, name, fam, attrs, keys)
        s.append(svg)
        E[name] = (x, y, 300, h)

    place("Infrastructure Shape", 60, 170, "reference",
          ["shape_id  (SHAPE-AI)", "family", "status  catalog|proposed"], ["shape_id  (SHAPE-AI)"])
    place("Shape Layer", 60, 290, "reference",
          ["shape_id  FK", "code  L0..L4", "canonical string", "covers, components, matters"],
          ["shape_id  FK", "code  L0..L4"])
    place("Framework Baseline", 60, 440, "reference",
          ["baseline  char(7)", "status  current|superseded", "owner", "review_due"], ["baseline  char(7)"])
    place("Technique Reference", 60, 590, "reference",
          ["baseline  FK", "framework", "technique_id", "name", "revoked / deprecated", "revoked_by"],
          ["baseline  FK", "framework", "technique_id"])
    place("Data Component", 60, 780, "reference",
          ["baseline  FK", "dc_id", "name", "deprecated"], ["baseline  FK", "dc_id"])

    place("Scenario", 470, 170, "authored",
          ["scenario_id  char(3)", "slug, title, one_liner", "status  draft..retired", "mode  attack|failure",
           "priority, evidence_tier", "stack  FK -> Infrastructure Shape", "objective layer  FK -> Shape Layer",
           "baseline  FK", "authored_by, reviewed_by", "retired_*, superseded_by"],
          ["scenario_id  char(3)"])
    place("Attack Step", 470, 430, "authored",
          ["step_id  surrogate", "scenario_id  FK", "position  1..6 (not key)", "seam_tag  18 chars",
           "text", "control_held"], ["step_id  surrogate"])
    place("Step Technique Mapping", 470, 620, "authored",
          ["step_id  FK", "baseline, framework, technique_id  FK"], ["step_id  FK"])
    place("Scenario Framework Mapping", 470, 730, "authored",
          ["scenario_id  FK", "baseline, framework, technique_id  FK", "OWASP only, scenario level"],
          ["scenario_id  FK"])
    place("Evidence Row Data Component", 470, 860, "authored",
          ["row_id  FK", "baseline, dc_id  FK"], ["row_id  FK"])

    place("Evidence Row", 880, 430, "authored",
          ["row_id  surrogate", "scenario_id  FK", "kind  attack-step|control", "step_id  FK (null for control)",
           "display_position  1..8", "signal", "emitted_at", "detection_opportunity"], ["row_id  surrogate"])
    place("Assessment Header", 880, 760, "authored",
          ["scenario_id, org_id  PK", "assessed_by", "assessed", "baseline  FK (optional)"],
          ["scenario_id, org_id  PK"])

    place("Organization", 1290, 170, "reference", ["org_id", "name"], ["org_id"])
    place("Coverage Assessment", 1290, 330, "authored",
          ["assessment_id  surrogate", "row_id  FK", "org_id  FK", "visibility  0..4 | null",
           "detection  -1..5 | null", "q_* five dimensions", "coverage_tag  GENERATED",
           "source  (this org's system)", "owner, evidence, backlog_ref", "notes, research_needed",
           "score_provenance"], ["assessment_id  surrogate"])
    place("Coverage Tag", 1290, 660, "computed",
          ["vis == 0            -> Blind", "vis>=1 & det>=1     -> Have", "vis>=1 & det<=0     -> Collectable",
           "no scores           -> null"], [])

    def R(a, b, ac, bc, label="", side="rl", b_dy=0):
        ax, ay, aw, ah = E[a]; bx, by, bw, bh = E[b]
        if side == "rl":
            s.append(edge(ax + aw, ay + ah / 2, bx, by + bh / 2 + b_dy, ac, bc, label))
        elif side == "lr":
            s.append(edge(ax, ay + ah / 2, bx + bw, by + bh / 2, ac, bc, label))
        elif side == "bt":
            s.append(edge(ax + aw / 2, ay + ah, bx + bw / 2, by, ac, bc, label))
        elif side == "hop":
            x0 = ax + aw; mid = x0 + 40
            d = f"M {x0} {ay + ah / 2} C {mid} {ay + ah / 2}, {mid} {by + bh / 2}, {x0} {by + bh / 2}"
            s.append(f'<path d="{d}" fill="none" stroke="{GRAY}" stroke-width="1.4" '
                     f'marker-start="url(#{MARK[ac]})" marker-end="url(#{MARK[bc]})"/>')
            if label:
                s.append(text(mid + 6, (ay + ah / 2 + by + bh / 2) / 2 + 4, label, 11, GRAY))

    R("Infrastructure Shape", "Scenario", "1", "0N", "classified against", b_dy=-70)
    R("Infrastructure Shape", "Shape Layer", "1", "N", "", "bt")
    R("Shape Layer", "Scenario", "1", "0N", "objective layer", b_dy=0)
    R("Framework Baseline", "Scenario", "1", "0N", "vocabulary of", b_dy=70)
    R("Framework Baseline", "Technique Reference", "1", "0N", "", "bt")
    R("Technique Reference", "Data Component", "1", "0N", "same baseline", "bt")
    R("Scenario", "Attack Step", "1", "N", "3 to 6", "bt")
    R("Attack Step", "Step Technique Mapping", "1", "0N", "", "bt")
    R("Technique Reference", "Step Technique Mapping", "1", "0N", "resolves")
    R("Technique Reference", "Scenario Framework Mapping", "1", "0N", "")
    R("Data Component", "Evidence Row Data Component", "1", "0N", "")
    R("Scenario", "Evidence Row", "1", "N", "3 to 8")
    R("Attack Step", "Evidence Row", "1", "1", "exactly one")
    R("Evidence Row", "Evidence Row Data Component", "1", "0N", "cites", "lr")
    R("Evidence Row", "Coverage Assessment", "1", "0N", "one per org")
    R("Organization", "Coverage Assessment", "1", "0N", "assesses", "hop")
    R("Organization", "Assessment Header", "1", "0N", "signs", "lr")
    R("Coverage Assessment", "Coverage Tag", "1", "1", "derived", "bt")

    s.append(legend(60, H - 90))
    s.append(text(660, H - 58, "The scenario's own scores are the reference organization's assessment and live in Coverage Assessment like everyone else's.", 12.5, INK))
    s.append(text(660, H - 40, "An evidence row with no assessment for an organization is unscored for that organization. Unscored is null, never zero.", 12.5, RED))
    s.append("</svg>")
    return "".join(s)


# ═════════════════════════════════════════════════════════════════════════════
# Diagram 2: the whole model
# ═════════════════════════════════════════════════════════════════════════════
#
# Layout: four areas, left to right. Inside an area, a parent and its children are drawn
# as a tree: the children sit below the parent, indented, hung off one vertical bus.
# Relationships that cross areas are orthogonal connectors routed through the gutter
# between the areas, one channel per connector so lines never overlap. Crow's feet are
# drawn by hand at the child end so their size is fixed and legible.

BW, BH, GAP, INDENT = 250, 36, 10, 26


def foot(x, y, dx, dy, card, s):
    """Crow's foot (many), bar (one), with an optional circle, at end point (x, y),
    the line arriving along direction (dx, dy)."""
    px, py = -dy, dx                     # perpendicular
    def L(x1, y1, x2, y2):
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{GRAY}" stroke-width="1.5"/>')
    if card in ("N", "0N"):
        bx, by = x - 12 * dx, y - 12 * dy
        L(bx, by, x + px * 6, y + py * 6)
        L(bx, by, x - px * 6, y - py * 6)
        L(bx, by, x, y)
        if card == "0N":
            s.append(f'<circle cx="{x - 17 * dx:.1f}" cy="{y - 17 * dy:.1f}" r="3.2" '
                     f'fill="{WHITE}" stroke="{GRAY}" stroke-width="1.4"/>')
    else:
        bx, by = x - 7 * dx, y - 7 * dy
        L(bx + px * 6, by + py * 6, bx - px * 6, by - py * 6)
        if card == "01":
            s.append(f'<circle cx="{x - 15 * dx:.1f}" cy="{y - 15 * dy:.1f}" r="3.2" '
                     f'fill="{WHITE}" stroke="{GRAY}" stroke-width="1.4"/>')


def bar(x, y, dx, dy, s):
    """The parent end: a single bar a little way along the line."""
    px, py = -dy, dx
    bx, by = x + 8 * dx, y + 8 * dy
    s.append(f'<line x1="{bx + px * 6:.1f}" y1="{by + py * 6:.1f}" x2="{bx - px * 6:.1f}" '
             f'y2="{by - py * 6:.1f}" stroke="{GRAY}" stroke-width="1.5"/>')


def place_tree(s, E, x, y, node, depth=0):
    """node = (name, family, [children]) where a child may be (name, fam, [..], card).
    Returns the y below the tree."""
    name, fam, kids = node[0], node[1], node[2]
    svg, h = entity_box(x + depth * INDENT, y, BW - depth * INDENT, name, fam)
    s.append(svg)
    E[name] = (x + depth * INDENT, y, BW - depth * INDENT, h)
    y_next = y + h + GAP
    if kids:
        bus_x = x + depth * INDENT + 14
        bus_top = y + h
        last_mid = bus_top
        for kid in kids:
            kx = x + (depth + 1) * INDENT
            ky = y_next
            y_next = place_tree(s, E, x, y_next, kid, depth + 1)
            kh = E[kid[0]][3]
            mid = ky + kh / 2
            last_mid = mid
            card = kid[3] if len(kid) > 3 else "N"
            s.append(f'<line x1="{bus_x}" y1="{mid}" x2="{kx}" y2="{mid}" stroke="{GRAY}" stroke-width="1.5"/>')
            foot(kx, mid, 1, 0, card, s)
        s.insert(len(s) - 1, f'<line x1="{bus_x}" y1="{bus_top}" x2="{bus_x}" y2="{last_mid}" '
                              f'stroke="{GRAY}" stroke-width="1.5"/>')
        bar(bus_x, bus_top, 0, 1, s)
    return y_next


def cross(s, E, a, b, card, channel_x, a_side="right", b_side="left"):
    """Orthogonal connector from parent a to child b through a vertical channel."""
    ax, ay, aw, ah = E[a]; bx, by, bw, bh = E[b]
    ay_mid, by_mid = ay + ah / 2, by + bh / 2
    x1 = ax + aw if a_side == "right" else ax
    x2 = bx if b_side == "left" else bx + bw
    d = (f"M {x1} {ay_mid} L {channel_x} {ay_mid} L {channel_x} {by_mid} L {x2} {by_mid}")
    s.append(f'<path d="{d}" fill="none" stroke="{GRAY}" stroke-width="1.5"/>')
    bar(x1, ay_mid, 1 if a_side == "right" else -1, 0, s)
    foot(x2, by_mid, 1 if b_side == "left" else -1, 0, card, s)


def full() -> str:
    W, H = 1590, 1150
    s = frame(W, H, "The whole model, by area",
              "Color is the family: blue reference, white authored, amber observed, green computed, "
              "purple interface. A child hangs below its parent; connectors across areas run through the gutters.")
    E = {}
    cols = [60, 510, 870, 1230]
    heads = ["REFERENCE", "THE LIBRARY", "USE CASES · TESTING · ENVIRONMENTS", "RUNS · SCORING"]
    for x, h in zip(cols, heads):
        s.append(text(x, 165, h, 12.5, BLUE, "bold", spacing=1.6))

    R, A, O, C, I = "reference", "authored", "observed", "computed", "interface"
    trees = {
        0: [("Framework Baseline", R, [
                ("Framework Version", R, []),
                ("Technique Reference", R, [("Tactic", R, [], "N")]),
                ("Data Component", R, [])]),
            ("Infrastructure Shape", R, [
                ("Shape Layer", R, []),
                ("Seam Tag", R, []),
                ("Emitted Source Category", R, [])]),
            ("Organization", R, []),
            ("Session File", I, [])],
        1: [("Scenario", A, [
                ("Attack Step", A, [("Framework Roll-up", C, [], "1")]),
                ("Evidence Row", A, [("Coverage Assessment", A, [("Coverage Tag", C, [], "1")], "0N")]),
                ("Hardening Action", A, [], "0N"),
                ("Source Citation", A, [], "0N"),
                ("Assessment Header", A, [], "0N"),
                ("Readiness Verdict", C, [], "1")]),
            ("Incident", A, [("Contested Claim", A, [], "0N"), ("Source Citation ", A, [])]),
            ("Snapshot", C, [("Rollup Metrics", C, [], "1")])],
        2: [("Use Case", A, [
                ("Trigger / Composed Signal", A, []),
                ("Use Case Coverage", A, []),
                ("Promotion", A, [], "01"),
                ("Source Citation  ", A, [], "0N")]),
            ("Test Spec", A, [
                ("Authorization", A, [("Promotion ", A, [], "01")], "1"),
                ("Procedure Step", A, []),
                ("Excluded Step", A, [], "0N"),
                ("Prediction", A, [("Prediction Row", A, [])], "1")]),
            ("Discovery Spec", A, []),
            ("Environment Definition", A, [("Target", A, []), ("Environment Component", A, [])])],
        3: [("Run Record", O, [
                ("Observation", O, []),
                ("Stop Condition Triggered", O, [], "0N"),
                ("Scorecard", C, [("Scorecard Row", C, [("Proposed Rescore", C, [], "0N")])], "01")]),
            ("Discovery Run", O, [("Discovery Observation", O, [])]),
            ("Agent Run Import", I, [])],
    }
    for col, nodes in trees.items():
        y = 180
        for node in nodes:
            y = place_tree(s, E, cols[col], y, node) + 18
    # size the canvas to the content
    H = max(y0 + h0 for (_, y0, _, h0) in E.values()) + 150
    s[0] = s[0].replace(f'height="{1150}"', f'height="{H}"').replace(f'0 0 {W} {1150}', f'0 0 {W} {H}')
    s[0] = s[0].replace(f'<rect width="{W}" height="{1150}"', f'<rect width="{W}" height="{H}"')

    # cross area connectors, one channel each, spaced inside the 110 px gutter
    def ch(col, i):
        return cols[col] + BW + 18 + i * 16
    cross(s, E, "Framework Baseline", "Scenario", "0N", ch(0, 0))
    cross(s, E, "Technique Reference", "Attack Step", "0N", ch(0, 1))
    cross(s, E, "Data Component", "Evidence Row", "0N", ch(0, 2))
    cross(s, E, "Organization", "Coverage Assessment", "0N", ch(0, 3))
    cross(s, E, "Session File", "Coverage Assessment", "N", ch(0, 4))
    cross(s, E, "Framework Baseline", "Snapshot", "0N", ch(0, 5))
    cross(s, E, "Infrastructure Shape", "Scenario", "0N", ch(0, 6))
    cross(s, E, "Shape Layer", "Scenario", "0N", ch(0, 7))
    cross(s, E, "Seam Tag", "Attack Step", "0N", ch(0, 8))
    cross(s, E, "Emitted Source Category", "Evidence Row", "0N", ch(0, 9))
    cross(s, E, "Infrastructure Shape", "Environment Definition", "0N", ch(0, 10))
    cross(s, E, "Infrastructure Shape", "Snapshot", "0N", ch(0, 11))

    cross(s, E, "Scenario", "Test Spec", "01", ch(1, 0))
    cross(s, E, "Scenario", "Discovery Spec", "01", ch(1, 1))
    cross(s, E, "Attack Step", "Use Case Coverage", "0N", ch(1, 2))
    cross(s, E, "Evidence Row", "Trigger / Composed Signal", "0N", ch(1, 3))

    cross(s, E, "Prediction", "Run Record", "0N", ch(2, 0))
    cross(s, E, "Environment Definition", "Run Record", "0N", ch(2, 1))
    cross(s, E, "Environment Definition", "Discovery Run", "0N", ch(2, 2))
    cross(s, E, "Discovery Spec", "Discovery Run", "0N", ch(2, 3))

    # the import feeds the runs: routed on the right of the last column, upward
    cross(s, E, "Agent Run Import", "Run Record", "01", ch(3, 0), "right", "right")
    cross(s, E, "Agent Run Import", "Discovery Run", "01", ch(3, 1), "right", "right")

    s.append(legend(60, H - 90))
    s.append(text(660, H - 66, "Source Citation appears under three parents because it is one shape with three owners. Promotion appears twice for the same reason.", 12.5, INK))
    s.append(text(660, H - 48, "Every derived entity (green) is written by a tool, never by hand. A snapshot reports one organization and one infrastructure shape; nothing is blended across shapes.", 12.5, INK))
    s.append(text(660, H - 30, "Not drawn: Attack Step to Hardening Action (many to many), Scenario to Incident (many to many), Technique Reference to Tactic (many to many).", 12.5, GRAY))
    s.append("</svg>")
    return "".join(s)


def main() -> int:
    for name, svg in (("erd-spine", spine()), ("erd-full", full())):
        (HERE / f"{name}.svg").write_text(svg, encoding="utf-8")
        try:
            import cairosvg
            cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=str(HERE / f"{name}.png"),
                             output_width=2520)
            print(f"  {name}.svg  {name}.png")
        except ImportError:
            print(f"  {name}.svg  (install cairosvg for the PNG)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
