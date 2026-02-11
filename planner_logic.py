import os
import google.generativeai as genai
from dotenv import load_dotenv

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
    - Resources must not be generic; suggest specific documentation (e.g., "MDN Web Docs for Flexbox") or specific tutorial types.
    - Include a **Weekly Milestone** row at the end of every 7 days (Day 7, 14, 21, 28) and a final wrap-up on Day 30.

    ### 4. Final Weekly Summary
    - Provide a high-level summary of what the user will be able to build or perform after each of the 4 weeks.
    """

    try:
        response = model.generate_content(prompt)
        if not response.text:
            return "Error: The AI generated an empty response. Please try again."
        return response.text
    except Exception as e:
        return f"System Error: {str(e)}. Please check your API connection."