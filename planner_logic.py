import os
import re
import google.generativeai as genai
from dotenv import load_dotenv
from ics import Calendar, Event
from datetime import datetime, timedelta

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_learning_plan(current_skills, target_role, time_commitment, difficulty):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
    Based on your current skills ({current_skills}), goal ({target_role}), difficulty level ({difficulty}), and {time_commitment} dedicated each day, here is your personalized 30-day learning plan.

    ---
    ### 1. Skill Gap Analysis
    Analyze the following based on the role of {target_role}:
    - **Core Skills Required**: List essential skills for this role.
    - **Skills Mastered**: Identify which of the user's current skills ({current_skills}) match the role.
    - **Partial Gaps**: Identify skills where the user has basic knowledge but needs intermediate/advanced training.
    - **Missing Foundations**: List critical foundational skills for a {difficulty} learner that are currently absent.
    - **Assumptions**: Explicitly state assumptions about the user's background to ensure transparency.

    ### 2. Strategic Reasoning
    - Explain the logical progression from {difficulty} foundations to advanced topics.
    - Describe how the workload is balanced to fit within {time_commitment}/day to avoid burnout.

    ### 3. The 30-Day Learning Roadmap
    Create a detailed Markdown Table with the following columns: 
    | Day | Objective | Actionable Tasks | Recommended Resources (Specific Articles/Docs/Videos) |
    
    Requirements for the table:
    - Cover all 30 days.
    - Tasks must be actionable and achievable within {time_commitment}.
    - Resources must not be generic; suggest specific documentation or specific tutorial types.
    - Include a Weekly Milestone row at the end of every 7 days (Day 7, 14, 21, 28) and a final wrap-up on Day 30.
  
    ### 4. Final Weekly Summary
    - Provide a high-level summary of what the user will be able to build or perform after each of the 4 weeks.

    ---
    ### CALENDAR_DATA_BLOCK
    Provide a list of 30 lines strictly in this format for machine parsing:
    DAY_DATA: Day X | Topic | Key Task
    ### END_CALENDAR_DATA
    """

    try:
        response = model.generate_content(prompt)
        if not response.text:
            return "Error: The AI generated an empty response. Please try again."
        return response.text
    except Exception as e:
        return f"System Error: {str(e)}. Please check your API connection."

def create_ics_calendar(roadmap_text, target_role):
    c = Calendar()
    start_date = datetime.now()
    
    day_entries = re.findall(r"DAY_DATA: Day (\d+) \| (.*?) \| (.*)", roadmap_text)
    
    if not day_entries:
        for i in range(1, 31):
            e = Event()
            e.name = f"Day {i}: {target_role} Study"
            e.begin = (start_date + timedelta(days=i)).replace(hour=9, minute=0)
            e.make_all_day()
            c.events.add(e)
    else:
        for day_num, topic, task in day_entries:
            e = Event()
            e.name = f"Day {day_num.strip()}: {topic.strip()}"
            e.begin = (start_date + timedelta(days=int(day_num))).replace(hour=9, minute=0)
            e.description = f"Focus: {topic.strip()}\nTask: {task.strip()}"
            e.make_all_day() 
            c.events.add(e)
    
    return c.serialize()
