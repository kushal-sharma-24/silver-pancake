"""Generate a 4-slide HiveShip deck: Overview, Product, Business Case, Competitive."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import os

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Colours ──
BG_NAVY    = RGBColor(0x0F, 0x17, 0x2A)
CARD_BG    = RGBColor(0x1A, 0x23, 0x3B)
CARD_BORDER = RGBColor(0x37, 0x47, 0x4F)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
GOLD       = RGBColor(0xFF, 0xC1, 0x07)
LIGHT_BLUE = RGBColor(0x64, 0xB5, 0xF6)
LIGHT_GRAY = RGBColor(0xB0, 0xBE, 0xC5)
GREEN      = RGBColor(0x66, 0xBB, 0x6A)
ORANGE     = RGBColor(0xFF, 0xA7, 0x26)
RED_SOFT   = RGBColor(0xEF, 0x53, 0x50)
CYAN       = RGBColor(0x26, 0xC6, 0xDA)


def new_slide():
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.background.fill
    bg.solid()
    bg.fore_color.rgb = BG_NAVY
    return slide


def add_text(slide, left, top, width, height, text, size, color,
             bold=False, alignment=PP_ALIGN.LEFT, font_name="Segoe UI"):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_multiline(slide, left, top, width, height, lines, size, color,
                  bold=False, alignment=PP_ALIGN.LEFT, spacing=1.2, font_name="Segoe UI"):
    """Add a text box with multiple paragraphs."""
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top),
                                     Inches(width), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.color.rgb = color
        p.font.bold = bold
        p.font.name = font_name
        p.alignment = alignment
        p.space_after = Pt(size * (spacing - 1))
    return txBox


def add_card(slide, x, y, w, h):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.color.rgb = CARD_BORDER
    shape.line.width = Pt(1)
    return shape


def slide_footer(slide):
    add_text(slide, 0.6, 6.95, 12, 0.35,
             "HiveShip  —  Headless  ·  Self-Hosted  ·  LLM-Agnostic  ·  Internal Infrastructure",
             12, LIGHT_BLUE, bold=True, alignment=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 1 — TITLE / OVERVIEW  (unchanged from original)
# ═══════════════════════════════════════════════════════════════════
slide = new_slide()

add_text(slide, 0.6, 0.3, 6, 0.9, "HiveShip", 44, GOLD, bold=True)
add_text(slide, 0.6, 1.0, 8, 0.5,
         "Internal Delivery Infrastructure", 20, LIGHT_BLUE)
add_text(slide, 0.6, 1.7, 10, 0.6,
         "Headless automation that handles work when no developer is present \u2014 "
         "webhook PR fixes, fleet-wide ops, boilerplate generation, off-hours maintenance.", 16, WHITE)

# Flow boxes
flow_y = 2.7
steps = [
    ("1", "Goal",   "Plain-English\nfeature description"),
    ("2", "Plan",   "LLM decomposes goal\ninto agent DAG"),
    ("3", "Build",  "Parallel agents write\ncode artifacts"),
    ("4", "Review", "AI reviewer flags\nconcrete issues"),
    ("5", "Fix",    "Agents auto-fix\nreview feedback"),
    ("6", "PR",     "Branch + PR opened\non GitHub"),
]
box_w, gap, start_x = 1.7, 0.35, 0.6
for i, (num, title, desc) in enumerate(steps):
    x = start_x + i * (box_w + gap)
    add_card(slide, x, flow_y, box_w, 1.55)
    add_text(slide, x + 0.05, flow_y + 0.05, 0.4, 0.35, num, 14, GOLD,
             bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, x + 0.05, flow_y + 0.35, box_w - 0.1, 0.35, title, 15,
             WHITE, bold=True, alignment=PP_ALIGN.CENTER)
    add_text(slide, x + 0.05, flow_y + 0.7, box_w - 0.1, 0.8, desc, 11,
             LIGHT_GRAY, alignment=PP_ALIGN.CENTER)
    if i < len(steps) - 1:
        add_text(slide, x + box_w, flow_y + 0.45, gap, 0.35, "\u2192", 20,
                 GOLD, bold=True, alignment=PP_ALIGN.CENTER)

# Differentiators
dy = 4.7
add_text(slide, 0.6, dy, 6, 0.4, "Why HiveShip?", 22, GOLD, bold=True)
for i, (lab, desc) in enumerate([
    ("Webhook PR Fix",   "PR comment \u2192 auto-fix \u2192 commit pushed. No developer context-switch"),
    ("Fleet Batch Ops",  "One trigger \u2192 N repos updated overnight. Developers review in the morning"),
    ("BYO LLM",         "Gemini, Ollama, vLLM \u2014 hybrid: frontier for planner, self-hosted for agents"),
    ("Self-Hosted",      "Single Docker container. Runs on your infra, fully offline with Ollama"),
    ("Goal \u2192 PR",  "Output is a reviewed GitHub PR, not files in an editor"),
]):
    y = dy + 0.5 + i * 0.4
    add_text(slide, 0.8, y, 2.2, 0.35, f"\u25cf  {lab}", 13, GREEN, bold=True)
    add_text(slide, 3.0, y, 8, 0.35, desc, 13, LIGHT_GRAY)

slide_footer(slide)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 2 — PRODUCT OVERVIEW
# ═══════════════════════════════════════════════════════════════════
slide = new_slide()

add_text(slide, 0.6, 0.3, 8, 0.7, "Product Overview", 36, GOLD, bold=True)
add_text(slide, 0.6, 0.95, 10, 0.5,
         "Headless automation for the work IDE tools don\u2019t cover: "
         "webhook PR revision, fleet-wide batch ops, CI auto-fix, off-hours maintenance.",
         16, WHITE)

# ── Left column: 5-phase pipeline ──
add_text(slide, 0.6, 1.8, 5, 0.4, "5-Phase Pipeline", 20, LIGHT_BLUE, bold=True)

phases = [
    ("1  PLANNING",           "LLM decomposes the goal into a DAG of 1\u20138 specialist agents"),
    ("2  DAG EXECUTION",      "Agents run in parallel (up to 4 threads); blocked agents auto-spawn helpers"),
    ("3  DELIVERY SYNTHESIS",  "Agent artifacts are merged into self-contained, runnable source files"),
    ("4  SELF-REVIEW",         "Reviewer agent checks code; rejected \u2192 fixer agent patches & re-submits"),
    ("5  PR DELIVERY",         "Branch created, files pushed, Pull Request opened on GitHub"),
]
for i, (phase, desc) in enumerate(phases):
    y = 2.3 + i * 0.85
    add_card(slide, 0.6, y, 5.8, 0.75)
    add_text(slide, 0.75, y + 0.05, 2.5, 0.35, phase, 13, GOLD, bold=True)
    add_text(slide, 0.75, y + 0.38, 5.4, 0.35, desc, 12, LIGHT_GRAY)

# ── Right column: Architecture properties ──
add_text(slide, 7.0, 1.8, 5, 0.4, "Architecture", 20, LIGHT_BLUE, bold=True)

props = [
    ("Multi-Agent DAG",      "Work decomposed into parallel specialist roles, not one monolithic prompt"),
    ("Self-Healing",          "Blocked agents trigger helper spawning; failed agents pruned gracefully"),
    ("Self-Reviewing",        "Separate reviewer agent evaluates output before delivery"),
    ("BYO LLM",              "Gemini, vLLM, Ollama, LM Studio \u2014 any OpenAI-compatible API"),
    ("Headless / API-First", "FastAPI server with REST + SSE; no IDE required"),
    ("Git-Native Output",    "Real PR on a real repo \u2014 not clipboard text or chat messages"),
    ("Container-Ready",      "Single Docker image \u2192 Azure Container Apps, AWS ECS, any host"),
]
for i, (prop, desc) in enumerate(props):
    y = 2.3 + i * 0.72
    add_text(slide, 7.2, y, 2.5, 0.35, f"\u25cf  {prop}", 13, GREEN, bold=True)
    add_text(slide, 7.2, y + 0.3, 5.5, 0.35, desc, 11, LIGHT_GRAY)

# Deployment diagram (simplified)
add_text(slide, 7.0, 6.0, 6, 0.5,
         "CLI / Teams / Webhook / Cron  \u2192  HiveShip API  \u2192  GitHub PR",
         14, CYAN, bold=True, alignment=PP_ALIGN.CENTER)
add_text(slide, 7.0, 6.4, 6, 0.35,
         "\u2193  LLM: Gemini Flash (planner) + Ollama/vLLM (agents)",
         12, LIGHT_GRAY, alignment=PP_ALIGN.CENTER)

slide_footer(slide)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 3 — BUSINESS CASE
# ═══════════════════════════════════════════════════════════════════
slide = new_slide()

add_text(slide, 0.6, 0.3, 8, 0.7, "Business Case", 36, GOLD, bold=True)

# Problem statement
add_text(slide, 0.6, 1.05, 12, 0.4, "The Problem", 20, RED_SOFT, bold=True)
add_text(slide, 0.6, 1.45, 12, 0.5,
         "Service companies bill for developer time, but margins are shrinking. "
         "AI coding tools help individuals type faster \u2014 they don\u2019t change "
         "team-level economics. The bottleneck is overhead, not typing speed.", 14, WHITE)

# Value prop table
add_text(slide, 0.6, 2.2, 6, 0.4, "Quantified Value", 20, GREEN, bold=True)

# Table header
tbl_x, tbl_y = 0.6, 2.7
col_widths = [3.0, 2.8, 2.8, 2.2]
headers = ["Metric", "Without HiveShip", "With HiveShip", "Improvement"]
add_card(slide, tbl_x, tbl_y, sum(col_widths) + 0.4, 0.4)
cx = tbl_x + 0.2
for j, (hdr, cw) in enumerate(zip(headers, col_widths)):
    add_text(slide, cx, tbl_y + 0.05, cw, 0.35, hdr, 12, GOLD, bold=True)
    cx += cw

rows = [
    ("Throughput gain",         "9 devs = 9 devs",       "9 devs + HiveShip",   "15\u201320% more output"),
    ("Boilerplate stories",    "1 dev \u00d7 5\u20137 SP",     "Auto-PR, 1hr review", "2\u20133 days saved/sprint"),
    ("PR comment fix cycle",   "~30 min context-switch", "Webhook auto-fix",    "Zero dev interruption"),
    ("Fleet-wide operation",   "30 devs \u00d7 2 hrs",     "1 trigger \u2192 30 PRs",  "10\u201350x faster"),
    ("Margin per project",     "Standard billing",      "15\u201320% throughput \u2191", "$120\u2013240K extra"),
]
for i, (m, wo, wi, imp) in enumerate(rows):
    ry = tbl_y + 0.45 + i * 0.38
    add_card(slide, tbl_x, ry, sum(col_widths) + 0.4, 0.35)
    cx = tbl_x + 0.2
    for j, (val, cw) in enumerate(zip([m, wo, wi, imp], col_widths)):
        clr = WHITE if j < 3 else GREEN
        add_text(slide, cx, ry + 0.03, cw, 0.3, val, 11, clr, bold=(j == 3))
        cx += cw

# ── Right side: Who is this for? ──
add_text(slide, 7.0, 2.2, 5, 0.4, "Who Is This For?", 20, LIGHT_BLUE, bold=True)
personas = [
    ("Your Delivery Team",     "9 devs deliver like 12. Boilerplate stories auto-generated as PRs"),
    ("Existing Clients",       "Managed codebase health: deps, tests, security fixes. $2\u20135K/mo"),
    ("Migration Contracts",    "Legacy modernization at lower bids. HiveShip + 2 reviewers"),
    ("Peer Service Cos",       "White-label license as a delivery accelerator. $10\u201330K/yr"),
    ("CI/CD Integration",      "CI fail \u2192 auto-fix \u2192 push. Off-hours, zero human session"),
]
for i, (persona, pain) in enumerate(personas):
    y = 2.7 + i * 0.65
    add_text(slide, 7.2, y, 2.4, 0.3, f"\u25cf  {persona}", 13, ORANGE, bold=True)
    add_text(slide, 7.2, y + 0.3, 5.5, 0.3, pain, 11, LIGHT_GRAY)

# ── Bottom: Cost model ──
add_text(slide, 0.6, 5.4, 12, 0.4, "Cost Model (Hybrid LLM)", 18, GOLD, bold=True)
why_now = [
    "\u25cf  Planner: Gemini Flash (~$0.02/call) \u2014 needs reasoning quality, 1\u20132 calls/job",
    "\u25cf  Executor agents: self-hosted 30B via Ollama ($0/call) \u2014 pattern-heavy tasks",
    "\u25cf  Total per job: ~$0.03 hybrid  vs  ~$1.10 frontier-only (Opus)",
    "\u25cf  Frontier-only is NOT viable: 50 jobs/day @ $1.10 = $1,650/mo \u2192 no margin",
]
for i, line in enumerate(why_now):
    add_text(slide, 0.8, 5.85 + i * 0.3, 11, 0.3, line, 12, LIGHT_GRAY)

slide_footer(slide)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 4 — COMPETITIVE ANALYSIS
# ═══════════════════════════════════════════════════════════════════
slide = new_slide()

add_text(slide, 0.6, 0.3, 8, 0.7, "Competitive Landscape", 36, GOLD, bold=True)

# Market reality
add_text(slide, 0.6, 1.05, 12, 0.5,
         "The autonomous coding market has matured. Multiple well-funded tools now do "
         "goal-to-PR generation. HiveShip\u2019s differentiation is operational, not categorical.",
         14, WHITE)

# Where We Lose (honest)
add_text(slide, 0.6, 1.7, 6, 0.35, "Where We Lose (Honestly)", 16, RED_SOFT, bold=True)
lose_items = [
    "Copilot Agent: $10/mo, execution feedback, GitHub-native",
    "Claude Code: interactive reasoning, human-in-the-loop",
    "Jules: secure VM sandbox, test execution, self-critique",
    "Devin: enterprise fine-tuning, Slack/Jira integration",
]
for i, item in enumerate(lose_items):
    add_text(slide, 0.8, 2.1 + i * 0.3, 5.5, 0.3, f"\u2717  {item}", 11, LIGHT_GRAY)

# ── Where We Win cards ──
add_text(slide, 7.0, 1.7, 6, 0.35, "Where We Win (Narrow but Real)", 16, GREEN, bold=True)

win_cards = [
    ("Webhook PR Revision",    "PR comment \u2192 auto-fix \u2192 push.\nNo competitor does this as a background service."),
    ("Fleet Batch Operations", "1 trigger \u2192 50 repos updated overnight.\nClosest: Devin ($500/mo SaaS)."),
    ("CI Auto-Fix",            "CI fail \u2192 read error \u2192 fix \u2192 push.\nNo IDE session, no human."),
    ("Zero Vendor Dependency", "Fully offline with Ollama. No API key,\nno license, no telemetry."),
    ("Customizable Pipeline",  "Every prompt, schema, review criterion\nis in your codebase."),
]

for i, (title, desc) in enumerate(win_cards):
    y = 2.1 + i * 0.72
    add_card(slide, 7.0, y, 5.8, 0.65)
    add_text(slide, 7.15, y + 0.05, 2.5, 0.3, f"\u2713  {title}", 12, GREEN, bold=True)
    add_text(slide, 7.15, y + 0.3, 5.4, 0.35, desc, 10, LIGHT_GRAY)

# ── Positioning summary ──
qx, qy, qw, qh = 0.4, 5.85, 12.5, 0.95
add_card(slide, qx, qy, qw, qh)
add_text(slide, qx + 0.2, qy + 0.05, qw - 0.4, 0.35,
         "Positioning:  HiveShip is NOT a product competing with Copilot or Claude Code. "
         "It\u2019s internal infrastructure for the work those tools can\u2019t do.",
         13, WHITE, alignment=PP_ALIGN.CENTER)
add_text(slide, qx + 0.2, qy + 0.4, qw - 0.4, 0.5,
         "Developers use Copilot for daily coding.  They use Claude Code for complex problems.  "
         "The team uses HiveShip for unattended batch work, webhook automation, and off-hours maintenance.",
         12, GOLD, bold=True, alignment=PP_ALIGN.CENTER)

slide_footer(slide)


# ═══════════════════════════════════════════════════════════════════
# SAVE
# ═══════════════════════════════════════════════════════════════════
out_path = os.path.join(os.path.dirname(__file__), "HiveShip-Overview.pptx")
prs.save(out_path)
print(f"Saved 4-slide deck → {out_path}")
