"""
AI-Based Student Study Assistant  (Rule-Based Version) — Enhanced UI
Class XII Data Science Project
"""

import random
import datetime
import streamlit as st
import plotly.graph_objects as go

# ---------------------------------------------------------------
# 1. RULE SETS
# ---------------------------------------------------------------
SUGGESTIONS_RULES = {
    "Excellent": [
        "Outstanding work! Attempt advanced and HOTS (Higher Order Thinking) questions.",
        "Solve previous 10 years' board papers under timed conditions.",
        "Start helping classmates — teaching is the best way to revise.",
        "Maintain a short formula/notes sheet for last-week revision.",
        "Don't get over-confident — stick to a consistent daily routine.",
    ],
    "Good": [
        "You're doing well. A little more practice can push you into the top band.",
        "Solve sample papers every weekend and track your accuracy.",
        "Identify silly mistakes in tests and maintain an 'error log'.",
        "Allocate extra 30 minutes daily to your two lowest-scoring subjects.",
        "Revise NCERT thoroughly before moving to reference books.",
    ],
    "Average": [
        "More practice required — start with NCERT line-by-line.",
        "Improve time management with a fixed daily study schedule.",
        "Break long chapters into small 30-minute focused sessions.",
        "Clear basic doubts immediately — don't let them pile up.",
        "Revise every topic within 24 hours of learning it.",
    ],
    "Needs Improvement": [
        "Don't panic. Start from the basics and build up step by step.",
        "Focus on scoring chapters first — they give quick confidence.",
        "Study in short 25-minute blocks (Pomodoro) with 5-minute breaks.",
        "Set 3 small, realistic daily goals and tick them off.",
        "Ask teachers/seniors for help on weak topics — it's a strength, not weakness.",
    ],
}

PLANNER_RULES = {
    "Excellent": [
        ("06:00 - 07:30 AM", "Advanced problems / HOTS questions"),
        ("10:00 - 11:30 AM", "Subject rotation – strongest subject"),
        ("04:00 - 05:30 PM", "Mock test / previous year paper"),
        ("07:00 - 08:30 PM", "Weak subject focus"),
        ("09:30 - 10:00 PM", "Quick revision of the day's topics"),
    ],
    "Good": [
        ("06:30 - 08:00 AM", "Weak subject – concept building"),
        ("11:00 AM - 12:30 PM", "Practice questions"),
        ("04:30 - 06:00 PM", "Subject rotation"),
        ("07:30 - 09:00 PM", "Sample paper / chapter test"),
        ("09:30 - 10:00 PM", "Error log review"),
    ],
    "Average": [
        ("07:00 - 08:30 AM", "Weak subject – NCERT reading"),
        ("11:00 AM - 12:00 PM", "Solved examples practice"),
        ("04:30 - 06:00 PM", "Another weak subject"),
        ("07:30 - 08:30 PM", "Easy/scoring subject"),
        ("09:00 - 09:30 PM", "Today's revision"),
    ],
    "Needs Improvement": [
        ("07:30 - 08:30 AM", "Easiest weak subject – basics"),
        ("11:00 - 11:45 AM", "Short practice (Pomodoro)"),
        ("05:00 - 06:00 PM", "Another weak subject – basics"),
        ("07:30 - 08:15 PM", "Scoring subject for confidence"),
        ("09:00 - 09:30 PM", "Light revision before sleep"),
    ],
}

QUOTES_RULES = {
    "Excellent": [
        "Excellence is not a skill, it's an attitude. Keep it up!",
        "The only way to do great work is to love what you do.",
        "Don't stop when you're tired. Stop when you're done.",
    ],
    "Good": [
        "You're closer to the top than you think — keep pushing!",
        "Small daily improvements lead to stunning results.",
        "Push yourself, because no one else is going to do it for you.",
    ],
    "Average": [
        "Every expert was once a beginner. Keep going!",
        "Progress, not perfection, is the goal.",
        "Hard work beats talent when talent doesn't work hard.",
    ],
    "Needs Improvement": [
        "It's okay to start slow — what matters is that you start.",
        "Fall seven times, stand up eight.",
        "A year from now you'll wish you had started today.",
    ],
    "General": [
        "Success is the sum of small efforts repeated day in and day out.",
        "Believe you can and you're halfway there.",
        "The future depends on what you do today.",
        "Dream big. Work hard. Stay focused.",
    ],
}

SUBJECT_TIPS = {
    "mathematics": "Solve 10 problems daily from RD Sharma / NCERT exemplar.",
    "maths":       "Solve 10 problems daily from RD Sharma / NCERT exemplar.",
    "physics":     "Memorise formulas with derivations; practice numericals daily.",
    "chemistry":   "Make flashcards for reactions and named processes.",
    "biology":     "Draw and label diagrams; revise NCERT lines verbatim.",
    "english":     "Read one editorial daily; practice writing skills (letter/notice/report).",
    "computer science": "Dry-run code on paper; revise SQL queries and Python syntax.",
    "informatics practices": "Practice pandas and SQL queries from previous papers.",
    "accountancy": "Solve at least one full ledger/balance-sheet problem daily.",
    "business studies": "Make one-page chapter summaries with bullet points.",
    "economics":   "Draw graphs neatly; revise definitions and formulas.",
    "history":     "Create timelines and mind-maps for each chapter.",
    "geography":   "Practice map work daily for 15 minutes.",
    "political science": "Make comparison tables of theories and constitutions.",
    "hindi":       "Read one passage daily and practice essay writing.",
}

BAND_COLORS = {
    "Excellent":         {"bg": "#10b981", "soft": "#d1fae5", "text": "#065f46", "emoji": "🏆"},
    "Good":              {"bg": "#3b82f6", "soft": "#dbeafe", "text": "#1e40af", "emoji": "🚀"},
    "Average":           {"bg": "#f59e0b", "soft": "#fef3c7", "text": "#92400e", "emoji": "📘"},
    "Needs Improvement": {"bg": "#ef4444", "soft": "#fee2e2", "text": "#991b1b", "emoji": "💪"},
}

# ---------------------------------------------------------------
# 2. CORE FUNCTIONS
# ---------------------------------------------------------------
def calculate_percentage(marks_dict):
    if not marks_dict:
        return 0.0
    return round(sum(marks_dict.values()) / len(marks_dict), 2)

def predict_performance(percentage):
    if percentage >= 85:   return "Excellent"
    elif percentage >= 70: return "Good"
    elif percentage >= 50: return "Average"
    else:                  return "Needs Improvement"

def find_weak_subjects(marks_dict, threshold=50):
    return [sub for sub, m in marks_dict.items() if m < threshold]

def get_suggestions(performance, weak_subjects):
    tips = list(SUGGESTIONS_RULES[performance])
    for sub in weak_subjects:
        key = sub.strip().lower()
        if key in SUBJECT_TIPS:
            tips.append(f"**{sub}:** {SUBJECT_TIPS[key]}")
        else:
            tips.append(f"**{sub}:** Spend an extra 30 minutes daily and revise NCERT first.")
    tips.append("📌 Revision reminder: revise every topic within 24 hours of learning it.")
    return tips

def build_planner(performance, weak_subjects, all_subjects):
    template = PLANNER_RULES[performance]
    focus = weak_subjects if weak_subjects else all_subjects
    if not focus:
        focus = ["Revision"]
    planner, weak_index, rotate_index = [], 0, 0
    for time_slot, activity in template:
        tag = None
        if "weak subject" in activity.lower() and focus:
            tag = focus[weak_index % len(focus)]; weak_index += 1
        elif "subject rotation" in activity.lower() and all_subjects:
            tag = all_subjects[rotate_index % len(all_subjects)]; rotate_index += 1
        planner.append((time_slot, activity, tag))
    return planner

def get_quote(performance=None):
    pool = QUOTES_RULES["General"][:]
    if performance and performance in QUOTES_RULES:
        pool += QUOTES_RULES[performance]
    return random.choice(pool)

def mark_color(m):
    if m >= 85:  return BAND_COLORS["Excellent"]
    if m >= 70:  return BAND_COLORS["Good"]
    if m >= 50:  return BAND_COLORS["Average"]
    return BAND_COLORS["Needs Improvement"]

# ---------------------------------------------------------------
# 3. PAGE CONFIG
# ---------------------------------------------------------------
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

# ---------------------------------------------------------------
# 4. GLOBAL CSS  — single source, no external file
# ---------------------------------------------------------------
st.markdown("""
<style>
/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #f5f7fb 0%, #eef2ff 100%) !important;
}

/* ── Hide ALL Streamlit branding & chrome ── */
#MainMenu { visibility: hidden !important; }
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
div[class*="viewerBadge"] { display: none !important; }
section[data-testid="stSidebar"] > div:last-child { display: none !important; }

/* ── Force all text dark (defeats dark-mode OS override) ── */
.stApp, .stApp p, .stApp span, .stApp div,
.stMarkdown, .stMarkdown p, .stMarkdown li, .stMarkdown span,
h1, h2, h3, h4, h5, h6 {
    color: #1e293b !important;
}

/* ── Widget labels ── */
label, [data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: #1e293b !important;
    font-weight: 600 !important;
}

/* ── Captions ── */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p { color: #64748b !important; }

/* ── Inputs — white bg, dark text ── */
.stTextInput input,
.stNumberInput input,
[data-baseweb="input"] input,
[data-baseweb="base-input"] input {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
}
.stNumberInput [data-baseweb="input"] { background-color: #ffffff !important; }
.stNumberInput button {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: none !important;
}
.stNumberInput button span, .stNumberInput button svg { color: #0f172a !important; }

/* ── Slider ── */
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] { color: #64748b !important; }
[data-baseweb="slider"] [data-testid="stThumbValue"] { color: #1e293b !important; }

/* ── Alerts ── */
[data-testid="stAlert"] p,
[data-testid="stAlert"] div,
[data-testid="stAlert"] span,
[role="alert"] p { color: #1e293b !important; }
[data-testid="stInfo"] p,
[data-testid="stInfo"] div { color: #1e40af !important; }

/* ── Expander ── */
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span { color: #1e293b !important; font-weight: 600 !important; }
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] td,
[data-testid="stExpander"] [data-testid="stMarkdownContainer"] th { color: #1e293b !important; }

/* ── Markdown tables ── */
[data-testid="stMarkdownContainer"] table,
[data-testid="stMarkdownContainer"] th,
[data-testid="stMarkdownContainer"] td {
    color: #1e293b !important;
    border-color: #e2e8f0 !important;
    background: #fff !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] { gap: 4px; }
.stTabs [data-baseweb="tab"] {
    background: white !important;
    border-radius: 10px 10px 0 0 !important;
    padding: 10px 18px !important;
    font-weight: 600 !important;
}
.stTabs [data-baseweb="tab"] p,
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] div { color: #334155 !important; font-weight: 600 !important; }
.stTabs [aria-selected="true"] { background: #6366f1 !important; }
.stTabs [aria-selected="true"] p,
.stTabs [aria-selected="true"] span,
.stTabs [aria-selected="true"] div { color: #ffffff !important; }

/* ── Hero (white text over gradient — exempted from global rule) ── */
.hero {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #ec4899 100%);
    padding: 28px 32px;
    border-radius: 18px;
    box-shadow: 0 10px 30px rgba(99,102,241,0.25);
    margin-bottom: 18px;
}
.hero h1, .hero p { color: #ffffff !important; }
.hero h1 { margin: 0; font-size: 28px; font-weight: 700; }
.hero p  { margin: 6px 0 0 0; font-size: 14px; opacity: 0.92; }

/* ── Generic card ── */
.card {
    background: white;
    padding: 18px 20px;
    border-radius: 14px;
    box-shadow: 0 4px 14px rgba(15,23,42,0.06);
    border: 1px solid #eef2f7;
    margin-bottom: 12px;
}

/* ── Login card ── */
.login-card {
    background: white;
    padding: 36px;
    border-radius: 20px;
    box-shadow: 0 20px 50px rgba(99,102,241,0.18);
    text-align: center;
    border: 1px solid #eef2f7;
}
.login-card h1, .login-card p { color: #1e293b !important; }

/* ── Band pill ── */
.band-pill {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 13px;
}

/* ── Subject row ── */
.subject-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 10px 14px; border-radius: 10px; margin-bottom: 6px;
    background: #f8fafc; border-left: 4px solid #cbd5e1;
}
.subject-name { font-weight: 600; color: #0f172a !important; }
.subject-mark { font-weight: 700; font-size: 15px; }

/* ── Timeline planner ── */
.tl-item {
    display: flex; gap: 14px; padding: 12px 14px;
    background: white; border-radius: 12px; margin-bottom: 8px;
    border-left: 4px solid #6366f1;
    box-shadow: 0 2px 6px rgba(15,23,42,0.04);
}
.tl-time { min-width: 145px; font-weight: 700; color: #4f46e5 !important; font-size: 13px; }
.tl-body { color: #334155 !important; font-size: 14px; }
.tl-tag {
    display: inline-block; margin-left: 8px; padding: 2px 10px;
    border-radius: 999px; background: #eef2ff; color: #4338ca !important;
    font-size: 12px; font-weight: 600;
}

/* ── Quote card ── */
.quote-card {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    padding: 28px; border-radius: 16px; border-left: 6px solid #f59e0b;
    font-style: italic; font-size: 18px; line-height: 1.6;
}
.quote-card, .quote-card * { color: #78350f !important; }

/* ── Tip items ── */
.tip-item {
    background: white; padding: 12px 16px; border-radius: 10px;
    margin-bottom: 8px; border-left: 4px solid #10b981;
    box-shadow: 0 2px 6px rgba(15,23,42,0.04); color: #1f2937 !important;
}
.tip-item * { color: #1f2937 !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# 5. SESSION STATE
# ---------------------------------------------------------------
for key, val in [("logged_in", False), ("student_name", ""), ("marks", {}), ("current_quote", None)]:
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------------------------------------------------------
# 6. LOGIN SCREEN
# ---------------------------------------------------------------
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <div style="font-size:54px;">📚</div>
            <h1 style="margin:8px 0 4px 0; color:#1e293b !important;">AI Study Assistant</h1>
            <p style="color:#64748b !important; margin-bottom:24px;">
                Class XII &nbsp;·&nbsp; Data Science Project &nbsp;·&nbsp; Rule-Based Expert System
            </p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        name = st.text_input("👤 Enter your name to begin", placeholder="e.g. Adeel Umar")
        if st.button("🚀 Start Learning", type="primary", use_container_width=True):
            if name.strip():
                st.session_state.student_name = name.strip()
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.warning("Please enter a valid name.")
    st.stop()

# ---------------------------------------------------------------
# 7. HERO HEADER
# ---------------------------------------------------------------
today = datetime.date.today().strftime('%A, %d %B %Y')
hero_col1, hero_col2 = st.columns([5, 1])
with hero_col1:
    st.markdown(f"""
    <div class="hero">
        <h1>👋 Hello, {st.session_state.student_name}!</h1>
        <p>📅 {today} &nbsp;·&nbsp; Your personalised AI-powered study companion</p>
    </div>
    """, unsafe_allow_html=True)
with hero_col2:
    st.write(""); st.write("")
    if st.button("🚪 Logout", use_container_width=True):
        for k in ["logged_in", "student_name", "marks", "current_quote"]:
            st.session_state[k] = False if k == "logged_in" else ("" if k == "student_name" else ({} if k == "marks" else None))
        st.rerun()

# ---------------------------------------------------------------
# 8. TABS
# ---------------------------------------------------------------
tab_home, tab_marks, tab_report, tab_suggest, tab_plan, tab_quote = st.tabs(
    ["🏠 Home", "✏️ Enter Marks", "📊 Report", "🤖 Suggestions", "🗓️ Planner", "💡 Quote"]
)

# ── HOME ──
with tab_home:
    for row_cards in [
        [("✏️","Enter Marks","Add subject-wise marks (out of 100)"),
         ("📊","Performance Report","Percentage, band & visual charts"),
         ("🤖","Smart Suggestions","Rule-based tips for your level")],
        [("🗓️","Daily Planner","Prioritises your weakest subjects"),
         ("💡","Motivation","Quotes tuned to your performance"),
         ("🧠","Expert System","If-elif rules — classic AI")],
    ]:
        cols = st.columns(3)
        for col, (icon, title, desc) in zip(cols, row_cards):
            col.markdown(f"""
            <div class="card" style="text-align:center; min-height:140px;">
                <div style="font-size:36px;">{icon}</div>
                <div style="font-weight:700;font-size:17px;margin-top:6px;color:#1e293b !important;">{title}</div>
                <div style="color:#64748b !important;font-size:13px;margin-top:4px;">{desc}</div>
            </div>""", unsafe_allow_html=True)
        st.write("")
    st.info("💡 **How it works:** A rule-based expert system — if-elif logic plus curated "
            "knowledge dictionaries — decides performance bands, study tips, and your daily schedule.")

# ── ENTER MARKS ──
with tab_marks:
    st.markdown("### ✏️ Subject-wise Marks Entry")
    st.caption("Enter marks out of 100 for each subject, then hit Save.")
    default_subjects = ["English", "Mathematics", "Physics", "Chemistry", "Computer Science"]
    num = st.number_input("Number of subjects", min_value=1, max_value=10,
                          value=len(default_subjects), step=1)
    with st.form("marks_form"):
        new_marks = {}
        cols = st.columns(2)
        for i in range(int(num)):
            with cols[i % 2]:
                sub_default = default_subjects[i] if i < len(default_subjects) else f"Subject {i+1}"
                sub  = st.text_input(f"📖 Subject {i+1} name", value=sub_default, key=f"sub_{i}")
                mark = st.slider(f"Marks — {sub_default}", 0, 100, 75, key=f"mark_{i}")
                if sub.strip():
                    new_marks[sub.strip()] = mark
        if st.form_submit_button("💾 Save Marks", type="primary", use_container_width=True):
            st.session_state.marks = new_marks
            st.success(f"✅ Saved marks for {len(new_marks)} subjects! Check the other tabs.")

# ── PERFORMANCE REPORT ──
with tab_report:
    st.markdown("### 📊 Performance Report")
    if not st.session_state.marks:
        st.warning("⚠️ Please enter marks first in the **✏️ Enter Marks** tab.")
    else:
        marks = st.session_state.marks
        pct   = calculate_percentage(marks)
        perf  = predict_performance(pct)
        band  = BAND_COLORS[perf]
        weak  = find_weak_subjects(marks)

        m1, m2, m3, m4 = st.columns(4)
        for col, (label, val, emoji) in zip([m1,m2,m3,m4], [
            ("Subjects",    len(marks),                             "📚"),
            ("Total Marks", f"{sum(marks.values())} / {len(marks)*100}", "✍️"),
            ("Percentage",  f"{pct}%",                             "📈"),
            ("Band",        f"{band['emoji']} {perf}",             "🎯"),
        ]):
            col.markdown(f"""
            <div class="card" style="text-align:center;">
                <div style="font-size:22px;">{emoji}</div>
                <div style="color:#64748b !important;font-size:12px;text-transform:uppercase;margin-top:4px;">{label}</div>
                <div style="font-weight:700;font-size:20px;color:#0f172a !important;margin-top:4px;">{val}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("")
        left, right = st.columns([1, 1.4])

        with left:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=pct,
                number={'suffix': "%", 'font': {'size': 38, 'color': band['bg']}},
                gauge={
                    'axis': {'range': [0,100], 'tickwidth': 1, 'tickcolor': "#cbd5e1"},
                    'bar':  {'color': band['bg'], 'thickness': 0.3},
                    'bgcolor': "white", 'borderwidth': 0,
                    'steps': [
                        {'range': [0,  50],  'color': '#fee2e2'},
                        {'range': [50, 70],  'color': '#fef3c7'},
                        {'range': [70, 85],  'color': '#dbeafe'},
                        {'range': [85, 100], 'color': '#d1fae5'},
                    ],
                }
            ))
            gauge.update_layout(height=280, margin=dict(l=20,r=20,t=20,b=20),
                                 paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(gauge, use_container_width=True)
            st.markdown(
                f"<div style='text-align:center;'>"
                f"<span class='band-pill' style='background:{band['soft']};color:{band['text']};'>"
                f"{band['emoji']} {perf}</span></div>", unsafe_allow_html=True)

        with right:
            sorted_marks = sorted(marks.items(), key=lambda x: x[1])
            vals   = [v for _, v in sorted_marks]
            subs   = [s for s, _ in sorted_marks]
            colors = [mark_color(v)["bg"] for v in vals]
            bar = go.Figure(go.Bar(
                x=vals, y=subs, orientation='h',
                marker=dict(color=colors),
                text=[str(v) for v in vals], textposition='outside',
            ))
            bar.update_layout(
                height=280, margin=dict(l=10,r=30,t=30,b=20),
                xaxis=dict(range=[0,115], showgrid=True, gridcolor='#eef2f7',
                           color='#334155', tickfont=dict(color='#334155')),
                yaxis=dict(showgrid=False, color='#334155',
                           tickfont=dict(color='#334155')),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                title=dict(text="Subject-wise Marks", font=dict(size=14, color="#334155")),
                font=dict(color='#334155'),
            )
            st.plotly_chart(bar, use_container_width=True)

        st.markdown("#### 🎯 Subject Breakdown")
        for sub, m in sorted(marks.items(), key=lambda x: -x[1]):
            c = mark_color(m)
            st.markdown(f"""
            <div class="subject-row" style="border-left-color:{c['bg']};">
                <span class="subject-name">{c['emoji']} {sub}</span>
                <span class="subject-mark" style="color:{c['bg']} !important;">{m} / 100</span>
            </div>""", unsafe_allow_html=True)

        if weak:
            st.error("🔴 **Weak subjects (below 50):** " + ", ".join(weak))
        else:
            st.success("🟢 No weak subjects — great going!")

        with st.expander("ℹ️ How is the performance band decided?"):
            st.markdown("""
| Percentage | Band |
|---|---|
| ≥ 85% | 🏆 Excellent |
| 70% – 84.99% | 🚀 Good |
| 50% – 69.99% | 📘 Average |
| < 50% | 💪 Needs Improvement |
""")

# ── SUGGESTIONS ──
with tab_suggest:
    st.markdown("### 🤖 Smart Study Suggestions")
    if not st.session_state.marks:
        st.warning("⚠️ Please enter marks first in the **✏️ Enter Marks** tab.")
    else:
        marks = st.session_state.marks
        pct   = calculate_percentage(marks)
        perf  = predict_performance(pct)
        weak  = find_weak_subjects(marks)
        band  = BAND_COLORS[perf]
        st.markdown(f"""
        <div class="card" style="background:{band['soft']};border-left:4px solid {band['bg']};">
            <div style="font-size:13px;color:{band['text']} !important;text-transform:uppercase;letter-spacing:0.5px;">Detected Band</div>
            <div style="font-size:22px;font-weight:700;color:{band['text']} !important;margin-top:4px;">
                {band['emoji']} {perf} &nbsp;·&nbsp; {pct}%
            </div>
        </div>""", unsafe_allow_html=True)
        for tip in get_suggestions(perf, weak):
            st.markdown(f"<div class='tip-item'>✅ {tip}</div>", unsafe_allow_html=True)

# ── PLANNER ──
with tab_plan:
    st.markdown("### 🗓️ Daily Study Planner")
    if not st.session_state.marks:
        st.warning("⚠️ Please enter marks first so the planner can prioritise weak subjects.")
    else:
        marks = st.session_state.marks
        pct   = calculate_percentage(marks)
        perf  = predict_performance(pct)
        weak  = find_weak_subjects(marks)
        band  = BAND_COLORS[perf]
        st.markdown(f"""
        <div class="card" style="background:{band['soft']};border-left:4px solid {band['bg']};">
            <b style="color:{band['text']} !important;">{band['emoji']} {perf} band</b>
            &nbsp;·&nbsp; Weak subjects: <b style="color:{band['text']} !important;">{', '.join(weak) if weak else 'None 🎉'}</b>
        </div>""", unsafe_allow_html=True)
        for time_slot, activity, tag in build_planner(perf, weak, list(marks.keys())):
            tag_html = f"<span class='tl-tag'>{tag}</span>" if tag else ""
            st.markdown(f"""
            <div class="tl-item">
                <div class="tl-time">🕒 {time_slot}</div>
                <div class="tl-body">{activity}{tag_html}</div>
            </div>""", unsafe_allow_html=True)
        st.caption("⏰ Tip: Take a 5-minute break between sessions and stay hydrated!")

# ── QUOTE ──
with tab_quote:
    st.markdown("### 💡 Motivational Quote")
    perf = None
    if st.session_state.marks:
        perf = predict_performance(calculate_percentage(st.session_state.marks))
        st.caption(f"Showing quotes tuned for the **{perf}** band.")
    if not st.session_state.current_quote:
        st.session_state.current_quote = get_quote(perf)
    if st.button("✨ Generate New Quote", type="primary"):
        st.session_state.current_quote = get_quote(perf)
    st.markdown(f"""
    <div class="quote-card">
        <div style="font-size:36px;line-height:1;margin-bottom:8px;">❝</div>
        {st.session_state.current_quote}
        <div style="text-align:right;font-size:32px;line-height:1;margin-top:8px;">❞</div>
    </div>""", unsafe_allow_html=True)