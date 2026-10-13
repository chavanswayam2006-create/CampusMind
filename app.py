import streamlit as st
from pathlib import Path
from modules import agent_rules, navigator, game_zone, comfort, insights

st.set_page_config(
    page_title="CampusMind - AI Academic Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    """Inject custom CSS from style.css for consistent dashboard aesthetics."""
    css_path = Path("style.css")
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

load_css()

# Left Sidebar Navigation
with st.sidebar:
    st.markdown('<div style="display:flex; align-items:center; gap:0.6rem; margin-bottom:1.2rem;">'
                '<span style="font-size:2rem;">🎓</span>'
                '<div><div style="font-size:1.35rem; font-weight:700; color:#1E293B;">CampusMind</div>'
                '<div style="font-size:0.8rem; color:#64748B;">AI Student Dashboard</div></div>'
                '</div>', unsafe_allow_html=True)
    
    menu_options = [
        "🤖 Agent & Rules",
        "🧭 Navigator",
        "🎮 Game Zone",
        "❄️ Comfort Control",
        "📊 Student Insights"
    ]
    
    choice = st.radio("Navigation Menu", menu_options, label_visibility="collapsed")
    
    st.markdown("<hr style='margin: 1.5rem 0; border-color:#E2E8F0;'>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:0.78rem; color:#94A3B8; line-height:1.5;">'
                'CampusMind showcases 10 fundamental AI practical techniques within a clean, student-friendly interface.'
                '</div>', unsafe_allow_html=True)

# Top Bar Header
clean_title = choice.split(" ", 1)[1] if " " in choice else choice
st.markdown(f'<div class="top-header">'
            f'<h1 class="top-title">{choice}</h1>'
            f'<div class="top-badge">⚡ Powered by 10 AI techniques</div>'
            f'</div>', unsafe_allow_html=True)

# Main Screen Dispatcher
if "Agent & Rules" in choice:
    agent_rules.run()
elif "Navigator" in choice:
    navigator.run()
elif "Game Zone" in choice:
    game_zone.run()
elif "Comfort Control" in choice:
    comfort.run()
elif "Student Insights" in choice:
    insights.run()
