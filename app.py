import random
import time
from datetime import datetime, timedelta

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Smart Plant Monitor", page_icon="🌱", layout="wide")
st.markdown("""<style>
.stApp{background:radial-gradient(circle at 15% 10%,#12352b 0%,#0b1a17 40%,#070d0c 100%);color:#e8f5ee}
[data-testid="stSidebar"]{background:rgba(255,255,255,.03);border-right:1px solid rgba(255,255,255,.08)}
.hero{display:flex;align-items:center;gap:22px;padding:18px 8px 6px}
.hero-emoji{font-size:78px;animation:float 3.2s ease-in-out infinite;filter:drop-shadow(0 0 18px rgba(74,222,128,.55))}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.hero-title{font-size:2.6rem;font-weight:800;line-height:1.1;background:linear-gradient(90deg,#86efac,#22d3ee,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero-sub{color:#9bbfae;margin-top:4px}
.glass{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:18px 20px;backdrop-filter:blur(10px);box-shadow:0 8px 32px rgba(0,0,0,.35)}
.pill{display:inline-block;padding:4px 12px;border-radius:999px;font-size:.8rem;font-weight:600;letter-spacing:.5px;background:rgba(74,222,128,.15);color:#86efac;border:1px solid rgba(74,222,128,.4)}
.pill.warn{background:rgba(251,191,36,.15);color:#fcd34d;border-color:rgba(251,191,36,.4)}
.pill.bad{background:rgba(248,113,113,.15);color:#fca5a5;border-color:rgba(248,113,113,.4)}
.big-num{font-size:3.2rem;font-weight:800;line-height:1}
.label{color:#9bbfae;font-size:.85rem;text-transform:uppercase;letter-spacing:1.5px}
.pump{text-align:center}.pump-icon{font-size:54px}
.pump.on{animation:glow 1.4s ease-in-out infinite;border-color:rgba(34,211,238,.7)}
@keyframes glow{0%,100%{box-shadow:0 0 10px rgba(34,211,238,.25)}50%{box-shadow:0 0 38px rgba(34,211,238,.85)}}
.tip{padding:10px 14px;margin:8px 0;border-radius:12px;background:rgba(255,255,255,.05);border-left:4px solid #4ade80}
.tip.warn{border-left-color:#fbbf24}.tip.bad{border-left-color:#f87171}
.footer{text-align:center;color:#6b8c7c;font-size:.8rem;margin-top:30px}
</style>""", unsafe_allow_html=True)

PLANTS = {
    "🌿 Tulsi (Holy Basil)": dict(moist=(50, 70), temp=(20, 35), hum=(40, 70), threshold=45),
    "🌵 Cactus": dict(moist=(10, 30), temp=(18, 38), hum=(20, 50), threshold=15),
    "🪴 Money Plant": dict(moist=(40, 70), temp=(18, 30), hum=(40, 70), threshold=40),
    "🍅 Tomato": dict(moist=(60, 80), temp=(20, 30), hum=(50, 70), threshold=55),
    "🌹 Rose": dict(moist=(50, 70), temp=(15, 28), hum=(40, 70), threshold=45),
}
ss = st.session_state
clamp = lambda v, lo, hi: max(lo, min(hi, v))


def seed():
    now, s, rows = datetime.now(), 78.0, []
    for i in range(14, 0, -1):
        s = clamp(s - random.uniform(1, 3.5), 5, 100)
        rows.append(dict(time=(now - timedelta(minutes=i * 5)).strftime("%H:%M"), moisture=round(s, 1)))
    return rows


def card(html, cls=""):
    st.markdown(f'<div class="glass {cls}">{html}</div>', unsafe_allow_html=True)


@st.cache_resource
def load_model():
    return joblib.load("model/plant_model.pkl")


if "init" not in ss:
    ss.update(init=True, plant="🌿 Tulsi (Holy Basil)", soil=35, temperature=28, humidity=65,
              threshold=45, live=False, history=seed(), pump_runs=0, _tick=False)

# Live simulation tick (must run before widgets are created)
if ss._tick:
    ss._tick = False
    if ss.soil < ss.threshold:
        ss.soil, ss.pump_runs = clamp(ss.soil + random.randint(5, 9), 0, 100), ss.pump_runs + 1
    else:
        ss.soil = clamp(ss.soil - random.randint(1, 4), 0, 100)
    ss.temperature = clamp(ss.temperature + random.choice([-1, 0, 0, 1]), 0, 50)
    ss.humidity = clamp(ss.humidity + random.choice([-2, -1, 0, 1, 2]), 0, 100)
    ss.history = (ss.history + [dict(time=datetime.now().strftime("%H:%M:%S"), moisture=float(ss.soil))])[-30:]

# Sidebar
sb = st.sidebar
sb.markdown("## 🎛️ Control Room")
sb.selectbox("Plant profile", list(PLANTS), key="plant",
             on_change=lambda: ss.update(threshold=PLANTS[ss.plant]["threshold"]))
sb.markdown("### 📡 Sensors")
soil = sb.slider("💧 Soil Moisture (%)", 0, 100, key="soil")
temperature = sb.slider("🌡️ Temperature (°C)", 0, 50, key="temperature")
humidity = sb.slider("☁️ Humidity (%)", 0, 100, key="humidity")
sb.markdown("### ⚙️ Automation")
threshold = sb.slider("🚰 Watering Threshold (%)", 5, 90, key="threshold")
sb.toggle("🔴 Live simulation (auto-updates every 2s)", key="live")
if sb.button("♻️ Reset history", use_container_width=True):
    ss.history, ss.pump_runs = seed(), 0
    st.rerun()
sb.caption("Demo mode: no real pump is being controlled.")

# Logic
profile = PLANTS[ss.plant]
pump_on = soil < threshold
(m_lo, m_hi), (t_lo, t_hi), (h_lo, h_hi) = profile["moist"], profile["temp"], profile["hum"]

X = pd.DataFrame({"soil_moisture": [soil], "temperature": [temperature], "humidity": [humidity]})
model = load_model()
ml_needs_water = model.predict(X)[0] == 1
ml_prob = model.predict_proba(X)[0][1] * 100


def band(v, lo, hi, tol):
    return 100.0 if lo <= v <= hi else max(0.0, 100 - min(abs(v - lo), abs(v - hi)) / tol * 100)


health = round(0.5 * band(soil, m_lo, m_hi, 30) + 0.25 * band(temperature, t_lo, t_hi, 15)
               + 0.25 * band(humidity, h_lo, h_hi, 35))

if soil > m_hi + 15:
    face, mood, cls, msg = "💦", "Overwatered", "warn", "Roots might be drowning. Ease off the water."
elif soil < threshold * 0.5:
    face, mood, cls, msg = "🥀", "Critical", "bad", "I'm parched! Pump is working overtime."
elif soil < threshold:
    face, mood, cls, msg = "😟", "Thirsty", "warn", "Getting dry. Watering kicks in now."
elif health >= 80:
    face, mood, cls, msg = "🪴", "Thriving", "", "Perfect vibes. Photosynthesis intensifies."
else:
    face, mood, cls, msg = "🌱", "Doing okay", "", "Healthy, but conditions could be better."

# Hero
st.markdown(f"""<div class="hero"><div class="hero-emoji">{face}</div><div>
<div class="hero-title">Smart Plant Monitor</div>
<div class="hero-sub">IoT auto-watering dashboard · ESP32 + Machine Learning · {ss.plant}</div></div></div>""",
            unsafe_allow_html=True)

# ML prediction
st.markdown("### 🧠 Machine Learning Prediction")
c1, c2 = st.columns(2)
c1.metric("ML Watering Prediction", "WATERING REQUIRED 💧" if ml_needs_water else "NO WATERING REQUIRED 🌿")
c2.metric("Model Prediction Probability", f"{ml_prob:.2f}%")
st.caption("Prediction generated using the trained Random Forest model.")

# Top cards
c1, c2, c3 = st.columns([1.2, 1.6, 1])
with c1:
    card(f'<div class="label">Plant Health Score</div><div class="big-num">{health}'
         f'<span style="font-size:1.4rem;color:#9bbfae"> /100</span></div>'
         f'<div style="margin-top:10px"><span class="pill {cls}">{mood.upper()}</span></div>')
with c2:
    card(f'<div class="label">Plant says</div><div style="font-size:1.35rem;font-weight:600;margin:8px 0 4px">"{msg}"</div>'
         f'<div style="color:#9bbfae;font-size:.9rem">Ideal moisture {m_lo}–{m_hi}% · temp {t_lo}–{t_hi}°C · humidity {h_lo}–{h_hi}%</div>')
with c3:
    card(f'<div class="pump-icon">{"💧" if pump_on else "😴"}</div><div class="label">Water Pump</div>'
         f'<div style="font-size:1.8rem;font-weight:800;color:{"#22d3ee" if pump_on else "#9bbfae"}">{"ON" if pump_on else "OFF"}</div>'
         f'<div style="color:#6b8c7c;font-size:.8rem">{ss.pump_runs} auto-waterings this session</div>',
         "pump on" if pump_on else "pump")

st.write("")

# Gauges
GOOD = "rgba(74,222,128,0.25)"


def gauge(value, title, suffix, rng, color, steps, line=None):
    cfg = dict(axis=dict(range=rng, tickcolor="#6b8c7c"), bar=dict(color=color, thickness=0.3),
               bgcolor="rgba(255,255,255,0.04)", borderwidth=0, steps=steps)
    if line is not None:
        cfg["threshold"] = dict(line=dict(color="#fff", width=4), thickness=0.85, value=line)
    fig = go.Figure(go.Indicator(mode="gauge+number", value=value,
                                 number=dict(suffix=suffix, font=dict(color="#e8f5ee", size=40)),
                                 title=dict(text=title, font=dict(color="#9bbfae", size=16)), gauge=cfg))
    fig.update_layout(height=240, margin=dict(l=25, r=25, t=60, b=10), paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="#e8f5ee"))
    return fig


gauges = [
    (soil, "💧 Soil Moisture", "%", [0, 100], "#f87171" if pump_on else "#22d3ee",
     [dict(range=[0, threshold], color="rgba(248,113,113,0.25)"), dict(range=[m_lo, m_hi], color=GOOD)], threshold),
    (temperature, "🌡️ Temperature", " °C", [0, 50], "#fb923c", [dict(range=[t_lo, t_hi], color=GOOD)], None),
    (humidity, "☁️ Humidity", "%", [0, 100], "#a78bfa", [dict(range=[h_lo, h_hi], color=GOOD)], None),
]
for col, g in zip(st.columns(3), gauges):
    col.plotly_chart(gauge(*g), use_container_width=True)

# Timeline + insights
left, right = st.columns([2, 1])
with left:
    st.markdown("#### 📈 Moisture Timeline")
    hist = pd.DataFrame(ss.history + [dict(time="Now", moisture=float(soil))])
    fig = go.Figure()
    fig.add_scatter(x=hist.time, y=hist.moisture, mode="lines", line=dict(color="#22d3ee", width=3, shape="spline"),
                    fill="tozeroy", fillcolor="rgba(34,211,238,0.12)")
    fig.add_scatter(x=hist.time, y=hist.moisture, mode="markers",
                    marker=dict(size=9, line=dict(color="#0b1a17", width=2),
                                color=["#f87171" if m < threshold else "#4ade80" for m in hist.moisture]),
                    hovertemplate="%{x}<br>%{y}%<extra></extra>")
    fig.add_hline(y=threshold, line=dict(color="#fbbf24", dash="dash"),
                  annotation_text="Watering threshold", annotation_font_color="#fbbf24")
    fig.update_layout(height=340, showlegend=False, margin=dict(l=10, r=10, t=10, b=10),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font=dict(color="#c9e6d6"),
                      yaxis=dict(range=[0, 100], title="Moisture (%)", gridcolor="rgba(255,255,255,0.07)"),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.04)"))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### 🧠 Smart Insights")
    tips = [("bad" if soil < threshold * 0.5 else "warn", "Soil is below threshold, so the pump is watering now.")
            if pump_on else ("", "Moisture is above threshold, so the pump rests.")]
    if temperature > t_hi: tips.append(("warn", "It's hot. Expect faster evaporation and consider shade."))
    if temperature < t_lo: tips.append(("warn", "It's cold for this plant. Keep it away from drafts."))
    if humidity < h_lo: tips.append(("warn", "Air is dry. Try misting or a pebble tray."))
    if humidity > h_hi: tips.append(("warn", "High humidity raises fungal risk. Improve airflow."))
    if soil > m_hi + 15: tips.append(("warn", "Soil is very wet. Skip watering and check drainage."))
    if len(tips) == 1 and not pump_on: tips.append(("", "Temperature and humidity are in the sweet spot. 🌤️"))
    for c, t in tips:
        st.markdown(f'<div class="tip {c}">{t}</div>', unsafe_allow_html=True)

# Log + footer
with st.expander("📋 Raw sensor log"):
    st.dataframe(pd.DataFrame(ss.history).rename(columns={"time": "Time", "moisture": "Moisture (%)"}).iloc[::-1],
                 use_container_width=True, hide_index=True)
st.markdown(f'<div class="footer">Smart Plant IoT Project · ESP32 + Machine Learning · '
            f'Last updated {datetime.now():%d-%m-%Y %H:%M:%S} · Demo values only</div>', unsafe_allow_html=True)

# Live loop
if ss.live:
    time.sleep(2)
    ss._tick = True
    st.rerun()