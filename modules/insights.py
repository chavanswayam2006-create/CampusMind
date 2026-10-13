import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict, Counter
from sklearn.linear_model import Perceptron

FAQS = [
    "where is the campus library located", "how to register for placement cell drives",
    "what is the minimum attendance requirement for exams", "how to check semester marks and grades",
    "where can students submit course assignments", "canteen lunch hours are from twelve to two",
    "how to pay semester hostel fees online", "where is the admin block and accounts desk",
    "when will semester exam dates be announced", "how to contact faculty advisor and mentor",
    "library timings are eight am to eight pm", "placement cell organizes mock interviews next week",
    "what is the attendance policy for scholarship", "canteen offers fresh food and snacks daily",
    "how to access online study materials and notes", "laboratory practical exams start next monday morning",
    "where to submit scholarship application forms", "how to apply for campus bus pass",
    "what is the passing marks for end term exams", "annual technical and cultural festival begins next month"
]

@st.cache_data
def get_student_sample_data() -> tuple[np.ndarray, np.ndarray]:
    """Generate 30 synthetic student records with attendance, marks, and assignments."""
    np.random.seed(42)
    att = np.random.randint(45, 98, 30)
    marks = np.random.randint(40, 95, 30)
    assgn = np.random.randint(2, 11, 30)
    X = np.column_stack([att, marks, assgn])
    y = ((att >= 75) & (marks >= 50) & (assgn >= 5)).astype(int)
    return X, y

def train_perceptron(X: np.ndarray, y: np.ndarray) -> Perceptron:
    """Train a Perceptron classifier to detect at-risk vs safe academic status."""
    return Perceptron(max_iter=100, random_state=42).fit(X, y)

def run_competitive_learning(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Cluster 30 students into 3 cohorts via unsupervised competitive learning."""
    W = np.array([[55.0, 50.0, 3.0], [75.0, 70.0, 6.0], [90.0, 88.0, 9.0]])
    for _ in range(15):
        for row in X:
            W[np.argmin(np.linalg.norm(W - row, axis=1))] += 0.15 * (row - W[np.argmin(np.linalg.norm(W - row, axis=1))])
    clusters = np.array([np.argmin(np.linalg.norm(W - row, axis=1)) for row in X])
    return clusters, W

def get_ngram_suggestions(text: str) -> list[str]:
    """Predict top 3 next words using bigram and trigram frequency counts on campus FAQs."""
    bigrams, trigrams = defaultdict(Counter), defaultdict(Counter)
    for s in FAQS:
        words = s.lower().split()
        for i in range(len(words)-1): bigrams[words[i]][words[i+1]] += 1
        for i in range(len(words)-2): trigrams[(words[i], words[i+1])][words[i+2]] += 1
    w = text.lower().strip().split()
    preds = [word for word, _ in trigrams.get((w[-2], w[-1]), Counter()).most_common(3)] if len(w) >= 2 else []
    if len(preds) < 3 and len(w) >= 1:
        for word, _ in bigrams.get(w[-1], Counter()).most_common(3):
            if word not in preds: preds.append(word)
    for default in ["campus", "library", "exam", "fees"]:
        if len(preds) < 3 and default not in preds: preds.append(default)
    return preds[:3]

def run():
    """Render Student Insights covering Perceptron risk, competitive clustering, and N-gram FAQ chat."""
    X, y = get_student_sample_data()
    perceptron = train_perceptron(X, y)
    clusters, W = run_competitive_learning(X)

    st.markdown('<div class="campus-card"><div class="card-title">📊 Practical 9: Academic Risk (Perceptron) & Clustering</div>'
                '<div class="card-subtitle">Supervised Perceptron Classifier + Unsupervised Competitive Learning (3 Clusters)</div>', unsafe_allow_html=True)
    c_in, c_plot = st.columns([1, 1.3])
    with c_in:
        att = st.slider("Attendance (%)", 0, 100, 78)
        marks = st.slider("Semester Marks (%)", 0, 100, 68)
        assgn = st.slider("Assignments Completed (0-10)", 0, 10, 7)
        if st.button("Predict Risk (Perceptron)", type="primary"):
            pred = perceptron.predict([[att, marks, assgn]])[0]
            st.session_state.risk_pred = "Safe / Low Risk" if pred == 1 else "Action Required / At Risk"
            st.session_state.risk_color = "chip-green" if pred == 1 else "chip-red"
        if "risk_pred" in st.session_state:
            st.markdown(f'<span class="chip {st.session_state.risk_color}">● Result: {st.session_state.risk_pred}</span>', unsafe_allow_html=True)
    with c_plot:
        fig, ax = plt.subplots(figsize=(4.8, 3.2))
        colors = ["#4F46E5", "#14B8A6", "#F59E0B"]
        labels = ["Needs Support", "Average", "High Achievers"]
        for k in range(3):
            pts = X[clusters == k]
            ax.scatter(pts[:, 0], pts[:, 1], c=colors[k], label=labels[k], alpha=0.8, s=45)
            ax.scatter(W[k, 0], W[k, 1], c=colors[k], marker="*", s=160, edgecolor="black")
        ax.scatter([att], [marks], c="red", marker="X", s=110, label="Current Input")
        ax.set_xlabel("Attendance (%)", fontsize=8); ax.set_ylabel("Marks (%)", fontsize=8)
        ax.legend(fontsize=7, loc="lower right"); ax.grid(True, linestyle="--", alpha=0.3)
        st.pyplot(fig)
        plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="campus-card"><div class="card-title">💬 Practical 10: Campus FAQ Chat (Bigram / Trigram NLP)</div>'
                '<div class="card-subtitle">Statistical language modeling predicts the next word based on 20 campus FAQ sentences</div>', unsafe_allow_html=True)
    query = st.text_input("Ask CampusMind a question (try: 'where is the' or 'how to'):", value="where is the")
    next_words = get_ngram_suggestions(query)
    chips_html = " ".join([f'<span class="chip chip-indigo">💡 {w}</span>' for w in next_words])
    st.markdown(f'<div><b>Next-Word Suggestions:</b> {chips_html}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
