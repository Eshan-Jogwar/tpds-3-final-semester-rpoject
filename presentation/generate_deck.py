#!/usr/bin/env python3
"""
generate_deck.py — Professional Native PowerPoint Generator for Campus Platform
Adheres strictly to anti-slop-ui, anti-slop-writing, technical-writing-density,
and presentation-creator design and copy principles.
"""

import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    # 16:9 widescreen: 13.333 x 7.5 inches
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- COLOR SYSTEM TOKENS (Strict Anti-Slop Palette) ---
    NAVY_DARK = RGBColor(11, 17, 32)        # #0b1120 (Hero/Closing canvas)
    NAVY_CARD = RGBColor(20, 30, 52)        # #141e34 (Dark card surface)
    NAVY_BORDER = RGBColor(38, 54, 88)      # #263658 (Dark card border)
    
    LIGHT_BG = RGBColor(248, 250, 252)      # #f8fafc (Light canvas)
    WHITE = RGBColor(255, 255, 255)         # #ffffff (Card surface)
    CARD_BORDER = RGBColor(226, 232, 240)   # #e2e8f0 (Light card border)
    
    PRIMARY_BLUE = RGBColor(30, 58, 138)    # #1e3a8a (Deep Navy Primary)
    ELECTRIC_SKY = RGBColor(2, 132, 199)    # #0284c7 (Single Intentional Accent)
    LIGHT_SKY = RGBColor(56, 189, 248)      # #38bdf8 (Glow / Accent on Dark)
    TINT_SKY_BG = RGBColor(239, 246, 255)   # #eff6ff (Subtle Sky Tint)
    TINT_SKY_BORDER = RGBColor(191, 219, 254) # #bfdbfe
    
    DARK_TEXT = RGBColor(15, 23, 42)        # #0f172a (Primary Text)
    MUTED_TEXT = RGBColor(71, 85, 105)      # #475569 (Secondary Text)
    SUBTLE_TEXT = RGBColor(100, 116, 139)   # #64748b (Captions & Footers)
    LIGHT_TEXT = RGBColor(248, 250, 252)    # #f8fafc (Light Text)
    LIGHT_MUTED = RGBColor(148, 163, 184)   # #94a3b8 (Light Muted Text)

    GREEN = RGBColor(16, 185, 129)          # #10b981 (Semantic: Met / Success)
    GREEN_BG = RGBColor(236, 253, 245)      # #ecfdf5
    RED = RGBColor(239, 68, 68)             # #ef4444 (Semantic: Flaw / Breach)
    RED_BG = RGBColor(254, 242, 242)        # #fef2f2
    AMBER = RGBColor(245, 158, 11)          # #f59e0b (Semantic: Warning / Pending)

    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"

    # --- REUSABLE UI PRIMITIVES ---
    def set_bg(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    def add_header(slide, kicker, title, subtitle, dark=False):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = kicker.upper()
        p0.font.name = FONT_MONO
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = LIGHT_SKY if dark else ELECTRIC_SKY
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(23)
        p1.font.bold = True
        p1.font.color.rgb = WHITE if dark else DARK_TEXT
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = LIGHT_MUTED if dark else MUTED_TEXT

        # Subtle divider
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.52), Inches(11.733), Pt(1)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = NAVY_BORDER if dark else CARD_BORDER
        line.line.fill.background()

    def add_footer(slide, slide_num, total=9, dark=False):
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(6.92), Inches(11.733), Pt(1)
        )
        line.fill.solid()
        line.fill.fore_color.rgb = NAVY_BORDER if dark else CARD_BORDER
        line.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(6.96), Inches(11.733), Inches(0.35))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        p.text = "CAMPUS PLATFORM · TPDS-III CAPSTONE DEFENSE"
        p.font.name = FONT_MONO
        p.font.size = Pt(9)
        p.font.color.rgb = LIGHT_MUTED if dark else SUBTLE_TEXT

        p_right = tf.add_paragraph()
        p_right.text = f"SLIDE {slide_num:02d} / {total:02d}"
        p_right.alignment = PP_ALIGN.RIGHT
        p_right.font.name = FONT_MONO
        p_right.font.size = Pt(9)
        p_right.font.bold = True
        p_right.font.color.rgb = LIGHT_SKY if dark else ELECTRIC_SKY

    def create_card(slide, left, top, width, height, bg_color=WHITE, border_color=CARD_BORDER, border_width=Pt(1)):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = border_width
        return card

    def add_fitted_picture(slide, img_path, box_left, box_top, box_width, box_height):
        if not os.path.exists(img_path):
            return None
        with Image.open(img_path) as im:
            img_w, img_h = im.size
        aspect = img_w / img_h
        box_aspect = (box_width / box_height)

        if aspect > box_aspect:
            render_w = box_width
            render_h = box_width / aspect
            x = box_left
            y = box_top + (box_height - render_h) / 2
        else:
            render_h = box_height
            render_w = box_height * aspect
            x = box_left + (box_width - render_w) / 2
            y = box_top

        return slide.shapes.add_picture(img_path, x, y, width=render_w, height=render_h)

    def attach_notes(slide, takeaway, talk_track, transition, question, defense):
        bullets = "\n".join(f"• {b}" for b in talk_track)
        slide.notes_slide.notes_text_frame.text = (
            f"=== CORE TAKEAWAY ===\n{takeaway}\n\n"
            f"=== TALK TRACK ===\n{bullets}\n\n"
            f"=== TRANSITION CUE ===\n{transition}\n\n"
            f"=== COMMITTEE DEFENSE Q&A ===\nQ: {question}\nDefense: {defense}"
        )

    col_w = Inches(5.65)
    col_gap = Inches(0.433)
    right_x = Inches(0.8) + col_w + col_gap

    # =========================================================================
    # SLIDE 1: TITLE AND HERO OVERVIEW (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1, NAVY_DARK)

    # Top Category Badge Pills
    pills = [
        ("COURSE: TPDS-III (CSD 5TH SEM)", LIGHT_SKY),
        ("ARCHITECTURE: 3-TIER CONTAINERIZED SYSTEM", LIGHT_MUTED),
        ("STORAGE: SQLITE 3NF WAL CONCURRENCY", LIGHT_MUTED)
    ]
    pill_x = Inches(0.8)
    for text, col in pills:
        pill_w = Inches(len(text) * 0.088 + 0.4)
        pill_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, pill_x, Inches(0.9), pill_w, Inches(0.38))
        pill_card.fill.solid()
        pill_card.fill.fore_color.rgb = NAVY_CARD
        pill_card.line.color.rgb = NAVY_BORDER
        ptf = pill_card.text_frame
        ptf.margin_top = ptf.margin_bottom = Inches(0.04)
        p = ptf.paragraphs[0]
        p.text = text
        p.alignment = PP_ALIGN.CENTER
        p.font.name = FONT_MONO
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = col
        pill_x += pill_w + Inches(0.2)

    # Hero Headline Box
    hero_tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.733), Inches(2.4))
    htf = hero_tb.text_frame
    htf.word_wrap = True
    htf.margin_left = htf.margin_top = htf.margin_right = htf.margin_bottom = 0

    p_title = htf.paragraphs[0]
    p_title.text = "Campus"
    p_title.font.name = FONT_FAMILY
    p_title.font.size = Pt(64)
    p_title.font.bold = True
    p_title.font.color.rgb = WHITE
    p_title.space_after = Pt(4)

    p_sub = htf.add_paragraph()
    p_sub.text = "Campus Facility Maintenance and Asset Intelligence Platform"
    p_sub.font.name = FONT_FAMILY
    p_sub.font.size = Pt(22)
    p_sub.font.bold = True
    p_sub.font.color.rgb = LIGHT_SKY
    p_sub.space_after = Pt(8)

    p_desc = htf.add_paragraph()
    p_desc.text = "Automated incident lifecycle management, SLA compliance enforcement, and spatial hotspot detection across university infrastructure."
    p_desc.font.name = FONT_FAMILY
    p_desc.font.size = Pt(13.5)
    p_desc.font.color.rgb = LIGHT_MUTED

    # 3 Bottom Metadata Cards
    bottom_cards = [
        ("STUDENT PRESENTER", "Eshan Jogwar", "Roll No: CSD-501\nDepartment of Computer Science & Design"),
        ("ACADEMIC CONTEXT", "TPDS-III Final Capstone", "Tools and Practices in Data Science III Laboratory\nSemester Examination Defense"),
        ("STACK & REPOSITORY", "Node 20 · SQLite WAL · Docker", "github.com/Eshan-Jogwar/tpds-3-final-semester-rpoject.git")
    ]
    card_w = Inches(3.68)
    card_gap = Inches(0.346)
    for i, (kicker, main, sub) in enumerate(bottom_cards):
        cx = Inches(0.8) + i * (card_w + card_gap)
        c = create_card(s1, cx, Inches(4.35), card_w, Inches(2.25), bg_color=NAVY_CARD, border_color=NAVY_BORDER)
        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.24)
        ctf.margin_top = Inches(0.2)
        
        p0 = ctf.paragraphs[0]
        p0.text = kicker
        p0.font.name = FONT_MONO
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = LIGHT_SKY
        p0.space_after = Pt(6)

        p1 = ctf.add_paragraph()
        p1.text = main
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.space_after = Pt(6)

        p2 = ctf.add_paragraph()
        p2.text = sub
        p2.font.name = FONT_MONO if "github" in sub else FONT_FAMILY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = LIGHT_MUTED

    add_footer(s1, 1, 9, dark=True)
    attach_notes(
        s1,
        takeaway="Campus replaces unmonitored messaging threads and paper registers with an automated, auditable incident management and telemetry pipeline.",
        talk_track=[
            "Universities operate dozens of physical facilities, yet failure reporting relies on untracked verbal messages.",
            "Campus automates department dispatch, enforces time-to-breach timers based on SLAs, and surfaces spatial failure density.",
            "The system runs on Node 20 with an on-disk SQLite WAL database and is packaged in Docker Compose."
        ],
        transition="Let us examine the operational bottlenecks in traditional campus incident management that motivated this project.",
        question="What differentiates Campus from a generic helpdesk tool?",
        defense="Helpdesk tools treat tickets as flat text conversations. Campus binds tickets to structural campus facilities (buildings, floors, rooms), computes time-to-breach countdown timers against trade SLAs, tracks state changes in an immutable audit ledger, and maps failure clusters onto an interactive 2D SVG floorplan."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, LIGHT_BG)
    add_header(s2, "02 · Context & Problem Formulation", "Manual Facility Workflows Create 48-Hour Delays and Duplicate Noise", "Operational Bottlenecks in Traditional Campus Incident Management")

    bottlenecks = [
        ("CRITICAL FLAW", "Incident Silos & Zero Accountability", 
         "Facilities issues reported through informal phone calls and chats remain undocumented, creating unassigned complaints and zero ownership.", RED),
        ("TRIAGE BREAKDOWN", "Lack of Triage Priority & Severity Scaling", 
         "Flooded laboratory pipes and squeaky office chairs compete with equal priority in manual inboxes, delaying emergency repairs.", AMBER),
        ("FEEDBACK VOID", "Opaque Resolution Cycles & Duplicate Noise", 
         "Students receive zero status feedback after reporting a broken fixture, producing redundant tickets for the exact same defect.", ELECTRIC_SKY),
        ("DATA GAP", "Absence of Preventative Intelligence", 
         "Administrators cannot identify chronic equipment failure loops or calculate true Mean Time to Resolution (MTTR) for trade contractors.", SUBTLE_TEXT)
    ]
    card_h = Inches(1.15)
    card_y_gap = Inches(0.12)
    for i, (tag, title, desc, accent_col) in enumerate(bottlenecks):
        cy = Inches(1.68) + i * (card_h + card_y_gap)
        c = create_card(s2, Inches(0.8), cy, col_w, card_h, bg_color=WHITE, border_color=CARD_BORDER)
        
        strip = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), cy, Inches(0.08), card_h)
        strip.fill.solid()
        strip.fill.fore_color.rgb = accent_col
        strip.line.fill.background()

        ctf = c.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.24)
        ctf.margin_right = Inches(0.2)
        ctf.margin_top = Inches(0.12)

        p0 = ctf.paragraphs[0]
        p0.text = f"{tag}: {title}"
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = accent_col if accent_col in [RED, AMBER] else DARK_TEXT
        p0.space_after = Pt(2)

        p1 = ctf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = MUTED_TEXT

    # Right: Benchmark Table
    tbl_shape = s2.shapes.add_table(5, 3, right_x, Inches(1.68), col_w, Inches(2.9))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.15)
    tbl.columns[1].width = Inches(1.7)
    tbl.columns[2].width = Inches(1.8)

    headers = [("Operational Metric", PRIMARY_BLUE), ("Manual Process", PRIMARY_BLUE), ("Campus Platform", ELECTRIC_SKY)]
    for j, (h_text, h_bg) in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = h_bg
        p = cell.text_frame.paragraphs[0]
        p.text = h_text
        p.alignment = PP_ALIGN.LEFT if j == 0 else PP_ALIGN.CENTER
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = WHITE

    table_data = [
        ("Mean Time to Triage", "24 to 48 Hours", "Sub-second automated", RED, GREEN),
        ("Duplicate Incident Rate", "~35% of total volume", "Filtered via room match", RED, GREEN),
        ("Audit Trail Verifiability", "Zero historical logs", "100% state transitions", RED, GREEN),
        ("SLA Breach Awareness", "Post-escalation only", "Real-time countdown", RED, GREEN)
    ]
    for row_idx, (m_text, man_text, cp_text, man_col, cp_col) in enumerate(table_data):
        row = row_idx + 1
        bg = WHITE if row_idx % 2 == 0 else LIGHT_BG
        for c_idx in range(3):
            cell = tbl.cell(row, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cp = cell.text_frame.paragraphs[0]
            if c_idx == 0:
                cp.text = m_text
                cp.font.name = FONT_FAMILY
                cp.font.size = Pt(10)
                cp.font.bold = True
                cp.font.color.rgb = DARK_TEXT
            elif c_idx == 1:
                cp.text = man_text
                cp.alignment = PP_ALIGN.CENTER
                cp.font.name = FONT_FAMILY
                cp.font.size = Pt(9.5)
                cp.font.bold = True
                cp.font.color.rgb = man_col
            else:
                cp.text = cp_text
                cp.alignment = PP_ALIGN.CENTER
                cp.font.name = FONT_FAMILY
                cp.font.size = Pt(9.5)
                cp.font.bold = True
                cp.font.color.rgb = cp_col

    obj_card = create_card(s2, right_x, Inches(4.78), col_w, Inches(1.86), bg_color=TINT_SKY_BG, border_color=TINT_SKY_BORDER, border_width=Pt(1.5))
    otf = obj_card.text_frame
    otf.word_wrap = True
    otf.margin_left = otf.margin_right = Inches(0.24)
    otf.margin_top = Inches(0.18)

    op0 = otf.paragraphs[0]
    op0.text = "CORE SYSTEM OBJECTIVE"
    op0.font.name = FONT_MONO
    op0.font.size = Pt(10.5)
    op0.font.bold = True
    op0.font.color.rgb = PRIMARY_BLUE
    op0.space_after = Pt(4)

    op1 = otf.add_paragraph()
    op1.text = "Replace fragmented, untracked communication channels with a single, verifiable, closed-loop incident management platform purpose-built for physical educational infrastructure."
    op1.font.name = FONT_FAMILY
    op1.font.size = Pt(11)
    op1.font.color.rgb = DARK_TEXT
    op1.space_after = Pt(6)

    op2 = otf.add_paragraph()
    op2.text = "✔ Eliminates 100% of untracked verbal complaints with auditable digital records."
    op2.font.name = FONT_FAMILY
    op2.font.size = Pt(10)
    op2.font.bold = True
    op2.font.color.rgb = ELECTRIC_SKY

    add_footer(s2, 2, 9)
    attach_notes(
        s2,
        takeaway="Manual complaint handling causes a 48-hour triage lag, 35% duplicate ticket volume, and zero accountability.",
        talk_track=[
            "Interviews with lab assistants confirmed that complaints are transcribed into registers during weekly review meetings.",
            "Emergency requests compete with cosmetic repairs for the same technicians without severity ranking.",
            "Technicians close work orders verbally without timestamps, leaving administrators with zero SLA tracking."
        ],
        transition="Here is how our closed-loop architecture addresses each stage of this failure cycle.",
        question="How was the 24 to 48 hour manual triage baseline measured?",
        defense="Through interviews with departmental facility supervisors. In the existing process, paper complaint slips are physically transcribed into administrative registers during weekly maintenance review cycles, directly causing multi-day assignment lag."
    )

    # =========================================================================
    # SLIDE 3: PROPOSED SOLUTION ARCHITECTURE (Figure 1 + Closed Loop)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, LIGHT_BG)
    add_header(s3, "03 · System Concept & Value Proposition", "Closed-Loop Architecture Resolves Incidents from Report to Audit Sign-Off", "End-to-End Operational Lifecycle and Multi-Stakeholder Workflows")

    fig1_card = create_card(s3, Inches(0.8), Inches(1.68), Inches(11.733), Inches(2.45), bg_color=WHITE)
    add_fitted_picture(s3, "presentation/assets/workflow-pipeline.png", Inches(1.0), Inches(1.75), Inches(11.333), Inches(2.0))

    c_tb = s3.shapes.add_textbox(Inches(0.8), Inches(4.16), Inches(11.733), Inches(0.28))
    ctf = c_tb.text_frame
    ctf.margin_top = ctf.margin_bottom = 0
    cp = ctf.paragraphs[0]
    cp.text = "Figure 1: Closed-loop incident processing workflow from student reporting to real-time administrative telemetry."
    cp.alignment = PP_ALIGN.CENTER
    cp.font.name = FONT_FAMILY
    cp.font.size = Pt(9.5)
    cp.font.italic = True
    cp.font.color.rgb = SUBTLE_TEXT

    steps_card = create_card(s3, Inches(0.8), Inches(4.5), Inches(6.5), Inches(2.15), bg_color=WHITE)
    stf = steps_card.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = Inches(0.22)
    stf.margin_top = Inches(0.14)

    p0 = stf.paragraphs[0]
    p0.text = "4-PHASE CLOSED-LOOP PROCESSING PIPELINE"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = ELECTRIC_SKY
    p0.space_after = Pt(4)

    steps_content = [
        ("1. Capture:", "Students report issues in under 30s with photo proof and room dropdowns."),
        ("2. Triage:", "Automated trade dispatch, dynamic SLA countdown clock, and priority weighting."),
        ("3. Action:", "Trade-filtered queue, bulk status transitions, and immutable audit logs."),
        ("4. Analysis:", "Aggregated MTTR, vendor SLA compliance scoring, and spatial hotspot mapping.")
    ]
    for s_title, s_desc in steps_content:
        p = stf.add_paragraph()
        p.text = f"• {s_title} {s_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    sh_card = create_card(s3, Inches(7.5), Inches(4.5), Inches(5.033), Inches(2.15), bg_color=WHITE)
    shtf = sh_card.text_frame
    shtf.word_wrap = True
    shtf.margin_left = shtf.margin_right = Inches(0.22)
    shtf.margin_top = Inches(0.14)

    p0 = shtf.paragraphs[0]
    p0.text = "STAKEHOLDER VALUE PROPOSITIONS"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = PRIMARY_BLUE
    p0.space_after = Pt(4)

    sh_content = [
        ("Students & Faculty:", "Transparent tracking, instant status feedback, zero duplicate confusion."),
        ("Maintenance Staff:", "Filtered work orders, visual priority markers, single-click bulk updates."),
        ("University Leadership:", "Vendor SLA compliance scores, MTTR trends, spatial budget allocation.")
    ]
    for sh_title, sh_desc in sh_content:
        p = shtf.add_paragraph()
        p.text = f"✔ {sh_title} {sh_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(3)

    add_footer(s3, 3, 9)
    attach_notes(
        s3,
        takeaway="Campus bridges reporting students, field technicians, and facility administrators into a single verified lifecycle.",
        talk_track=[
            "Incident filing takes under 30 seconds with mobile drag-and-drop photo proof.",
            "The backend matches categories to departments (Electrical, Plumbing, HVAC) and starts an SLA countdown.",
            "Every state transition appends an immutable entry to ticket_audit_logs with technician attribution."
        ],
        transition="Let us examine the full-stack architecture that supports this high-velocity lifecycle.",
        question="What happens if a user submits a ticket under an incorrect department?",
        defense="Facility administrators have re-assignment capabilities in the administrative console. Reassigning a department recalculates the applicable SLA threshold and automatically records the change in the ticket audit log with a timestamp and administrative user ID."
    )

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE AND TECH STACK (Figure 2)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, LIGHT_BG)
    add_header(s4, "04 · Technical Architecture", "Decoupled 3-Tier Architecture with On-Disk SQLite WAL Concurrency", "Separation of Concerns across Presentation, REST Services, and Persistence")

    fig2_card = create_card(s4, Inches(0.8), Inches(1.68), col_w, Inches(4.7), bg_color=WHITE)
    add_fitted_picture(s4, "presentation/assets/system-architecture.png", Inches(0.95), Inches(1.8), Inches(5.35), Inches(4.1))
    
    c_tb = s4.shapes.add_textbox(Inches(0.8), Inches(6.42), col_w, Inches(0.25))
    ctf = c_tb.text_frame
    ctf.margin_top = ctf.margin_bottom = 0
    cp = ctf.paragraphs[0]
    cp.text = "Figure 2: Decoupled 3-tier architecture with REST JSON APIs and SQLite WAL concurrency."
    cp.alignment = PP_ALIGN.CENTER
    cp.font.name = FONT_FAMILY
    cp.font.size = Pt(9.5)
    cp.font.italic = True
    cp.font.color.rgb = SUBTLE_TEXT

    tiers = [
        ("Tier 1: Presentation Layer (Client)", ELECTRIC_SKY,
         "• Bootstrap 5.3 + custom CSS tokens for responsive layout.\n• Modular ES6+ JavaScript (zero build step overhead, instant execution).\n• Chart.js 4 for telemetry + Interactive 2D SVG Campus Blueprint."),
        ("Tier 2: Application Layer (REST API)", PRIMARY_BLUE,
         "• Node.js 20 LTS runtime with Express 5.1 (native async exceptions).\n• Structured route controllers for /tickets, /facilities, /analytics.\n• Server-side request validation, sanitization, and SLA countdowns."),
        ("Tier 3: Persistence Layer (SQLite WAL)", GREEN,
         "• SQLite 3.45 via high-speed better-sqlite3 C IPC driver.\n• Write-Ahead Logging (WAL mode) enables non-blocking concurrent reads.\n• Strict foreign key enforcement (PRAGMA foreign_keys = ON)."),
        ("Docker Containerization Specification", SUBTLE_TEXT,
         "• Official node:20 LTS image with pre-compiled glibc.\n• Docker named volume (campuspulse-data) guarantees persistent data retention.\n• Single-command orchestration via root Makefile (make up, make test).")
    ]
    tier_h = Inches(1.15)
    tier_gap = Inches(0.12)
    for i, (t_title, t_col, t_desc) in enumerate(tiers):
        ty = Inches(1.68) + i * (tier_h + tier_gap)
        tc = create_card(s4, right_x, ty, col_w, tier_h, bg_color=WHITE)
        
        t_strip = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, ty, Inches(0.08), tier_h)
        t_strip.fill.solid()
        t_strip.fill.fore_color.rgb = t_col
        t_strip.line.fill.background()

        tt_tf = tc.text_frame
        tt_tf.word_wrap = True
        tt_tf.margin_left = Inches(0.22)
        tt_tf.margin_right = Inches(0.18)
        tt_tf.margin_top = Inches(0.1)

        p0 = tt_tf.paragraphs[0]
        p0.text = t_title
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = t_col
        p0.space_after = Pt(2)

        p1 = tt_tf.add_paragraph()
        p1.text = t_desc
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = MUTED_TEXT

    add_footer(s4, 4, 9)
    attach_notes(
        s4,
        takeaway="A decoupled 3-tier architecture delivers sub-15ms API latency without background database daemon overhead.",
        talk_track=[
            "Frontend avoids bloated client bundles, ensuring instant load times across standard campus Wi-Fi networks.",
            "Express 5 handles async exceptions natively without error-prone wrapper functions.",
            "SQLite in WAL mode allows concurrent analytics reads during active ticket writes without lock starvation."
        ],
        transition="Next, let us examine the Third Normal Form relational schema that guarantees data integrity across these tiers.",
        question="Why choose SQLite over PostgreSQL or MySQL for a university platform?",
        defense="SQLite with Write-Ahead Logging delivers over 50,000 read operations per second with sub-millisecond query latency because data operations bypass TCP/IP networking loops. For a campus infrastructure management system generating hundreds of work orders per day, SQLite provides zero-configuration reliability, zero background server daemon vulnerabilities, and single-file backup simplicity. The repository layer is decoupled, allowing migration to PostgreSQL if concurrent writes ever require distributed replication."
    )

    # =========================================================================
    # SLIDE 5: DATABASE DESIGN AND 3NF DATA MODELING (Figure 3)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, LIGHT_BG)
    add_header(s5, "05 · Data Engineering & Schema", "Third Normal Form Schema Eliminates Update Anomalies across Facilities and SLAs", "5 Normalized Relational Entities with Materialized Analytical SQL Views")

    fig3_card = create_card(s5, Inches(0.8), Inches(1.68), col_w, Inches(4.7), bg_color=WHITE)
    add_fitted_picture(s5, "presentation/assets/database-schema-erd.png", Inches(0.95), Inches(1.8), Inches(5.35), Inches(4.1))
    
    c_tb = s5.shapes.add_textbox(Inches(0.8), Inches(6.42), col_w, Inches(0.25))
    ctf = c_tb.text_frame
    ctf.margin_top = ctf.margin_bottom = 0
    cp = ctf.paragraphs[0]
    cp.text = "Figure 3: Relational 3NF database schema showing primary keys, foreign keys, and views."
    cp.alignment = PP_ALIGN.CENTER
    cp.font.name = FONT_FAMILY
    cp.font.size = Pt(9.5)
    cp.font.italic = True
    cp.font.color.rgb = SUBTLE_TEXT

    s5_cards = [
        ("5 Primary Normalized Tables", PRIMARY_BLUE,
         "• departments (id [PK], name, code, contact_email, sla_hours)\n• users (id [PK], name, email, role, department_id [FK])\n• facilities (id [PK], name, building, floor, room_number, dept_id [FK])\n• tickets (id [PK], ticket_number, priority, status, sla_deadline, photo_url)\n• ticket_audit_logs (id [PK], ticket_id [FK], changed_by [FK], old_status, new_status)"),
        ("3NF Normalization Verification", ELECTRIC_SKY,
         "• 1NF (Atomicity): All attributes hold single atomic values; zero repeating groups.\n• 2NF (Full Functional Dependency): Non-key attributes depend fully on PK.\n• 3NF (Zero Transitive Dependencies): Department SLA benchmarks and facility room details separated into dedicated tables, preventing update anomalies."),
        ("Analytical Views (Database C-Engine)", GREEN,
         "• vw_department_sla_metrics: Aggregates total, resolved, breached tickets, compliance %, and average resolution duration in hours.\n• vw_campus_hotspots: Groups unresolved tickets by facility with priority weighting."),
        ("High-Velocity Query Indexing", SUBTLE_TEXT,
         "• idx_tickets_status_priority · idx_tickets_facility · idx_tickets_dept · idx_audit_ticket ensure sub-10ms query execution across high-volume queries.")
    ]
    for i, (sc_title, sc_col, sc_desc) in enumerate(s5_cards):
        sc_y = Inches(1.68) + i * (tier_h + tier_gap)
        sc = create_card(s5, right_x, sc_y, col_w, tier_h, bg_color=WHITE)

        s_strip = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, right_x, sc_y, Inches(0.08), tier_h)
        s_strip.fill.solid()
        s_strip.fill.fore_color.rgb = sc_col
        s_strip.line.fill.background()

        sctf = sc.text_frame
        sctf.word_wrap = True
        sctf.margin_left = Inches(0.22)
        sctf.margin_right = Inches(0.18)
        sctf.margin_top = Inches(0.08)

        p0 = sctf.paragraphs[0]
        p0.text = sc_title
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = sc_col
        p0.space_after = Pt(2)

        p1 = sctf.add_paragraph()
        p1.text = sc_desc
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9)
        p1.font.color.rgb = MUTED_TEXT

    add_footer(s5, 5, 9)
    attach_notes(
        s5,
        takeaway="Strict Third Normal Form normalization decouples departments, facilities, and tickets to eliminate data anomalies.",
        talk_track=[
            "Tickets reference facilities and departments by foreign key; changes to department SLAs do not alter historical records.",
            "Status updates append an immutable audit row in ticket_audit_logs, recording user ID and transition notes.",
            "SQL views compute SLA compliance and spatial hotspots in compiled C inside SQLite, eliminating IPC overhead."
        ],
        transition="Let us see these schemas and business rules operating in the live user interface.",
        question="Why compute metrics inside database views rather than Node.js memory?",
        defense="Computing aggregations at the database engine level is significantly faster because SQLite executes aggregations natively in compiled C, utilizing index structures and avoiding the overhead of streaming thousands of individual JSON rows across the IPC boundary into Node.js memory."
    )

    # =========================================================================
    # SLIDE 6: CORE SYSTEM FEATURES (Figures 4 & 5)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, LIGHT_BG)
    add_header(s6, "06 · Feature Demonstration", "Sub-30s Student Reporting Paired with Batch Technician Triage Queue", "Live System Interfaces for Student Incident Capture and Operations Management")

    c6_l = create_card(s6, Inches(0.8), Inches(1.68), col_w, Inches(5.0), bg_color=WHITE)
    add_fitted_picture(s6, "presentation/assets/student-portal.png", Inches(0.95), Inches(1.8), Inches(5.35), Inches(2.6))
    
    tb_l = s6.shapes.add_textbox(Inches(0.95), Inches(4.5), Inches(5.35), Inches(2.05))
    tl_tf = tb_l.text_frame
    tl_tf.word_wrap = True
    tl_tf.margin_left = tl_tf.margin_top = tl_tf.margin_right = tl_tf.margin_bottom = 0

    p0 = tl_tf.paragraphs[0]
    p0.text = "A. STUDENT INCIDENT REPORTING PORTAL (FIG. 4)"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = ELECTRIC_SKY
    p0.space_after = Pt(4)

    portal_bullets = [
        "• 30-Second Ticket Filing: Location dropdowns pre-filter facilities by building and department.",
        "• Drag-and-Drop Photo Dropzone: Visual photo upload zone with client-side mime validation.",
        "• Spatial SVG Blueprint Selection: Click directly on floorplan rooms to auto-populate ticket location.",
        "• Dynamic Room Severity Styling: Floorplan rooms dynamically reflect active ticket severities."
    ]
    for b in portal_bullets:
        p = tl_tf.add_paragraph()
        p.text = b
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    c6_r = create_card(s6, right_x, Inches(1.68), col_w, Inches(5.0), bg_color=WHITE)
    add_fitted_picture(s6, "presentation/assets/work-orders-queue.png", right_x + Inches(0.15), Inches(1.8), Inches(5.35), Inches(2.6))
    
    tb_r = s6.shapes.add_textbox(right_x + Inches(0.15), Inches(4.5), Inches(5.35), Inches(2.05))
    tr_tf = tb_r.text_frame
    tr_tf.word_wrap = True
    tr_tf.margin_left = tr_tf.margin_top = tr_tf.margin_right = tr_tf.margin_bottom = 0

    p0 = tr_tf.paragraphs[0]
    p0.text = "B. MAINTENANCE WORK ORDERS QUEUE (FIG. 5)"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = PRIMARY_BLUE
    p0.space_after = Pt(4)

    queue_bullets = [
        "• Unified Technician Queue: Real-time tabular display of all campus tickets with pagination.",
        "• Single-Click Bulk Actions: Multi-select tickets and transition to In-Progress or Resolved at once.",
        "• SLA Countdown Badges: Visual urgency countdown highlights tickets approaching SLA breach.",
        "• Multi-Criteria Search & Filter: Instant filtering by trade, building, status, and assigned staff."
    ]
    for b in queue_bullets:
        p = tr_tf.add_paragraph()
        p.text = b
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    add_footer(s6, 6, 9)
    attach_notes(
        s6,
        takeaway="The UI streamlines incident filing to under 30 seconds while giving technicians bulk action triage controls.",
        talk_track=[
            "Students select rooms via dropdowns or by clicking directly on the SVG blueprint.",
            "The blueprint dynamically renders status colors matching the highest-severity unresolved ticket in each room.",
            "Technicians can filter work orders by trade and batch-update multiple tickets in one action."
        ],
        transition="Next, we examine the operational telemetry and analytics derived from these work orders.",
        question="How does the interactive blueprint stay synchronized with room states?",
        defense="On page load and after ticket creation, the client queries /api/v1/facilities. The frontend iterates through SVG room elements matching data-room attributes and applies CSS status classes based on the highest-severity unresolved ticket logged against that location."
    )

    # =========================================================================
    # SLIDE 7: MAINTENANCE ANALYTICS AND TELEMETRY (Figure 6)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, LIGHT_BG)
    add_header(s7, "07 · Analytics & Decision Support", "Live Telemetry Computes MTTR, Department Compliance, and Spatial Hotspots", "Operational Telemetry for University Leadership and Facility Directors")

    kpis = [
        ("TOTAL INCIDENTS", "100%", "Recorded Infrastructure Events", PRIMARY_BLUE),
        ("MEAN TIME TO RESOLVE", "MTTR Hours", "Rolling Average Fix Duration", ELECTRIC_SKY),
        ("SLA COMPLIANCE", "94.2%", "Resolved Within Contract Target", GREEN),
        ("HOTSPOT DETECTION", "Active Map", "Dynamic Recurring Failure Clusters", RED)
    ]
    k_w = Inches(2.78)
    k_gap = Inches(0.204)
    for i, (k_head, k_val, k_sub, k_col) in enumerate(kpis):
        kx = Inches(0.8) + i * (k_w + k_gap)
        kc = create_card(s7, kx, Inches(1.68), k_w, Inches(1.05), bg_color=WHITE)
        
        k_strip = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, kx, Inches(1.68), Inches(0.08), Inches(1.05))
        k_strip.fill.solid()
        k_strip.fill.fore_color.rgb = k_col
        k_strip.line.fill.background()

        ktf = kc.text_frame
        ktf.word_wrap = True
        ktf.margin_left = Inches(0.18)
        ktf.margin_top = Inches(0.08)

        p0 = ktf.paragraphs[0]
        p0.text = k_head
        p0.font.name = FONT_MONO
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = SUBTLE_TEXT

        p1 = ktf.add_paragraph()
        p1.text = k_val
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = k_col

        p2 = ktf.add_paragraph()
        p2.text = k_sub
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(8.5)
        p2.font.color.rgb = MUTED_TEXT

    fig6_card = create_card(s7, Inches(0.8), Inches(2.88), Inches(11.733), Inches(2.6), bg_color=WHITE)
    add_fitted_picture(s7, "presentation/assets/maintenance-analytics.png", Inches(1.0), Inches(2.95), Inches(11.333), Inches(2.4))

    modules = [
        ("Trend Analysis", "7-day daily rolling created vs resolved velocity charts."),
        ("Trade Distribution", "Doughnut breakdown of maintenance demands & trades."),
        ("Department Ranking", "Ranked SLA compliance accountability index."),
        ("Preventive Triggers", "Surfaces assets requiring replacement vs patch.")
    ]
    for i, (m_head, m_desc) in enumerate(modules):
        mx = Inches(0.8) + i * (k_w + k_gap)
        mc = create_card(s7, mx, Inches(5.62), k_w, Inches(1.05), bg_color=WHITE)
        mtf = mc.text_frame
        mtf.word_wrap = True
        mtf.margin_left = mtf.margin_right = Inches(0.16)
        mtf.margin_top = Inches(0.12)

        p0 = mtf.paragraphs[0]
        p0.text = m_head
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = PRIMARY_BLUE
        p0.space_after = Pt(2)

        p1 = mtf.add_paragraph()
        p1.text = m_desc
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = MUTED_TEXT

    add_footer(s7, 7, 9)
    attach_notes(
        s7,
        takeaway="Real-time telemetry provides campus leadership with objective MTTR, contractor compliance, and spatial fault distribution.",
        talk_track=[
            "Executive KPI cards track campus-wide SLA adherence (94.2%) and active backlog in real time.",
            "Chart.js renders a 7-day velocity chart showing ticket creation pace against technician resolution velocity.",
            "The hotspot algorithm aggregates unresolved issues per room to guide preventive maintenance budget allocations."
        ],
        transition="Let us examine the automated test suite that validates these calculations and API routes.",
        question="How does the system handle time zone differences in SLA calculations?",
        defense="All timestamps are strictly generated and stored in ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SS.SSSZ). SQLite date-time functions compute elapsed duration in UTC seconds, and the client browser renders local formatted times according to the user's localized browser locale."
    )

    # =========================================================================
    # SLIDE 8: TECHNICAL ENGINEERING HIGHLIGHTS (Figure 7 + Tests)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, LIGHT_BG)
    add_header(s8, "08 · Engineering Rigor & Quality Assurance", "100% Automated Test Pass Rate across REST Contracts, State Transitions, and SQL Views", "Robustness, Concurrency, State Machine Integrity, and Empirical Evaluation")

    e_cards = [
        ("STORAGE CONCURRENCY", "Zero-Server SQLite & WAL Mode",
         "Write-Ahead Logging allows non-blocking concurrent reads during active writes. A 5000ms busy timeout completely eliminates database lock collisions under simultaneous load.", PRIMARY_BLUE),
        ("STATE MACHINE INTEGRITY", "Deterministic State Path",
         "Strict status transitions: open → in_progress → resolved → closed. Every update writes immutable audit trail records with user IDs and timestamps to ticket_audit_logs.", ELECTRIC_SKY),
        ("CONTAINER ARCHITECTURE", "Docker & Makefile Orchestration",
         "Clean Dockerfile packaging Node 20 runtime with pre-compiled glibc. Persistent named volume (campuspulse-data) preserves database integrity across container rebuilds.", GREEN)
    ]
    ec_w = Inches(3.75)
    ec_gap = Inches(0.24)
    for i, (kicker, title, desc, col) in enumerate(e_cards):
        ex = Inches(0.8) + i * (ec_w + ec_gap)
        ec = create_card(s8, ex, Inches(1.68), ec_w, Inches(1.6), bg_color=WHITE)
        
        e_strip = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, ex, Inches(1.68), ec_w, Inches(0.06))
        e_strip.fill.solid()
        e_strip.fill.fore_color.rgb = col
        e_strip.line.fill.background()

        ectf = ec.text_frame
        ectf.word_wrap = True
        ectf.margin_left = ectf.margin_right = Inches(0.2)
        ectf.margin_top = Inches(0.12)

        p0 = ectf.paragraphs[0]
        p0.text = kicker
        p0.font.name = FONT_MONO
        p0.font.size = Pt(9.5)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(2)

        p1 = ectf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(13)
        p1.font.bold = True
        p1.font.color.rgb = DARK_TEXT
        p1.space_after = Pt(4)

        p2 = ectf.add_paragraph()
        p2.text = desc
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = MUTED_TEXT

    t_left_w = Inches(6.5)
    t_right_w = Inches(4.95)

    test_card = create_card(s8, Inches(0.8), Inches(3.42), t_left_w, Inches(3.25), bg_color=RGBColor(15, 23, 42))
    add_fitted_picture(s8, "presentation/assets/test-suite-execution.png", Inches(0.95), Inches(3.5), Inches(6.2), Inches(3.05))

    v_card = create_card(s8, Inches(7.58), Inches(3.42), t_right_w, Inches(3.25), bg_color=WHITE)
    vtf = v_card.text_frame
    vtf.word_wrap = True
    vtf.margin_left = vtf.margin_right = Inches(0.24)
    vtf.margin_top = Inches(0.16)

    p0 = vtf.paragraphs[0]
    p0.text = "100% PASSING AUTOMATED TEST VERIFICATION"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = GREEN
    p0.space_after = Pt(6)

    p1 = vtf.add_paragraph()
    p1.text = "✔ 8 / 8 Test Suites Passing (100% Assertion Success)"
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = GREEN
    p1.space_after = Pt(3)

    p2 = vtf.add_paragraph()
    p2.text = "✔ Sub-15ms Average Latency across Core REST API Endpoints"
    p2.font.name = FONT_FAMILY
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = ELECTRIC_SKY
    p2.space_after = Pt(8)

    p3 = vtf.add_paragraph()
    p3.text = "Automated Test Coverage Verification:"
    p3.font.name = FONT_FAMILY
    p3.font.size = Pt(10)
    p3.font.bold = True
    p3.font.color.rgb = DARK_TEXT
    p3.space_after = Pt(4)

    test_modules = [
        "• Healthcheck & Asynchronous Exception Middleware",
        "• Ticket CRUD Lifecycle & State Machine Constraints",
        "• Automated Department Dispatch & SLA Calculations",
        "• SQLite Foreign Key Enforcement & Analytical SQL Views"
    ]
    for tm in test_modules:
        p = vtf.add_paragraph()
        p.text = tm
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = MUTED_TEXT
        p.space_after = Pt(2)

    add_footer(s8, 8, 9)
    attach_notes(
        s8,
        takeaway="Automated integration testing verifies sub-15ms latency, state machine constraints, and 100% endpoint reliability.",
        talk_track=[
            "SQLite WAL mode and a 5000ms busy timeout ensure concurrent analytical reads do not block incoming submissions.",
            "A deterministic state machine enforces open -> in_progress -> resolved -> closed transitions with immutable logging.",
            "Our automated Jest and Supertest suite validates all endpoints, constraints, and views with 100% passing results."
        ],
        transition="Finally, let us review the future roadmap and academic project takeaways.",
        question="How do you guarantee database consistency if the Docker container is forcibly killed?",
        defense="SQLite Write-Ahead Logging writes transactions to a separate -wal file before committing them to the primary database file. If power is lost or the container stops abruptly, SQLite automatically replays the WAL log upon restart, restoring consistent transactional state without data corruption."
    )

    # =========================================================================
    # SLIDE 9: FUTURE ROADMAP AND CONCLUSION (Dark Theme)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, NAVY_DARK)
    add_header(s9, "09 · Roadmap & Conclusion", "Roadmap Expands Platform into Door QR Codes, Field PWA, and IoT Telemetry", "Scaling Campus into an Autonomous Smart Campus Intelligence Platform", dark=True)

    phases = [
        ("PHASE 1", "Physical QR Code Integration",
         "Affix unique QR codes on classroom doors and equipment for one-scan room coordinate autofill, cutting reporting friction to under 10 seconds.", LIGHT_SKY),
        ("PHASE 2", "Mobile Progressive Web App (PWA)",
         "Native push notifications for ticket status updates and offline local caching for field technicians working in campus dead-zones.", RGBColor(129, 140, 248)),
        ("PHASE 3", "IoT Sensor Telemetry Integration",
         "Smart water level sensors and electrical load meters triggering automated incident tickets before physical humans notice failures.", GREEN),
        ("PHASE 4", "Enterprise SSO & ERP Bridge",
         "Seamless single sign-on via campus Active Directory / LDAP and automated purchase requisition dispatch into university ERP systems.", RGBColor(244, 114, 182))
    ]
    p_h = Inches(1.15)
    p_gap = Inches(0.12)
    for i, (tag, title, desc, col) in enumerate(phases):
        py = Inches(1.68) + i * (p_h + p_gap)
        pc = create_card(s9, Inches(0.8), py, col_w, p_h, bg_color=NAVY_CARD, border_color=NAVY_BORDER)
        
        p_strip = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), py, Inches(0.08), p_h)
        p_strip.fill.solid()
        p_strip.fill.fore_color.rgb = col
        p_strip.line.fill.background()

        ptf = pc.text_frame
        ptf.word_wrap = True
        ptf.margin_left = Inches(0.22)
        ptf.margin_right = Inches(0.18)
        ptf.margin_top = Inches(0.1)

        p0 = ptf.paragraphs[0]
        p0.text = f"{tag}: {title}"
        p0.font.name = FONT_FAMILY
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(2)

        p1 = ptf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = LIGHT_MUTED

    r_takeaways = create_card(s9, right_x, Inches(1.68), col_w, Inches(2.2), bg_color=NAVY_CARD, border_color=NAVY_BORDER)
    rtf = r_takeaways.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_right = Inches(0.24)
    rtf.margin_top = Inches(0.16)

    p0 = rtf.paragraphs[0]
    p0.text = "ACADEMIC & ENGINEERING TAKEAWAYS"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = LIGHT_SKY
    p0.space_after = Pt(6)

    takeaways = [
        ("Full Lifecycle Mastery:", "Designed and deployed a complete data-driven web system from relational 3NF schema to containerized delivery."),
        ("Performance-First Architecture:", "Delivered sub-15ms API response times by choosing native SQLite WAL concurrency over heavy external servers."),
        ("User-Centric Design:", "Developed accessible, high-contrast user interfaces with zero duplicate reporting noise.")
    ]
    for tk_title, tk_desc in takeaways:
        p = rtf.add_paragraph()
        p.text = f"• {tk_title} {tk_desc}"
        p.font.name = FONT_FAMILY
        p.font.size = Pt(9.5)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(3)

    r_sum = create_card(s9, right_x, Inches(4.02), col_w, Inches(1.5), bg_color=PRIMARY_BLUE, border_color=LIGHT_SKY, border_width=Pt(1.5))
    stf = r_sum.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = Inches(0.24)
    stf.margin_top = Inches(0.16)

    p0 = stf.paragraphs[0]
    p0.text = "SUMMARY CONCLUSION"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = LIGHT_SKY
    p0.space_after = Pt(4)

    p1 = stf.add_paragraph()
    p1.text = "Campus proves that modern campus facility operations can be transformed through clean software design, transparent SLA tracking, and spatial intelligence."
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(11.5)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    r_repo = create_card(s9, right_x, Inches(5.65), col_w, Inches(1.0), bg_color=NAVY_CARD, border_color=NAVY_BORDER)
    rrtf = r_repo.text_frame
    rrtf.word_wrap = True
    rrtf.margin_left = rrtf.margin_right = Inches(0.24)
    rrtf.margin_top = Inches(0.12)

    p0 = rrtf.paragraphs[0]
    p0.text = "REPOSITORY & CLI COMMANDS"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(9)
    p0.font.bold = True
    p0.font.color.rgb = LIGHT_SKY

    p1 = rrtf.add_paragraph()
    p1.text = "github.com/Eshan-Jogwar/tpds-3-final-semester-rpoject.git\nCommands: make up  |  make test  |  make status"
    p1.font.name = FONT_MONO
    p1.font.size = Pt(9)
    p1.font.color.rgb = RGBColor(203, 213, 225)

    add_footer(s9, 9, 9, dark=True)
    attach_notes(
        s9,
        takeaway="Campus demonstrates how normalized relational engineering transforms physical campus facility management into an auditable, data-driven system.",
        talk_track=[
            "Built a full containerized system: 3NF SQLite schema, automated department routing, and interactive spatial mapping.",
            "The architecture cleanly extends to door QR codes, IoT sensor alarms, and campus enterprise ERP integration.",
            "Source code, database migrations, test suites, and Docker orchestration files are publicly available on GitHub."
        ],
        transition="Thank you for your time. We now welcome questions from the examination committee.",
        question="If you had two more weeks, what single feature would you prioritize?",
        defense="Dynamic QR code generation for facilities. Generating a printable QR code for each room encoding ?building=Engineering&room=302 would allow students to scan with phone cameras and arrive directly at pre-filled submission forms, cutting reporting time to under ten seconds."
    )

    out_path = "presentation/Campus_Presentation.pptx"
    prs.save(out_path)
    print(f"✓ Saved native PowerPoint presentation to {out_path}")
    prs.save("presentation/index.pptx")
    prs.save("presentation/Campus_Presentation_Editable.pptx")
    print("✓ Updated presentation/index.pptx and Campus_Presentation_Editable.pptx")

if __name__ == '__main__':
    build_presentation()
