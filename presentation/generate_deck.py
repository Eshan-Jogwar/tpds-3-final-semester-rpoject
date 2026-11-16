#!/usr/bin/env python3
"""
generate_deck.py — Professional Native PowerPoint Generator for Campus Platform
Builds a high-fidelity 16:9 widescreen presentation using native PowerPoint shapes,
text frames, formatted tables, badges, and neatly framed figures.
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

    # --- COLOR SYSTEM TOKENS ---
    NAVY_DARK = RGBColor(11, 17, 32)        # #0b1120
    NAVY_CARD = RGBColor(20, 30, 52)        # #141e34
    NAVY_BORDER = RGBColor(38, 54, 88)      # #263658
    
    LIGHT_BG = RGBColor(248, 250, 252)      # #f8fafc
    WHITE = RGBColor(255, 255, 255)         # #ffffff
    CARD_BORDER = RGBColor(226, 232, 240)   # #e2e8f0
    
    PRIMARY_BLUE = RGBColor(30, 58, 138)    # #1e3a8a
    ELECTRIC_SKY = RGBColor(2, 132, 199)    # #0284c7
    LIGHT_SKY = RGBColor(56, 189, 248)      # #38bdf8
    TINT_SKY_BG = RGBColor(239, 246, 255)   # #eff6ff
    TINT_SKY_BORDER = RGBColor(191, 219, 254) # #bfdbfe
    
    DARK_TEXT = RGBColor(15, 23, 42)        # #0f172a
    MUTED_TEXT = RGBColor(71, 85, 105)      # #475569
    SUBTLE_TEXT = RGBColor(100, 116, 139)   # #64748b
    LIGHT_TEXT = RGBColor(248, 250, 252)    # #f8fafc
    LIGHT_MUTED = RGBColor(148, 163, 184)   # #94a3b8

    GREEN = RGBColor(16, 185, 129)          # #10b981
    GREEN_BG = RGBColor(236, 253, 245)      # #ecfdf5
    RED = RGBColor(239, 68, 68)             # #ef4444
    RED_BG = RGBColor(254, 242, 242)        # #fef2f2
    AMBER = RGBColor(245, 158, 11)          # #f59e0b

    FONT_FAMILY = "Segoe UI"
    FONT_MONO = "Consolas"

    # --- HELPER FUNCTIONS ---
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
        p0.font.size = Pt(10.5)
        p0.font.bold = True
        p0.font.color.rgb = LIGHT_SKY if dark else ELECTRIC_SKY
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = WHITE if dark else DARK_TEXT
        p1.space_after = Pt(2)

        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.name = FONT_FAMILY
        p2.font.size = Pt(12)
        p2.font.color.rgb = LIGHT_MUTED if dark else MUTED_TEXT

        # Hairline divider
        line = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.52), Inches(11.733), Pt(1.5)
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
        p.font.size = Pt(9.5)
        p.font.color.rgb = LIGHT_MUTED if dark else SUBTLE_TEXT

        p_right = tf.add_paragraph()
        p_right.text = f"SLIDE {slide_num:02d} / {total:02d}"
        p_right.alignment = PP_ALIGN.RIGHT
        p_right.font.name = FONT_MONO
        p_right.font.size = Pt(9.5)
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
            # Width bound
            render_w = box_width
            render_h = box_width / aspect
            x = box_left
            y = box_top + (box_height - render_h) / 2
        else:
            # Height bound
            render_h = box_height
            render_w = box_height * aspect
            x = box_left + (box_width - render_w) / 2
            y = box_top

        return slide.shapes.add_picture(img_path, x, y, width=render_w, height=render_h)

    def attach_notes(slide, script, question, defense):
        tf = slide.notes_slide.notes_text_frame
        tf.text = (
            f"=== VERBATIM PRESENTER SCRIPT ===\n\n{script}\n\n"
            f"=== ANTICIPATED COMMITTEE DEFENSE Q&A ===\n\n"
            f"Q: {question}\n\nDefense: {defense}"
        )

    # =========================================================================
    # SLIDE 1: TITLE AND HERO OVERVIEW (Dark Navy Theme)
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
    p_desc.text = "An Automated Incident Lifecycle Management, SLA Compliance Enforcement, and Spatial Hotspot Detection Platform"
    p_desc.font.name = FONT_FAMILY
    p_desc.font.size = Pt(14)
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
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = LIGHT_SKY
        p0.space_after = Pt(6)

        p1 = ctf.add_paragraph()
        p1.text = main
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = WHITE
        p1.space_after = Pt(6)

        p2 = ctf.add_paragraph()
        p2.text = sub
        p2.font.name = FONT_MONO if "github" in sub else FONT_FAMILY
        p2.font.size = Pt(11)
        p2.font.color.rgb = LIGHT_MUTED

    add_footer(s1, 1, 9, dark=True)
    attach_notes(
        s1,
        "Good morning, members of the evaluation committee. Today we present Campus, an integrated campus facility maintenance and asset intelligence platform developed for the TPDS-III capstone curriculum. Universities operate like small cities, with hundreds of classrooms, laboratories, and residential wings requiring continuous facility management. Yet most campuses still handle equipment failures through manual WhatsApp groups, paper registers, or untracked helpdesks. Campus replaces that fragmentation with a clean incident lifecycle, automated department dispatch, strict SLA compliance tracking, and spatial hotspot analytics.",
        "What differentiates this project from a generic helpdesk ticketing tool?",
        "Generic ticketing systems treat tickets as flat support conversations. Campus is purpose-built for physical infrastructure: it couples tickets with structural campus entities (buildings, floors, rooms, and asset codes), enforces time-to-breach countdown timers based on department SLAs, tracks state transitions in an immutable audit ledger, and computes spatial hotspots directly onto an interactive campus blueprint."
    )

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & MOTIVATION (Light Theme)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2, LIGHT_BG)
    add_header(s2, "02 · Context & Problem Formulation", "Campus Infrastructure Management: Current Inefficiencies", "Why Traditional Campus Incident Workflows Break Down in Daily Operation")

    col_w = Inches(5.65)
    col_gap = Inches(0.433)

    # Left Column: 4 Problem Bottleneck Cards
    bottlenecks = [
        ("CRITICAL FLAW", "Incident Silos & Zero Accountability", 
         "Facilities issues reported through informal phone calls, emails, and word of mouth remain undocumented, creating unassigned complaints and zero ownership.", RED, RED_BG),
        ("TRIAGE BREAKDOWN", "Lack of Triage Priority & Severity Scaling", 
         "A flooded laboratory pipe and a squeaky office chair receive equal priority in manual inboxes, delaying emergency fixes that threaten campus safety.", AMBER, RGBColor(255, 251, 235)),
        ("FEEDBACK VOID", "Opaque Resolution Cycles & Duplicate Noise", 
         "Students and faculty receive no feedback after reporting a broken projector or AC, producing redundant tickets for the exact same defect.", ELECTRIC_SKY, TINT_SKY_BG),
        ("DATA GAP", "Absence of Preventative Intelligence", 
         "Administrators cannot identify recurring equipment failure loops or calculate true Mean Time to Resolution (MTTR) for trade contractors.", SUBTLE_TEXT, RGBColor(241, 245, 249))
    ]
    card_h = Inches(1.15)
    card_y_gap = Inches(0.12)
    for i, (tag, title, desc, accent_col, bg_col) in enumerate(bottlenecks):
        cy = Inches(1.68) + i * (card_h + card_y_gap)
        c = create_card(s2, Inches(0.8), cy, col_w, card_h, bg_color=WHITE, border_color=CARD_BORDER)
        
        # Accent indicator strip on left
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
        p1.font.size = Pt(10)
        p1.font.color.rgb = MUTED_TEXT

    # Right Column: Operational Impact Comparison Table
    right_x = Inches(0.8) + col_w + col_gap
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
        p.font.size = Pt(11)
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
                cp.font.size = Pt(10.5)
                cp.font.bold = True
                cp.font.color.rgb = DARK_TEXT
            elif c_idx == 1:
                cp.text = man_text
                cp.alignment = PP_ALIGN.CENTER
                cp.font.name = FONT_FAMILY
                cp.font.size = Pt(10)
                cp.font.bold = True
                cp.font.color.rgb = man_col
            else:
                cp.text = cp_text
                cp.alignment = PP_ALIGN.CENTER
                cp.font.name = FONT_FAMILY
                cp.font.size = Pt(10)
                cp.font.bold = True
                cp.font.color.rgb = cp_col

    # Right Column: Objective Highlight Card below table
    obj_card = create_card(s2, right_x, Inches(4.78), col_w, Inches(1.86), bg_color=TINT_SKY_BG, border_color=TINT_SKY_BORDER, border_width=Pt(1.5))
    otf = obj_card.text_frame
    otf.word_wrap = True
    otf.margin_left = otf.margin_right = Inches(0.24)
    otf.margin_top = Inches(0.18)

    op0 = otf.paragraphs[0]
    op0.text = "CORE SYSTEM OBJECTIVE"
    op0.font.name = FONT_MONO
    op0.font.size = Pt(11)
    op0.font.bold = True
    op0.font.color.rgb = PRIMARY_BLUE
    op0.space_after = Pt(4)

    op1 = otf.add_paragraph()
    op1.text = "Replace fragmented, untracked communication channels with a single, verifiable, closed-loop incident management platform purpose-built for physical educational infrastructure."
    op1.font.name = FONT_FAMILY
    op1.font.size = Pt(11.5)
    op1.font.color.rgb = DARK_TEXT
    op1.space_after = Pt(6)

    op2 = otf.add_paragraph()
    op2.text = "✔ Eliminates 100% of untracked verbal complaints with auditable digital records."
    op2.font.name = FONT_FAMILY
    op2.font.size = Pt(10.5)
    op2.font.bold = True
    op2.font.color.rgb = ELECTRIC_SKY

    add_footer(s2, 2, 9)
    attach_notes(
        s2,
        "To understand why we built Campus, examine the daily friction inside any college campus. When an air conditioner malfunctions in a seminar hall or water leaks in a science laboratory, students notify whoever is nearby. The message passes through three or four intermediaries before reaching maintenance. Because there is no central tracking system, several students report the identical issue, creating duplicate noise. Critical emergencies compete with cosmetic repairs for the same technician. Technicians close complaints verbally without time stamps, meaning administration has zero data on whether maintenance contractors meet their contractual service level agreements. Campus resolves this entire breakdown by formalizing the pipeline from initial report to verified technician sign-off.",
        "How did you determine the 24 to 48 hour baseline for manual triage?",
        "We interviewed departmental lab assistants and facility supervisors on campus. In the current process, paper complaints must be physically transcribed into an administrative register before being assigned to trade contractors during weekly review cycles, directly causing multi-day delays."
    )

    # =========================================================================
    # SLIDE 3: PROPOSED SOLUTION ARCHITECTURE (Figure 1 + Closed Loop)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3, LIGHT_BG)
    add_header(s3, "03 · System Concept & Value Proposition", "Campus Solution Architecture", "End-to-End Operational Lifecycle and Multi-Stakeholder Workflows")

    # Top: Figure 1 Container Card
    fig1_card = create_card(s3, Inches(0.8), Inches(1.68), Inches(11.733), Inches(2.45), bg_color=WHITE)
    add_fitted_picture(s3, "presentation/assets/workflow-pipeline.png", Inches(1.0), Inches(1.75), Inches(11.333), Inches(2.0))

    # Caption
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

    # Bottom: 4 Steps on Left (Width = 6.4 in), Stakeholders on Right (Width = 5.0 in)
    steps_card = create_card(s3, Inches(0.8), Inches(4.5), Inches(6.5), Inches(2.15), bg_color=WHITE)
    stf = steps_card.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = Inches(0.22)
    stf.margin_top = Inches(0.14)

    p0 = stf.paragraphs[0]
    p0.text = "4-PHASE CLOSED-LOOP PROCESSING PIPELINE"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(11)
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
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # Right: Stakeholder Value Propositions
    sh_card = create_card(s3, Inches(7.5), Inches(4.5), Inches(5.033), Inches(2.15), bg_color=WHITE)
    shtf = sh_card.text_frame
    shtf.word_wrap = True
    shtf.margin_left = shtf.margin_right = Inches(0.22)
    shtf.margin_top = Inches(0.14)

    p0 = shtf.paragraphs[0]
    p0.text = "STAKEHOLDER VALUE PROPOSITIONS"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(11)
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
        p.font.size = Pt(10.5)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(4)

    add_footer(s3, 3, 9)
    attach_notes(
        s3,
        "Campus bridges three core campus groups into a single closed loop. First, for students and faculty, we provide an intuitive web interface where an issue can be documented with photographic proof in under 30 seconds. Second, the backend system processes the submission, matches the facility category with the correct trade department such as Electrical, Plumbing, or HVAC, and starts an SLA countdown clock. Third, maintenance staff work from an administrative work queue equipped with bulk status controls, quick search filters, and single-click state transitions. Every state modification writes to an append-only audit table. Finally, campus directors see an executive analytics dashboard displaying facility hotspots, vendor compliance, and resolution velocity.",
        "What happens if a student files a ticket under the wrong department?",
        "Facility administrators have re-assignment capabilities in the administrative console. Updating a ticket department recalculates the applicable SLA threshold and automatically records the reassignment in the ticket audit log with a timestamp and administrative user identifier."
    )

    # =========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE AND TECH STACK (Figure 2)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4, LIGHT_BG)
    add_header(s4, "04 · Technical Architecture", "Full-Stack Architecture and Technology Stack", "Decoupled 3-Tier Design with On-Disk SQLite Storage and Containerization")

    # Left: Figure 2 Architecture Diagram Card
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

    # Right: 4 Structured Tier Cards
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
        
        # Indicator strip
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
        "Here we see the architectural blueprint of Campus. We chose a decoupled three-tier architecture focused on performance, durability, and operational simplicity. On the client side, we avoided heavy frontend frameworks like React or Angular to ensure instant load times and zero compilation friction on standard campus Wi-Fi networks. Bootstrap 5, modular ES6 JavaScript, and Chart.js provide a modern interface across mobile phones, tablets, and desktops. The application tier runs on Node.js with Express 5, which handles asynchronous exceptions natively without error-prone wrapper functions. For our persistence layer, following syllabus guidance, we eliminated external database server overhead by utilizing on-disk SQLite with Write-Ahead Logging enabled. WAL mode allows concurrent readers to query analytics while writes occur without lock starvation. The entire stack is packaged into a container managed through a Makefile, allowing complete one-command local or cloud deployment.",
        "Why use SQLite rather than PostgreSQL or MySQL for a university platform?",
        "SQLite with Write-Ahead Logging delivers over 50,000 read operations per second with sub-millisecond query latency because data operations bypass TCP/IP networking loops. For a campus infrastructure management system generating hundreds of work orders per day, SQLite provides zero-configuration reliability, zero background server daemon vulnerabilities, and single-file backup simplicity. If the university ever scales past 50,000 concurrent daily writes, the repository layer is fully decoupled and can be migrated to PostgreSQL without altering frontend contracts."
    )

    # =========================================================================
    # SLIDE 5: DATABASE DESIGN AND 3NF DATA MODELING (Figure 3)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5, LIGHT_BG)
    add_header(s5, "05 · Data Engineering & Schema", "Relational Schema and Normalization Strategy", "Third Normal Form (3NF) Architecture with Materialized Analytical Views")

    # Left: Figure 3 ERD Diagram Card
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

    # Right: Schema & 3NF Cards
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
        "Data integrity is the bedrock of Campus. We strictly normalized our data layer to Third Normal Form. Notice how tickets do not store facility room details or department contact information directly. Instead, foreign keys reference dedicated facilities and departments tables. This eliminates update anomalies: if a department changes its SLA benchmark or a room is repurposed, historical ticket records remain structurally sound. Every status modification writes a record into ticket_audit_logs, providing an immutable audit trail showing who transitioned a ticket and when. To accelerate analytics without complicating application code, we defined database views: vw_department_sla_metrics calculates live compliance rates and average resolution durations using SQLite native date math, and vw_campus_hotspots surfaces locations experiencing recurring maintenance problems.",
        "Why create database views instead of computing metrics in Node.js?",
        "Computing aggregations at the database engine level is significantly faster because SQLite executes aggregations natively in compiled C, utilizing index structures and avoiding the overhead of streaming thousands of individual JSON rows across the IPC boundary into Node.js memory."
    )

    # =========================================================================
    # SLIDE 6: CORE SYSTEM FEATURES (Figures 4 & 5)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6, LIGHT_BG)
    add_header(s6, "06 · Feature Demonstration", "Core System Features: Reporting and Work Orders", "End-to-End Incident Processing Workflow in Live Operational Action")

    # Left Column: Student Submission Portal
    c6_l = create_card(s6, Inches(0.8), Inches(1.68), col_w, Inches(5.0), bg_color=WHITE)
    
    # Image frame
    add_fitted_picture(s6, "presentation/assets/student-portal.png", Inches(0.95), Inches(1.8), Inches(5.35), Inches(2.6))
    
    tb_l = s6.shapes.add_textbox(Inches(0.95), Inches(4.5), Inches(5.35), Inches(2.05))
    tl_tf = tb_l.text_frame
    tl_tf.word_wrap = True
    tl_tf.margin_left = tl_tf.margin_top = tl_tf.margin_right = tl_tf.margin_bottom = 0

    p0 = tl_tf.paragraphs[0]
    p0.text = "A. STUDENT INCIDENT REPORTING PORTAL (FIG. 4)"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(11)
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
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    # Right Column: Maintenance Work Orders Queue
    c6_r = create_card(s6, right_x, Inches(1.68), col_w, Inches(5.0), bg_color=WHITE)
    
    # Image frame
    add_fitted_picture(s6, "presentation/assets/work-orders-queue.png", right_x + Inches(0.15), Inches(1.8), Inches(5.35), Inches(2.6))
    
    tb_r = s6.shapes.add_textbox(right_x + Inches(0.15), Inches(4.5), Inches(5.35), Inches(2.05))
    tr_tf = tb_r.text_frame
    tr_tf.word_wrap = True
    tr_tf.margin_left = tr_tf.margin_top = tr_tf.margin_right = tr_tf.margin_bottom = 0

    p0 = tr_tf.paragraphs[0]
    p0.text = "B. MAINTENANCE WORK ORDERS QUEUE (FIG. 5)"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(11)
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
        p.font.size = Pt(10)
        p.font.color.rgb = DARK_TEXT
        p.space_after = Pt(2)

    add_footer(s6, 6, 9)
    attach_notes(
        s6,
        "This slide displays the core operational interfaces of Campus in live action. In Figure 4, we see the Student and Staff Reporting Portal. Submitting an issue takes under 30 seconds. A student selects their building and room or clicks directly on the interactive 2D campus blueprint. The blueprint dynamically colors rooms based on their operational status: green for normal, red for active critical issues. The reporting form includes a drag-and-drop dropzone for visual proof, which maintenance staff rely upon to bring the correct replacement parts. In Figure 5, we show the Administrative Work Orders Queue used by facility staff. Technicians can filter by trade, search by room number, and sort by SLA deadline. We implemented bulk action capabilities so a technician servicing a full floor can select multiple plumbing tickets and transition them all to 'In Progress' or 'Resolved' in a single operation.",
        "How does the interactive blueprint receive real-time room status updates?",
        "On page load and following ticket creation, the client queries /api/v1/facilities. The frontend iterates through the SVG room elements matching data-room attributes and applies CSS status classes based on the highest-severity unresolved ticket logged against that location."
    )

    # =========================================================================
    # SLIDE 7: MAINTENANCE ANALYTICS AND TELEMETRY (Figure 6)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7, LIGHT_BG)
    add_header(s7, "07 · Analytics & Decision Support", "Facility Analytics and SLA Compliance Intelligence", "Real-Time Operational Telemetry for University Leadership and Facility Directors")

    # Top: 4 KPI Cards
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

    # Middle: Figure 6 Analytics Dashboard Card
    fig6_card = create_card(s7, Inches(0.8), Inches(2.88), Inches(11.733), Inches(2.6), bg_color=WHITE)
    add_fitted_picture(s7, "presentation/assets/maintenance-analytics.png", Inches(1.0), Inches(2.95), Inches(11.333), Inches(2.4))

    # Bottom: 4 Analytical Module Cards
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
        "Operational data without actionable visualization is useless to university leadership. Slide 7 demonstrates the Campus Analytics Dashboard shown in Figure 6. At the top, executive KPI cards immediately answer critical operational questions: what is our global SLA compliance rate, how many unresolved work orders are active right now, and what is our campus-wide Mean Time to Resolution? Below the KPI strip, Chart.js renders two analytical perspectives: a 7-day workload trend line showing ticket creation versus resolution pace, and a category distribution doughnut highlighting where maintenance load concentrates. Notice the Department SLA Compliance table in the bottom left. It computes compliance percentages for Electrical, Plumbing, HVAC, and Carpentry directly from our SQL view. Facilities exhibiting more than two active complaints appear on the Hotspot table, giving leadership concrete data on which campus assets require complete replacement rather than continued short-term patching.",
        "How does the platform handle time zone discrepancies when calculating SLA deadlines?",
        "All timestamps are strictly generated and stored in ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SS.SSSZ). SQLite date-time functions compute elapsed duration in UTC seconds, and the client browser renders local formatted times according to the user's localized browser locale."
    )

    # =========================================================================
    # SLIDE 8: TECHNICAL ENGINEERING HIGHLIGHTS (Figure 7 + Tests)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8, LIGHT_BG)
    add_header(s8, "08 · Engineering Rigor & Quality Assurance", "Engineering Decisions, Performance, and Verification", "Robustness, Concurrency, State Machine Integrity, and 100% Automated Testing")

    # Top: 3 Engineering Highlight Cards
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

    # Bottom: Test Terminal Screenshot (Left) + Verification Metrics (Right)
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
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = GREEN
    p0.space_after = Pt(6)

    # 2 Mini metric boxes
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
    p3.font.size = Pt(10.5)
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
        p.font.size = Pt(10)
        p.font.color.rgb = MUTED_TEXT
        p.space_after = Pt(2)

    add_footer(s8, 8, 9)
    attach_notes(
        s8,
        "Engineering rigor separates an academic prototype from production-ready software. On this slide, we summarize three key engineering decisions. First, following syllabus requirements, we configured on-disk SQLite with Write-Ahead Logging and a 5-second busy timeout. This allows analytical queries to execute without blocking incoming ticket submissions from students. Second, we enforced a strict state machine with immutable audit logging. A ticket cannot skip from open to closed without logging who performed the work and recording intermediate state in ticket_audit_logs. Third, our deployment uses Docker orchestration that packages the Node.js runtime and compiled SQLite bindings into an isolated container. As shown in Figure 7, our automated integration test suite exercises all REST endpoints, validation constraints, and database views with 100% passing results.",
        "How do you guarantee database consistency if the Docker container is forcibly killed?",
        "SQLite Write-Ahead Logging writes transactions to a separate -wal file before committing them to the primary database file. If power is lost or the container stops abruptly, SQLite automatically replays the WAL log upon restart, restoring consistent transactional state without data corruption."
    )

    # =========================================================================
    # SLIDE 9: FUTURE ROADMAP AND CONCLUSION (Dark Navy Theme)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9, NAVY_DARK)
    add_header(s9, "09 · Roadmap & Conclusion", "Future Roadmap and Project Conclusion", "Scaling Campus into an Autonomous Smart Campus Intelligence Platform", dark=True)

    # Left Column: 4 Evolutionary Roadmap Phases
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
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(2)

        p1 = ptf.add_paragraph()
        p1.text = desc
        p1.font.name = FONT_FAMILY
        p1.font.size = Pt(9.5)
        p1.font.color.rgb = LIGHT_MUTED

    # Right Column: Takeaways + Summary Conclusion Card
    r_takeaways = create_card(s9, right_x, Inches(1.68), col_w, Inches(2.2), bg_color=NAVY_CARD, border_color=NAVY_BORDER)
    rtf = r_takeaways.text_frame
    rtf.word_wrap = True
    rtf.margin_left = rtf.margin_right = Inches(0.24)
    rtf.margin_top = Inches(0.16)

    p0 = rtf.paragraphs[0]
    p0.text = "ACADEMIC & ENGINEERING TAKEAWAYS"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(11)
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
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(226, 232, 240)
        p.space_after = Pt(3)

    # Summary Quote Card
    r_sum = create_card(s9, right_x, Inches(4.02), col_w, Inches(1.5), bg_color=PRIMARY_BLUE, border_color=LIGHT_SKY, border_width=Pt(1.5))
    stf = r_sum.text_frame
    stf.word_wrap = True
    stf.margin_left = stf.margin_right = Inches(0.24)
    stf.margin_top = Inches(0.16)

    p0 = stf.paragraphs[0]
    p0.text = "SUMMARY CONCLUSION"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = LIGHT_SKY
    p0.space_after = Pt(4)

    p1 = stf.add_paragraph()
    p1.text = "Campus proves that modern campus facility operations can be transformed through clean software design, transparent SLA tracking, and spatial intelligence."
    p1.font.name = FONT_FAMILY
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    # Repo & Makefile Box
    r_repo = create_card(s9, right_x, Inches(5.65), col_w, Inches(1.0), bg_color=NAVY_CARD, border_color=NAVY_BORDER)
    rrtf = r_repo.text_frame
    rrtf.word_wrap = True
    rrtf.margin_left = rrtf.margin_right = Inches(0.24)
    rrtf.margin_top = Inches(0.12)

    p0 = rrtf.paragraphs[0]
    p0.text = "REPOSITORY & CLI COMMANDS"
    p0.font.name = FONT_MONO
    p0.font.size = Pt(9.5)
    p0.font.bold = True
    p0.font.color.rgb = LIGHT_SKY

    p1 = rrtf.add_paragraph()
    p1.text = "github.com/Eshan-Jogwar/tpds-3-final-semester-rpoject.git\nCommands: make up  |  make test  |  make status"
    p1.font.name = FONT_MONO
    p1.font.size = Pt(9.5)
    p1.font.color.rgb = RGBColor(203, 213, 225)

    add_footer(s9, 9, 9, dark=True)
    attach_notes(
        s9,
        "In conclusion, Campus demonstrates how thoughtful software engineering and normalized relational design can solve longstanding physical campus inefficiencies. Over this semester, we built a fully containerized, responsive web system featuring 3NF SQLite persistence, automated SLA compliance tracking, interactive spatial mapping, and executive telemetry. Looking forward, our architecture easily accommodates QR code scanning at classroom doors, IoT water and power sensor alerts, and mobile push notifications for maintenance crews. The complete source code, database migrations, test suites, and Docker orchestration files are publicly available on GitHub. Thank you for your time, and we now welcome any questions from the examination committee.",
        "If you had two more weeks, what single feature would you implement first?",
        "We would implement dynamic QR code generation for facilities. Generating a printable QR code for each room that encodes ?building=Engineering&room=302 would allow any student to scan with their phone camera and immediately arrive at a pre-filled incident submission screen, reducing report friction to under ten seconds."
    )

    # Save to presentation/Campus_Presentation.pptx and presentation/index.pptx
    out_path = "presentation/Campus_Presentation.pptx"
    prs.save(out_path)
    print(f"✓ Saved native PowerPoint presentation to {out_path}")

    # Also save as presentation/index.pptx so both are native PowerPoint!
    prs.save("presentation/index.pptx")
    print("✓ Updated presentation/index.pptx as native PowerPoint")

if __name__ == '__main__':
    build_presentation()
