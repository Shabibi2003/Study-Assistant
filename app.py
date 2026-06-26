"""
AI-Based Student Study Assistant
Class XII Data Science Project
--------------------------------
A Streamlit app that:
  1. Takes student login (name)
  2. Accepts subject-wise marks
  3. Calculates percentage
  4. Predicts performance band
  5. Gives AI-based study suggestions (via Google Gemini Flash)
  6. Generates a daily study planner
  7. Shows a motivational quote
  8. Provides a simple menu-driven interface
"""

import os
import random
import datetime
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------------------------
# 1. CONFIGURATION
# ---------------------------------------------------------------
load_dotenv()  # loads GEMINI_API_KEY from .env file if present

# Try Streamlit secrets first (for deployment), then environment variable
API_KEY = None
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-flash-latest"   # Gemini Flash model

# ---------------------------------------------------------------
# 2. STATIC DATA (used as offline fallback)
# ---------------------------------------------------------------
QUOTES = [
    "Success is the sum of small efforts repeated day in and day out.",
    "Don't watch the clock; do what it does. Keep going.",
    "The expert in anything was once a beginner.",
    "Push yourself, because no one else is going to do it for you.",
    "Dream big. Work hard. Stay focused.",
    "Believe you can and you're halfway there.",
    "Hard work beats talent when talent doesn't work hard.",
    "The future depends on what you do today.",
    "Study while others are sleeping; work while others are loafing.",
    "Small progress is still progress."
]

# ---------------------------------------------------------------
# 3. CORE FUNCTIONS
# ---------------------------------------------------------------
def calculate_percentage(marks_dict):
    """Return overall percentage from {subject: marks} dict (out of 100 each)."""
    if not marks_dict:
        return 0.0
    total = sum(marks_dict.values())
    return round(total / len(marks_dict), 2)


def predict_performance(percentage):
    """Classify performance into one of four bands."""
    if percentage >= 85:
        return "Excellent"
    elif percentage >= 70:
        return "Good"
    elif percentage >= 50:
        return "Average"
    else:
        return "Needs Improvement"


def find_weak_subjects(marks_dict, threshold=50):
    """Return list of subjects below threshold."""
    return [sub for sub, m in marks_dict.items() if m < threshold]


def offline_suggestions(performance, weak_subjects):
    """Rule-based fallback suggestions if API is unavailable."""
    tips = []
    if performance == "Excellent":
        tips.append("Keep up the great work! Try advanced problems and mock tests.")
        tips.append("Help classmates — teaching strengthens your own understanding.")
    elif performance == "Good":
        tips.append("You are doing well. A bit more practice can push you to excellent.")
        tips.append("Solve previous years' question papers regularly.")
    elif performance == "Average":
        tips.append("More practice required — focus on NCERT first, then reference books.")
        tips.append("Improve time management with a daily study schedule.")
    else:
        tips.append("Don't worry. Start with basics and build up step by step.")
        tips.append("Set small daily goals and revise every weekend.")

    if weak_subjects:
        tips.append("Focus on weak subjects: " + ", ".join(weak_subjects) + ".")
    tips.append("Revision reminder: revise each topic within 24 hours of learning it.")
    return tips


def ai_suggestions(name, marks_dict, percentage, performance):
    """Call Gemini Flash for personalised suggestions. Falls back to offline tips on error."""
    weak = find_weak_subjects(marks_dict)
    if not API_KEY:
        return offline_suggestions(performance, weak), "Offline (no API key configured)"

    prompt = f"""
    You are a friendly study coach for an Indian Class 12 student named {name}.
    Their subject marks (out of 100) are: {marks_dict}.
    Overall percentage: {percentage}%. Performance band: {performance}.
    Weak subjects (below 50): {weak if weak else 'None'}.

    Give 5 short, practical study suggestions as a bullet list.
    Cover: time management, weak-subject focus, revision strategy,
    practice resources, and motivation. Keep each point under 25 words.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Split into bullet-like lines
        lines = [ln.lstrip("-*• ").strip() for ln in text.split("\n") if ln.strip()]
        return lines, "Gemini Flash"
    except Exception as e:
        return offline_suggestions(performance, weak) + [f"(AI error: {e})"], "Offline fallback"


def ai_study_planner(name, weak_subjects, all_subjects):
    """Generate a daily study planner using Gemini Flash."""
    if not API_KEY:
        # Offline fallback planner
        plan = []
        slots = ["6:00 - 7:30 AM", "5:00 - 6:30 PM", "8:00 - 9:30 PM"]
        focus = weak_subjects if weak_subjects else all_subjects
        for i, slot in enumerate(slots):
            sub = focus[i % len(focus)] if focus else "Revision"
            plan.append(f"{slot}  →  {sub}")
        plan.append("10:00 PM  →  Quick revision of today's topics")
        return plan, "Offline planner"

    prompt = f"""
    Create a simple 1-day study planner for a Class 12 student named {name}.
    Subjects: {all_subjects}. Weak subjects to prioritise: {weak_subjects if weak_subjects else 'None'}.
    Give 5 to 6 time slots from morning to night.
    Format each line strictly as:  TIME  -  SUBJECT/ACTIVITY
    Keep it concise. No extra commentary.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        lines = [ln.strip("-*• ").strip() for ln in response.text.split("\n") if ln.strip()]
        return lines, "Gemini Flash"
    except Exception as e:
        return [f"(AI error: {e})"], "Offline fallback"


def get_motivational_quote():
    """Use Gemini for a fresh quote, else pick a random offline one."""
    if API_KEY:
        try:
            model = genai.GenerativeModel(MODEL_NAME)
            r = model.generate_content(
                "Give me ONE short motivational quote (under 20 words) for a student preparing for board exams. Only the quote, no author."
            )
            return r.text.strip().strip('"')
        except Exception:
            pass
    return random.choice(QUOTES)


# ---------------------------------------------------------------
# 4. STREAMLIT UI
# ---------------------------------------------------------------
st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

# ----- Session state init -----
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "student_name" not in st.session_state:
    st.session_state.student_name = ""
if "marks" not in st.session_state:
    st.session_state.marks = {}

# ----- Login screen -----
if not st.session_state.logged_in:
    st.title("📚 AI-Based Student Study Assistant")
    st.caption("Class XII – Data Science Project")
    st.markdown("---")
    name = st.text_input("Enter your name to begin:")
    if st.button("Login", type="primary"):
        if name.strip():
            st.session_state.student_name = name.strip()
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.warning("Please enter a valid name.")
    st.stop()

# ----- Main app (after login) -----
st.sidebar.title(f"👋 Hello, {st.session_state.student_name}")
st.sidebar.markdown("### Menu")
menu = st.sidebar.radio(
    "Choose a feature:",
    [
        "🏠 Home",
        "✏️ Enter Marks",
        "📊 Performance Report",
        "🤖 AI Study Suggestions",
        "🗓️ Daily Study Planner",
        "💡 Motivational Quote",
        "🚪 Logout",
    ],
)

# Show API status in sidebar
st.sidebar.markdown("---")
if API_KEY:
    st.sidebar.success("✅ Gemini AI: Connected")
else:
    st.sidebar.warning("⚠️ Gemini AI: Offline mode\n\nAdd GEMINI_API_KEY to `.env`")

# ----- HOME -----
if menu == "🏠 Home":
    st.title("📚 AI-Based Student Study Assistant")
    st.subheader(f"Welcome, {st.session_state.student_name}!")
    st.write(
        "This is a smart study assistant built using **Python**, **Streamlit**, "
        "and **Google Gemini Flash AI**. Use the sidebar menu to:"
    )
    st.markdown(
        """
        - ✏️ Enter your subject-wise marks
        - 📊 See your percentage and performance band
        - 🤖 Get personalised AI study suggestions
        - 🗓️ Generate a daily study planner
        - 💡 Get a motivational quote
        """
    )
    st.info(f"📅 Today is **{datetime.date.today().strftime('%A, %d %B %Y')}**")

# ----- ENTER MARKS -----
elif menu == "✏️ Enter Marks":
    st.title("✏️ Subject-wise Marks Entry")
    st.write("Enter marks (out of 100) for each subject.")

    default_subjects = ["English", "Mathematics", "Physics", "Chemistry", "Computer Science"]
    num = st.number_input("Number of subjects:", min_value=1, max_value=10,
                          value=len(default_subjects), step=1)

    with st.form("marks_form"):
        new_marks = {}
        cols = st.columns(2)
        for i in range(int(num)):
            with cols[i % 2]:
                sub_default = default_subjects[i] if i < len(default_subjects) else f"Subject {i+1}"
                sub = st.text_input(f"Subject {i+1} name", value=sub_default, key=f"sub_{i}")
                mark = st.number_input(f"Marks for {sub_default}", min_value=0, max_value=100,
                                       value=75, key=f"mark_{i}")
                if sub.strip():
                    new_marks[sub.strip()] = mark
        submitted = st.form_submit_button("💾 Save Marks", type="primary")
        if submitted:
            st.session_state.marks = new_marks
            st.success(f"Saved marks for {len(new_marks)} subjects!")
            st.write(new_marks)

# ----- PERFORMANCE REPORT -----
elif menu == "📊 Performance Report":
    st.title("📊 Performance Report")
    if not st.session_state.marks:
        st.warning("Please enter marks first from the ✏️ Enter Marks menu.")
    else:
        marks = st.session_state.marks
        pct = calculate_percentage(marks)
        perf = predict_performance(pct)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Subjects", len(marks))
        c2.metric("Percentage", f"{pct}%")
        c3.metric("Performance", perf)

        st.subheader("Subject-wise breakdown")
        st.bar_chart(marks)

        weak = find_weak_subjects(marks)
        if weak:
            st.error("Weak subjects (below 50): " + ", ".join(weak))
        else:
            st.success("No weak subjects — great going!")

# ----- AI SUGGESTIONS -----
elif menu == "🤖 AI Study Suggestions":
    st.title("🤖 AI-Based Study Suggestions")
    if not st.session_state.marks:
        st.warning("Please enter marks first.")
    else:
        marks = st.session_state.marks
        pct = calculate_percentage(marks)
        perf = predict_performance(pct)
        with st.spinner("Thinking with Gemini Flash..."):
            tips, source = ai_suggestions(st.session_state.student_name, marks, pct, perf)
        st.caption(f"Source: {source}")
        for t in tips:
            st.markdown(f"- {t}")

# ----- STUDY PLANNER -----
elif menu == "🗓️ Daily Study Planner":
    st.title("🗓️ Daily Study Planner")
    if not st.session_state.marks:
        st.warning("Enter marks first so the planner can prioritise weak subjects.")
    else:
        marks = st.session_state.marks
        weak = find_weak_subjects(marks)
        with st.spinner("Building your planner..."):
            plan, source = ai_study_planner(
                st.session_state.student_name, weak, list(marks.keys())
            )
        st.caption(f"Source: {source}")
        for slot in plan:
            st.markdown(f"- {slot}")

# ----- MOTIVATIONAL QUOTE -----
elif menu == "💡 Motivational Quote":
    st.title("💡 Motivational Quote of the Moment")
    if st.button("✨ Generate New Quote", type="primary"):
        with st.spinner("Fetching inspiration..."):
            q = get_motivational_quote()
        st.success(f"> {q}")
    else:
        st.info(f"> {random.choice(QUOTES)}")

# ----- LOGOUT -----
elif menu == "🚪 Logout":
    st.title("Goodbye! 👋")
    st.write(f"Thanks for using the assistant, {st.session_state.student_name}.")
    if st.button("Confirm Logout"):
        st.session_state.logged_in = False
        st.session_state.student_name = ""
        st.session_state.marks = {}
        st.rerun()
