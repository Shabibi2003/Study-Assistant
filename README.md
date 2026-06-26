# AI-Based Student Study Assistant

**Class XII – Data Science (Python) Holiday Homework Project**

A Streamlit web app that helps students manage studies, track performance, get
AI-powered study suggestions, build a daily planner, and stay motivated — powered
by **Google Gemini Flash**.

---

## 🔧 Setup Instructions

### 1. Install Python (3.9 or newer)
Download from https://www.python.org/downloads/

### 2. Open a terminal in this project folder and install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API key
Get a free key from https://aistudio.google.com/apikey

Then **either**:

**Option A (recommended for local use)** — copy `.env.example` to `.env` and edit:
```
GEMINI_API_KEY=paste_your_real_key_here
```

**Option B (for Streamlit Cloud)** — copy `.streamlit/secrets.toml.example` to
`.streamlit/secrets.toml` and edit the same way.

> ⚠️ **Never share your API key publicly.** The `.gitignore` is already set up to
> keep `.env` and `secrets.toml` out of version control.

### 4. Run the app
```bash
streamlit run app.py
```
The browser will open at `http://localhost:8501`.

### 5. Run the extra practice programs
```bash
python practice_programs.py
```

---

## 📁 File Structure
```
ai_study_assistant/
├── app.py                  # Main Streamlit application
├── practice_programs.py    # 10 list + string practice programs
├── requirements.txt        # Python dependencies
├── .env.example            # Template for API key (rename to .env)
├── .gitignore
├── .streamlit/
│   └── secrets.toml.example
└── README.md
```

---

## ✅ Features (matches homework rubric)

| # | Feature | Where in code |
|---|---------|---------------|
| 1 | Student login / name input | Login screen in `app.py` |
| 2 | Subject-wise marks entry | `✏️ Enter Marks` menu |
| 3 | Percentage calculation | `calculate_percentage()` |
| 4 | Performance prediction (4 bands) | `predict_performance()` |
| 5 | AI study suggestions | `ai_suggestions()` (Gemini) |
| 6 | Daily study planner | `ai_study_planner()` |
| 7 | Motivational quote generator | `get_motivational_quote()` |
| 8 | Menu-driven interface | Sidebar radio menu |

If the API key is missing or fails, the app **automatically falls back to
offline rule-based suggestions**, so it always works.

---

# 📘 Project Report Content
*(Paste these sections into your practical file)*

## 5. Introduction

**Artificial Intelligence (AI)** is the branch of computer science that builds
machines capable of performing tasks that normally require human intelligence —
such as learning, reasoning, problem-solving, perception, and decision-making.
Modern AI systems use vast amounts of data and algorithms (especially machine
learning and deep learning) to recognise patterns and make predictions.

**Importance of AI in Education:** AI is transforming the way students learn.
Smart tutoring systems can adapt to each learner's pace, identify weak areas,
recommend personalised resources, and provide 24/7 doubt support. Tools like AI
chatbots, automatic grading, and adaptive testing reduce teachers' workload and
make learning more engaging.

**Purpose of the Project:** The "AI-Based Student Study Assistant" is designed
to help Class XII students manage their studies efficiently. It collects subject
marks, calculates performance, classifies it into bands (Excellent / Good /
Average / Needs Improvement), and uses Google's **Gemini Flash** Large Language
Model to give personalised study suggestions, a daily planner, and motivational
quotes.

**How smart systems help students:** By analysing a student's marks the system
identifies weak subjects and recommends focused practice. Daily planners help
with time management, while motivational quotes keep the learner positive. This
combination of analytics + generative AI mirrors how real EdTech platforms (BYJU'S,
Khan Academy, Duolingo) personalise learning at scale.

## 6. Problem Statement

Students today juggle multiple subjects, coaching classes, projects, and exam
pressure. Many face:
- Difficulty deciding **what to study and when**
- No clear feedback on **which subjects need more attention**
- Lack of **consistent motivation**
- Trial-and-error study plans that waste time

A smart, AI-driven assistant can solve these by acting as a personal study coach
that is always available, free, and adapts to each student's performance.

## 7. Objectives

1. To accept subject-wise marks and calculate overall percentage automatically.
2. To classify performance into four bands using rule-based logic.
3. To provide personalised AI-generated study suggestions using Gemini Flash.
4. To generate a day-wise study planner that prioritises weak subjects.
5. To motivate students with quotes and an interactive, user-friendly UI.

## 8. AI Concepts Used

- **Generative AI / LLM:** Gemini Flash generates suggestions and planners in
  natural language based on the student's marks (a *prompt-engineering* approach).
- **Decision-making system:** `if-elif-else` rules classify performance bands
  and detect weak subjects (classic *rule-based AI*).
- **Input → Processing → Output pipeline:** marks (input) → percentage + band
  computation (processing) → recommendations + planner (output).
- **Smart recommendations:** the AI is given context (name, marks, weak subjects)
  so its replies are *personalised*, not generic.

## 9. Algorithm

```
Step 1 : Start
Step 2 : Ask the student to log in by entering their name.
Step 3 : Display menu with options:
         a) Enter Marks
         b) View Performance Report
         c) Get AI Study Suggestions
         d) Get Daily Study Planner
         e) Get Motivational Quote
         f) Logout
Step 4 : If "Enter Marks":
            For each subject, read subject name and marks (0-100).
            Store in dictionary `marks`.
Step 5 : If "View Performance Report":
            percentage = sum(marks.values()) / number_of_subjects
            If percentage >= 85  -> performance = "Excellent"
            Elif percentage >= 70 -> performance = "Good"
            Elif percentage >= 50 -> performance = "Average"
            Else                  -> performance = "Needs Improvement"
            Display percentage, band, and bar chart.
Step 6 : If "AI Study Suggestions":
            Build prompt with name, marks, % and weak subjects.
            Send prompt to Gemini Flash API.
            Display returned suggestions.
Step 7 : If "Daily Study Planner":
            Send weak subjects + all subjects to Gemini Flash.
            Display time-slotted planner.
Step 8 : If "Motivational Quote":
            Call Gemini for a fresh quote, else pick random from list.
Step 9 : If "Logout": clear session and return to login.
Step 10: Stop
```

## 10. Flowchart
*(Draw in your file. Suggested boxes in order:)*

```
 START → LOGIN (name?) → MENU
   ├── Enter Marks → store in dict → MENU
   ├── Report → calc % → classify band → show chart → MENU
   ├── AI Suggestions → build prompt → Gemini API → show tips → MENU
   ├── Planner → Gemini API → show schedule → MENU
   ├── Quote → Gemini / random → show → MENU
   └── Logout → END
```

## 13. Advantages

1. **Personalised:** suggestions adapt to each student's actual marks.
2. **Always available:** runs locally any time, no coaching-class timings.
3. **Free / low-cost:** uses Gemini Flash which has a generous free tier.
4. **Offline-safe:** falls back to rule-based tips if the internet/API is down.
5. **Easy to use:** menu-driven Streamlit UI works in any web browser.
6. **Educational:** demonstrates AI, Python, dictionaries, functions and APIs.

## 14. Limitations

1. Requires an internet connection and valid API key for full AI features.
2. Performance prediction is based only on marks — it ignores attendance,
   sleep, mental health, and other real-world factors.
3. The AI can occasionally produce generic advice or hallucinate facts; it is
   not a substitute for a real teacher or counsellor.

## 15. Future Scope

- **Voice assistant integration** (speech-to-text input, text-to-speech output).
- **Automatic timetable generation** spanning weeks, syncing with exam dates.
- **AI chatbot doubt-solver** for any subject question.
- **Machine-learning performance prediction** using historical test data.
- **Mobile app version** with push-notification reminders.
- **Multi-language support** for regional languages.

## 16. Conclusion

Building this project taught me how to combine **classical Python programming**
(variables, loops, lists, dictionaries, functions, conditionals) with **modern
AI APIs** to make something genuinely useful. I learned how Streamlit turns a
plain script into an interactive web app, how to safely store API keys in
environment variables, and how prompt engineering shapes the quality of AI
output. Most importantly, I now understand that AI is a *tool* — its real value
comes from how thoughtfully we design the workflow around it.

---

## 📌 Submission Checklist
- [ ] Cover page, certificate, acknowledgement, index
- [ ] Sections 5–16 above pasted into practical file
- [ ] Printed Python code (`app.py` + `practice_programs.py`)
- [ ] Screenshots: login, marks entry, report, suggestions, planner, quote
- [ ] Flowchart drawn neatly
- [ ] Colored headings and diagrams
