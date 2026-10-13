# 🎓 CampusMind - Student AI Academic Dashboard

A clean, light-mode dashboard web application built with Streamlit demonstrating **10 essential Artificial Intelligence practical techniques** across 5 intuitive study-tool screens.

Designed with light mode, crisp white cards on soft grey-blue (`#F4F7FB`), primary indigo (`#4F46E5`), accent teal (`#14B8A6`), warning amber (`#F59E0B`), and typography using Inter.

---

## 🚀 10 AI Techniques Mapping

| # | AI Technique | Module | Screen / Features |
|---|---|---|---|
| **1** | **PEAS Agent Framework** | `modules/agent_rules.py` | Specification cards for Campus Assistant Agent (Performance, Environment, Actuators, Sensors) |
| **2** | **Prolog Rule-Based Logic** | `modules/agent_rules.py` | Academic eligibility knowledge base (`attendance >= 75 AND cgpa >= 6.5`) with live Prolog code viewer |
| **3** | **Uninformed Graph Search (BFS & DFS)** | `modules/navigator.py` | Landmark routing on campus graph comparing Breadth-First vs Depth-First Search with connected step chips |
| **4** | **Informed Search (A* Algorithm)** | `modules/game_zone.py` | 8-Puzzle sliding tile solver with Manhattan distance heuristic and interactive next-move Hint engine |
| **5** | **Adversarial Search (Minimax Algorithm)** | `modules/game_zone.py` | Unbeatable Tic-Tac-Toe AI player calculating game-tree terminal states |
| **6** | **Fuzzy Logic (Mamdani Inference)** | `modules/comfort.py` | Smart study room fan speed control via centroid defuzzification with temperature & humidity inputs |
| **7** | **Sugeno Fuzzy Inference** | `modules/comfort.py` | Singleton / weighted-average fuzzy inference comparison toggle |
| **8** | **Neuro-Fuzzy Modeling (MLP Regressor)** | `modules/comfort.py` | Neural network (`MLPRegressor`) trained on fuzzy rules, visualized alongside fuzzy curves via Matplotlib |
| **9** | **Supervised & Unsupervised Learning** | `modules/insights.py` | Perceptron pass/risk predictor + Competitive Learning clustering 30 students into 3 cohorts with scatter plot |
| **10** | **Statistical N-Gram Language Modeling** | `modules/insights.py` | Bigram & Trigram frequency-based next-word autocomplete for Campus FAQ assistant |

---

## 📁 Project File Structure

```text
ResQ/
├── .streamlit/
│   └── config.toml          # Custom light theme and server configuration
├── modules/
│   ├── __init__.py          # Module package initializer
│   ├── agent_rules.py       # Practicals 1 & 2: PEAS & Prolog
│   ├── navigator.py         # Practical 3: BFS & DFS
│   ├── game_zone.py         # Practicals 4 & 5: A* 8-Puzzle & Minimax Tic-Tac-Toe
│   ├── comfort.py           # Practicals 6, 7 & 8: Fuzzy & Neuro-Fuzzy MLP
│   └── insights.py          # Practicals 9 & 10: Perceptron, Clustering & N-Gram NLP
├── app.py                   # Main Streamlit dashboard application with sidebar routing
├── requirements.txt         # Pinned Python package dependencies
├── rules.pl                 # Prolog knowledge base facts and eligibility rules
├── style.css                # Custom CSS styling (Inter font, cards, chips, responsive design)
└── README.md                # Documentation and running instructions
```

---

## 🛠️ Quickstart Commands

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the Streamlit application
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

---

## ✅ Acceptance Test Checklist

- [x] **Light Mode & Aesthetics**: Soft grey-blue background (`#F4F7FB`), clean white cards, Inter typography, 12px rounded corners, chips and badges.
- [x] **Practical 1 (PEAS)**: 4 cards for Performance, Environment, Actuators, and Sensors.
- [x] **Practical 2 (Prolog)**: Student selection dropdown, eligibility check, red/green chip, and `rules.pl` display.
- [x] **Practical 3 (BFS & DFS)**: Campus graph routing between landmarks, step count and step chips.
- [x] **Practical 4 (A* 8-Puzzle)**: 3x3 interactive puzzle with Manhattan distance "Hint (A*)" button.
- [x] **Practical 5 (Minimax Tic-Tac-Toe)**: Interactive board, minimax AI responds, unbeatable play.
- [x] **Practical 6 & 7 (Mamdani & Sugeno Fuzzy)**: Temperature & humidity sliders, fan speed gauge %, mode toggle.
- [x] **Practical 8 (Neuro-Fuzzy MLP)**: Live MLP comparison against fuzzy output with Matplotlib curves.
- [x] **Practical 9 (Perceptron & Clustering)**: Pass/risk prediction badge + 3-cluster competitive learning scatter plot.
- [x] **Practical 10 (N-Gram FAQ NLP)**: Query input with 3 dynamic next-word suggestion chips.
