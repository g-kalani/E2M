import streamlit as st
from planner_logic import generate_learning_plan, create_ics_calendar

st.set_page_config(
    page_title="AI Personal Learning Planner",
    layout="wide"
)

st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color: white !important;
        border-radius: 8px;
        height: 3.5em;
        width: 100%;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background-color: #ff3333;
        color: white !important;
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
        transform: translateY(-2px);
    }
    .stTextArea textarea, .stTextInput input { border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("AI Personal Learning Planner")
st.markdown("Personalized, reasoning-driven roadmaps for your career goals.")

# Function to clear session and reset inputs
def reset_app():
    for key in ['generated_plan', 's_skills', 's_role']:
        if key in st.session_state:
            st.session_state.pop(key)
    st.rerun()

# Sidebar/Expander for Samples
with st.expander("Quick Start Samples"):
    s1, s2, s3 = st.columns(3)
    if s1.button("Frontend Developer"):
        st.session_state.s_skills, st.session_state.s_role = "HTML, CSS, Basic JS", "React Developer"
        st.rerun()
    if s2.button("Data Analyst"):
        st.session_state.s_skills, st.session_state.s_role = "Excel, Math", "Junior Data Analyst"
        st.rerun()
    if s3.button("Backend Engineer"):
        st.session_state.s_skills, st.session_state.s_role = "Python, SQL", "Node.js Developer"
        st.rerun()

st.divider()

col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.subheader("User Profile")
    curr_skills = st.text_area("Current Skills", value=st.session_state.get('s_skills', ''), height=150)
    t_role = st.text_input("Target Role", value=st.session_state.get('s_role', ''))

with col_right:
    st.subheader("Learning Preferences")
    time_val = st.radio("Daily Time Commitment", ["30 Minutes", "1 Hour", "2 Hours"], index=0, horizontal=True)
    diff_val = st.select_slider("Difficulty Level", options=["Beginner", "Intermediate", "Advanced"], value="Beginner")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    generate_btn = st.button("Generate Roadmap")

if generate_btn:
    if not curr_skills or not t_role:
        st.error("Please fill in all fields.")
    else:
        with st.status("Analyzing gaps and crafting your plan...", expanded=True) as status:
            st.session_state.generated_plan = generate_learning_plan(curr_skills, t_role, time_val, diff_val)
            st.session_state.current_target_role = t_role 
            status.update(label="Roadmap Generated", state="complete", expanded=False)


if "generated_plan" in st.session_state:
    display_content = st.session_state.generated_plan.split("### CALENDAR_DATA_BLOCK")[0]
    
    st.subheader("30-Day Structured Roadmap")
    st.markdown(display_content)
    
    st.divider()
    st.subheader("Export Options")
    ex1, ex2, ex3 = st.columns(3)
    
    ex1.download_button(
        "Download Markdown (.md)", 
        data=display_content, 
        file_name="Roadmap.md"
    )
    
    ex2.download_button(
        "Download Text (.txt)", 
        data=display_content, 
        file_name="Roadmap.txt"
    )

    calendar_data = create_ics_calendar(
        st.session_state.generated_plan, 
        st.session_state.current_target_role
    )
    
    ex3.download_button(
        "Download Calendar (.ics)", 
        data=calendar_data, 
        file_name="Learning_Plan.ics",
        mime="text/calendar"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Change Inputs & Start Over", type="secondary"):
        reset_app()

st.markdown("---")
st.caption("E2M Solutions Technical Assessment - Developed by Garima Kalani")
