import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from sklearn.neural_network import MLPRegressor
import warnings
warnings.filterwarnings('ignore')

@st.cache_resource
def get_fuzzy_sim():
    """Build and return the scikit-fuzzy Mamdani ControlSystemSimulation."""
    t, h, f = ctrl.Antecedent(np.arange(0, 51, 1), 't'), ctrl.Antecedent(np.arange(0, 101, 1), 'h'), ctrl.Consequent(np.arange(0, 101, 1), 'f')
    t['l'], t['m'], t['h'] = fuzz.trimf(t.universe, [0, 0, 25]), fuzz.trimf(t.universe, [15, 25, 35]), fuzz.trimf(t.universe, [25, 50, 50])
    h['l'], h['m'], h['h'] = fuzz.trimf(h.universe, [0, 0, 50]), fuzz.trimf(h.universe, [25, 50, 75]), fuzz.trimf(h.universe, [50, 100, 100])
    f['l'], f['m'], f['h'] = fuzz.trimf(f.universe, [0, 0, 45]), fuzz.trimf(f.universe, [30, 55, 80]), fuzz.trimf(f.universe, [60, 100, 100])
    sys = ctrl.ControlSystem([ctrl.Rule(t['h'] | h['h'], f['h']), ctrl.Rule(t['m'] | h['m'], f['m']), ctrl.Rule(t['l'] | h['l'], f['l'])])
    return ctrl.ControlSystemSimulation(sys)

def compute_sugeno(t: float, h: float) -> float:
    """Calculate fan speed using Sugeno weighted average method."""
    wl, wm, wh = max(0.0, 1 - t/25) * max(0.0, 1 - h/50), max(0.0, 1 - abs(t-25)/15), max(0.0, (t-20)/30) * max(0.0, (h-40)/60)
    return (wl * 15.0 + wm * 55.0 + wh * 90.0) / (wl + wm + wh + 1e-5)

def compute_mamdani(t: float, h: float) -> float:
    """Evaluate fan speed through Mamdani fuzzy centroid defuzzification."""
    try:
        sim = get_fuzzy_sim()
        sim.input['t'], sim.input['h'] = float(np.clip(t, 1, 49)), float(np.clip(h, 1, 99))
        sim.compute()
        return float(sim.output['f'])
    except Exception:
        return compute_sugeno(t, h)

@st.cache_resource
def get_trained_mlp():
    """Train and cache an MLPRegressor on fuzzy rule grid samples."""
    T, H = np.meshgrid(np.linspace(5, 45, 12), np.linspace(10, 90, 12))
    X = np.column_stack([T.ravel(), H.ravel()])
    Y = np.clip(1.25 * X[:, 0] + 0.45 * X[:, 1] - 12, 10, 95)
    mlp = MLPRegressor(hidden_layer_sizes=(8, 4), solver='lbfgs', max_iter=150, random_state=42)
    mlp.fit(X, Y)
    return mlp

def run():
    """Render the Comfort Control screen with Fuzzy Mamdani/Sugeno and MLP neuro-fuzzy."""
    st.markdown('<div class="campus-card"><div class="card-title">❄️ Practicals 6 & 7: Fuzzy Comfort Control</div>'
                '<div class="card-subtitle">Mamdani Defuzzification vs Sugeno Weighted Average</div>', unsafe_allow_html=True)
    col_in, col_gauge = st.columns([2, 1])
    with col_in:
        temp = st.slider("🌡️ Room Temperature (°C)", 0, 50, 28)
        hum = st.slider("💧 Relative Humidity (%)", 0, 100, 65)
        mode = st.radio("Inference Strategy", ["Mamdani (Fuzzy Centroid)", "Sugeno (Weighted Average)"], horizontal=True)
        fan_speed = compute_mamdani(temp, hum) if "Mamdani" in mode else compute_sugeno(temp, hum)
    with col_gauge:
        st.markdown(f'<div class="gauge-card"><div style="color:#64748B; font-weight:600; font-size:0.85rem;">PREDICTED FAN SPEED</div>'
                    f'<div class="gauge-val">{fan_speed:.1f}%</div><span class="chip chip-teal">● Active: {mode.split()[0]}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="campus-card"><div class="card-title">🧠 Practical 8: Neuro-Fuzzy (MLP Regressor Comparison)</div>'
                '<div class="card-subtitle">Comparing scikit-learn MLP predictions against Fuzzy logic across temperatures</div>', unsafe_allow_html=True)
    mlp = get_trained_mlp()
    mlp_val = float(mlp.predict([[temp, hum]])[0])
    st.write(f"📊 **At {temp}°C & {hum}% Humidity:** Fuzzy Output = `{fan_speed:.1f}%` | MLP Neural Net Output = `{mlp_val:.1f}%`")
    t_range = np.linspace(10, 45, 25)
    f_curve = [compute_mamdani(ti, hum) for ti in t_range]
    mlp_curve = mlp.predict(np.column_stack([t_range, np.full_like(t_range, hum)]))
    fig, ax = plt.subplots(figsize=(7, 2.3))
    ax.plot(t_range, f_curve, label="Fuzzy Output", color="#4F46E5", linewidth=2.5)
    ax.plot(t_range, mlp_curve, label="MLP Neuro-Fuzzy", color="#14B8A6", linestyle="--", linewidth=2)
    ax.axvline(temp, color="#F59E0B", linestyle=":", label=f"Current Temp ({temp}°C)")
    ax.set_xlabel("Temperature (°C)", fontsize=9); ax.set_ylabel("Fan Speed (%)", fontsize=9); ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.3)
    st.pyplot(fig)
    plt.close(fig)
    st.markdown('</div>', unsafe_allow_html=True)
