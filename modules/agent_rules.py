import streamlit as st

STUDENTS = {
    "Aarav Sharma": {"attendance": 85, "cgpa": 8.2},
    "Diya Patel": {"attendance": 72, "cgpa": 7.8},
    "Rohan Verma": {"attendance": 90, "cgpa": 6.1},
    "Ananya Iyer": {"attendance": 78, "cgpa": 7.0},
}

def check_eligibility(att: float, cgpa: float) -> tuple[bool, str]:
    """Evaluate eligibility using Prolog rule: attendance >= 75 and cgpa >= 6.5."""
    if att >= 75 and cgpa >= 6.5:
        return True, f"Eligible (Attendance: {att}%, CGPA: {cgpa})"
    reasons = []
    if att < 75:
        reasons.append(f"Attendance {att}% < 75%")
    if cgpa < 6.5:
        reasons.append(f"CGPA {cgpa} < 6.5")
    return False, f"Not Eligible: {', '.join(reasons)}"

def run():
    """Render the Agent PEAS framework and Prolog rule eligibility interface."""
    st.markdown('<div class="campus-card">'
                '<div class="card-title">🤖 Practical 1: PEAS Campus Assistant Agent</div>'
                '<div class="card-subtitle">Formal specification: Performance, Environment, Actuators & Sensors</div>',
                unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown('<div class="peas-box"><div class="peas-label">Performance</div>'
                '<div class="peas-text">High GPA success, timely task alerts, 95%+ query accuracy</div></div>', unsafe_allow_html=True)
    c2.markdown('<div class="peas-box"><div class="peas-label">Environment</div>'
                '<div class="peas-text">Campus portal, lecture halls, library LMS, student union</div></div>', unsafe_allow_html=True)
    c3.markdown('<div class="peas-box"><div class="peas-label">Actuators</div>'
                '<div class="peas-text">Push notifications, calendar invites, automated advisories</div></div>', unsafe_allow_html=True)
    c4.markdown('<div class="peas-box"><div class="peas-label">Sensors</div>'
                '<div class="peas-text">Attendance card scans, LMS exam marks feed, user queries</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="campus-card">'
                '<div class="card-title">📜 Practical 2: Prolog Knowledge Base Eligibility</div>'
                '<div class="card-subtitle">Evaluates rule: attendance >= 75% AND CGPA >= 6.5 (mirrored from rules.pl)</div>',
                unsafe_allow_html=True)
    col_left, col_right = st.columns([1, 1])
    with col_left:
        name = st.selectbox("Select Student", list(STUDENTS.keys()))
        s = STUDENTS[name]
        st.write(f"📊 **Attendance:** {s['attendance']}% | **CGPA:** {s['cgpa']}")
        if st.button("Check Eligibility", type="primary"):
            ok, msg = check_eligibility(s['attendance'], s['cgpa'])
            cls = "chip-green" if ok else "chip-red"
            st.markdown(f'<span class="chip {cls}">● {msg}</span>', unsafe_allow_html=True)
    with col_right:
        try:
            with open("rules.pl", "r") as f:
                st.code(f.read(), language="prolog")
        except FileNotFoundError:
            st.info("rules.pl not found.")
    st.markdown('</div>', unsafe_allow_html=True)
