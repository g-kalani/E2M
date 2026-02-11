# AI Personal Learning Planner
An AI-powered assistant built for the **E2M Solutions Technical Assessment**. This tool analyzes a learner's current skills, identifies gaps relative to a target career role, and generates a realistic, structured 30-day learning journey with curated resources.

## Local Setup

### 1. Prerequisites
* **Python 3.9+**
* **Git**
* A **Google Gemini API Key** 

### 2. Installation & Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd <repo-folder>

# Create a virtual environment
python -m venv venv

# Activate the environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```
### 3. Environment Configuration
Create a .env file in the root directory and add your API key:
`GOOGLE_API_KEY=your_gemini_api_key_here`

### 4. Run the Application
```bash
streamlit run app.py
```
The app should automatically open in your browser at http://localhost:8501.

---

### 1. Skill Gap Analysis Logic
The core of this application is a transparent reasoning engine that moves beyond simple keyword matching.

* **Core Identification:** The system identifies essential skills for the `{target_role}` based on current industry standards.
* **Logical Comparison:** It performs a set-difference analysis between the user's `{current_skills}` and the role's requirements.
* **Gap Categorization:** Instead of a generic list, skills are categorized into:
    * **Mastered Skills:** Validating what the user already knows.
    * **Partial Gaps:** Areas where the user has a base but lacks depth.
    * **Missing Foundations:** Critical "day-zero" skills the user currently lacks.
* **Transparency:** To ensure the analysis is explainable, the system explicitly documents any **assumptions** made about the user's background.

---

### 2. Prompt Design & Personalization Strategy
The prompts were engineered to prioritize "practical and achievable" outcomes over aspirational ones.

* **Pacing & Commitment:** By injecting the `{time_commitment}` variable, the AI adjusts the density of daily tasks to ensure they are realistic for daily execution.
* **Difficulty Scaling:** The `{difficulty}` level changes the depth of resources suggested—Beginner focuses on "Why," while Advanced focuses on "How" and optimization.
* **Tone:** The AI acts as a "High-Context Career Coach," providing specific reasoning behind why each step in the progression is necessary.

---

### 3. Learning Plan Structuring Approach
* **Logical Progression:** Topics are organized chronologically, moving from **Foundations → Intermediate → Advanced/Project-based** learning.
* **Tabular UI:** To maximize "UX Clarity," the 30-day plan is presented in a Markdown table, allowing users to easily scroll through daily tasks and objectives.
* **Weekly Milestones:** Every 7 days, the plan includes a "Weekly Milestone" to summarize achievements and keep the learner motivated.

---

### 4. Error Handling & Validation
Reliability was a primary focus during implementation:

* **Input Validation:** The app ensures inputs are meaningful and non-empty before calling the LLM to prevent hallucinated or generic roadmaps.
* **Graceful Failures:** All LLM calls are wrapped in `try-except` blocks. If the API fails, the user receives a helpful error message and a retry option rather than a crash.
* **Stability:** The application state is managed to ensure it remains stable across multiple runs.

---

## 🚀 5. Known Limitations & Future Enhancements
While this MVP fulfills all functional requirements, the following improvements are planned:

* **Live Resource Verification:** Currently, resources are suggested based on LLM training data. Future versions could integrate the Google Search API to provide real-time, verified links.
* **Interactive Checkpoints:** Adding the ability to "mark as complete" directly in the Streamlit UI to track progress.
* **Calendar Export:** Allowing users to download an `.ics` file to block out their learning time on a real calendar.
