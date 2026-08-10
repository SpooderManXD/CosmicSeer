import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Scripts"))

import streamlit as st
import streamlit.components.v1 as components
import base64
from logic import calculate_kardashev, get_tier_label
from ui import (
    inject_css, render_header, render_k_gauge,
    render_power_breakdown, render_advisor_panel, render_input_label
)
from ai import generate_advisor_response

st.set_page_config(
    page_title="CosmoSeer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

BASE_DIR = r"C:\Users\Temp_Baitan\Documents\GitHub\CosmicSeer"

def img_to_base64(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

t1_b64 = img_to_base64(os.path.join(BASE_DIR, "type_1_background.jpg"))
t2_b64 = img_to_base64(os.path.join(BASE_DIR, "type_2_background.jpg"))
t3_b64 = img_to_base64(os.path.join(BASE_DIR, "type_3_background.jpg"))

ORB_HTML = """
<!DOCTYPE html>
<html>
<head>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; overflow: hidden; }
  canvas { border-radius: 50%; filter: drop-shadow(0 0 20px rgba(0, 212, 255, 0.4)); cursor: pointer; }
</style>
</head>
<body>
<canvas id="orb" width="800" height="600"></canvas>
<script>
var canvas = document.getElementById('orb');
var ctx = canvas.getContext('2d');
var W = 800, H = 600, baseCx = W/2, baseCy = H/2, t = 0;

var orbX = baseCx;
var orbY = baseCy;

var mouse = { x: -1000, y: -1000, active: false };

canvas.addEventListener('mousemove', function(e) {
  var rect = canvas.getBoundingClientRect();
  mouse.x = e.clientX - rect.left;
  mouse.y = e.clientY - rect.top;
  mouse.active = true;
});

canvas.addEventListener('mouseleave', function() {
  mouse.active = false;
});

var numPoints = 16;
var points = [];
for (var i = 0; i < numPoints; i++) {
  points.push({
    baseAngle: (i / numPoints) * Math.PI * 2,
    phase: i * 0.4,
    speed: 1.2 + (i % 3) * 0.3,
    amp: 4 + (i % 2) * 3
  });
}

function draw() {
  t += 0.025;
  ctx.clearRect(0, 0, W, H);

  var targetX = baseCx;
  var targetY = baseCy;

  if (mouse.active) {
    var dxCenter = mouse.x - baseCx;
    var dyCenter = mouse.y - baseCy;
    var distCenter = Math.sqrt(dxCenter * dxCenter + dyCenter * dyCenter);
    
    if (distCenter < 600) {
      var pullFactor = 0.55;
      targetX = baseCx + dxCenter * pullFactor;
      targetY = baseCy + dyCenter * pullFactor;
    }
  }

  orbX += (targetX - orbX) * 0.08;
  orbY += (targetY - orbY) * 0.08;

  var baseRadius = 130;
  var calculated = [];

  for (var i = 0; i < numPoints; i++) {
    var p = points[i];
    var r = baseRadius + Math.sin(t * p.speed + p.phase) * p.amp + Math.cos(t * 0.8 + p.phase * 2) * 2;

    var px = orbX + Math.cos(p.baseAngle) * r;
    var py = orbY + Math.sin(p.baseAngle) * r;

    if (mouse.active) {
      var dx = px - mouse.x;
      var dy = py - mouse.y;
      var dist = Math.sqrt(dx * dx + dy * dy);
      var maxDist = 250;

      if (dist < maxDist) {
        var force = (1 - dist / maxDist) * 16;
        px += (dx / dist) * force;
        py += (dy / dist) * force;
      }
    }

    calculated.push({ x: px, y: py });
  }

  var outerGlow = ctx.createRadialGradient(orbX, orbY, baseRadius * 0.8, orbX, orbY, baseRadius + 30);
  outerGlow.addColorStop(0, 'rgba(0, 212, 255, 0.25)');
  outerGlow.addColorStop(1, 'rgba(0, 212, 255, 0)');
  ctx.fillStyle = outerGlow;
  ctx.beginPath();
  ctx.arc(orbX, orbY, baseRadius + 30, 0, Math.PI * 2);
  ctx.fill();

  ctx.beginPath();
  var firstMidX = (calculated[0].x + calculated[numPoints - 1].x) / 2;
  var firstMidY = (calculated[0].y + calculated[numPoints - 1].y) / 2;
  ctx.moveTo(firstMidX, firstMidY);

  for (var i = 0; i < numPoints; i++) {
    var pNext = calculated[(i + 1) % numPoints];
    var pCurr = calculated[i];
    var midX = (pCurr.x + pNext.x) / 2;
    var midY = (pCurr.y + pNext.y) / 2;
    ctx.quadraticCurveTo(pCurr.x, pCurr.y, midX, midY);
  }
  ctx.closePath();

  var fluidGrad = ctx.createRadialGradient(orbX - 30, orbY - 30, 10, orbX, orbY, baseRadius);
  fluidGrad.addColorStop(0, '#5ce1ff');
  fluidGrad.addColorStop(0.7, '#00d4ff');
  fluidGrad.addColorStop(1, '#0088cc');
  ctx.fillStyle = fluidGrad;
  ctx.fill();

  var highlightOffsetX = Math.sin(t * 1.5) * 8;
  var highlightOffsetY = Math.cos(t * 1.2) * 8;

  if (mouse.active) {
    var dxH = mouse.x - orbX;
    var dyH = mouse.y - orbY;
    highlightOffsetX += dxH * 0.18;
    highlightOffsetY += dyH * 0.18;
  }

  ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
  ctx.beginPath();
  ctx.arc(orbX - 35 + highlightOffsetX, orbY - 35 + highlightOffsetY, 42, 0, Math.PI * 2);
  ctx.fill();

  requestAnimationFrame(draw);
}
draw();
</script>
</body>
</html>
"""

inject_css()

if "page" not in st.session_state:
    st.session_state["page"] = "main"
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "TYPE I"

if st.session_state["page"] == "orb_view":
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #04060f !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.15)) !important;
        color: #00d4ff !important;
        border: 1px solid #1e3a5f !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 13px !important;
        letter-spacing: 0.08em !important;
        border-radius: 6px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    col = st.columns([1, 6, 1])[1]
    with col:
        components.html(ORB_HTML, height=610)

    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)

    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        if st.button("View Analysis Report", use_container_width=True):
            st.session_state["page"] = "advisor_response"
            st.rerun()

elif st.session_state["page"] == "advisor_response":
    advisor_data = st.session_state.get("advisor_data", {})

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #04060f !important;
        font-family: 'Space Grotesk', sans-serif;
    }
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stButton"] > button {
        background: linear-gradient(135deg, rgba(0,212,255,0.15), rgba(124,58,237,0.15)) !important;
        color: #00d4ff !important;
        border: 1px solid #1e3a5f !important;
        font-family: 'Space Mono', monospace !important;
        font-size: 13px !important;
        letter-spacing: 0.08em !important;
        border-radius: 6px !important;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;padding:48px 0 8px;">
        <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.3em;color:#00d4ff;text-transform:uppercase;margin-bottom:12px;">CosmoSeer Advisory</div>
        <h2 style="font-family:'Space Grotesk',sans-serif;font-size:32px;font-weight:700;color:#e2e8f0;margin:0;">Cosmic Intelligence Report</h2>
    </div>
    """, unsafe_allow_html=True)

    if "advisor_response" not in st.session_state:
        with st.spinner("Consulting CosmoSeer..."):
            data = advisor_data
            tier_label = f"{data['tier_type']} ({data['tier_desc']})"
            response = generate_advisor_response(
                data["solar"], data["fusion"], data["ai_boost"],
                data["dyson"], data["harvesters"],
                data["stars"], data["blackholes"],
                data["k_score"], data["total_watts"], tier_label
            )
            st.session_state["advisor_response"] = response
            st.rerun()

    st.markdown(f"""
    <div style="max-width:760px;margin:32px auto 0;background:#0c1221;border:1px solid #1e3a5f;border-left:3px solid #00d4ff;border-radius:8px;padding:32px 36px;">
        <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;color:#00d4ff;text-transform:uppercase;margin-bottom:16px;">
            Advisory Report  /  K-Index {advisor_data.get('k_score', 0):.4f}  /  {advisor_data.get('tier_type','')} {advisor_data.get('tier_desc','')}
        </div>
        <p style="font-size:15px;color:#94a3b8;line-height:1.8;margin:0;font-family:'Space Grotesk',sans-serif;">
            {st.session_state['advisor_response']}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)

    col = st.columns([1, 1, 1])[1]
    with col:
        if st.button("Try More Values", use_container_width=True):
            if "advisor_response" in st.session_state:
                del st.session_state["advisor_response"]
            st.session_state["page"] = "main"
            st.rerun()

else:
    render_header()

    bg_map = {"TYPE I": t1_b64, "TYPE II": t2_b64, "TYPE III": t3_b64}
    active_bg = bg_map.get(st.session_state["active_tab"])
    if active_bg:
        st.markdown(f"""
        <style>
        [data-testid="stAppViewContainer"] > .main {{
            background-image: url("data:image/jpeg;base64,{active_bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        [data-testid="stAppViewContainer"] > .main::before {{
            content: '';
            position: fixed;
            inset: 0;
            background: rgba(4, 6, 15, 0.82);
            pointer-events: none;
            z-index: 0;
        }}
        </style>
        """, unsafe_allow_html=True)

    left, right = st.columns([1.1, 1], gap="large")

    with left:
        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;color:#475569;text-transform:uppercase;margin-bottom:20px;padding-bottom:12px;border-bottom:1px solid #1a2540;">
        Energy Infrastructure Configuration</div>
        """, unsafe_allow_html=True)

        tab1, tab2, tab3 = st.tabs(["TYPE I / Planetary", "TYPE II / Stellar", "TYPE III / Galactic"])

        solar = fusion = ai_boost = dyson = harvesters = stars = blackholes = 0

        with tab1:
            st.session_state["active_tab"] = "TYPE I"
            render_input_label("Solar Panel Coverage (%)")
            solar = st.slider("solar", 0, 100, 10, label_visibility="collapsed")
            render_input_label("Fusion Reactor Plants")
            fusion = st.number_input("fusion", min_value=0, max_value=10000, value=100, step=10, label_visibility="collapsed")
            render_input_label("AI Optimization Boost (%)")
            ai_boost = st.slider("ai_boost", 0, 100, 5, label_visibility="collapsed")

        with tab2:
            st.session_state["active_tab"] = "TYPE II"
            render_input_label("Dyson Swarm Coverage (%)")
            dyson = st.slider("dyson", 0, 100, 0, label_visibility="collapsed")
            render_input_label("Stellar Harvesters")
            harvesters = st.number_input("harvesters", min_value=0, max_value=1000, value=0, step=1, label_visibility="collapsed")

        with tab3:
            st.session_state["active_tab"] = "TYPE III"
            render_input_label("Colonized Star Systems")
            stars = st.number_input("stars", min_value=0, max_value=100000, value=0, step=100, label_visibility="collapsed")
            render_input_label("Black Hole Extraction (%)")
            blackholes = st.slider("blackholes", 0, 100, 0, label_visibility="collapsed")

        st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
        run_advisor = st.button("Run CosmoSeer Advisory", use_container_width=True)

    with right:
        total_watts, k_score, type_1, type_2, type_3 = calculate_kardashev(
            solar, fusion, ai_boost,
            dyson, harvesters,
            stars, blackholes
        )
        tier_type, tier_desc = get_tier_label(k_score)

        render_k_gauge(k_score, tier_type, tier_desc)

        st.markdown("""
        <div style="font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;color:#475569;text-transform:uppercase;margin:24px 0 12px;">
        Power Breakdown by Tier</div>
        """, unsafe_allow_html=True)

        render_power_breakdown(type_1, type_2, type_3, total_watts)

        st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Output", f"{total_watts:.2e} W")
        with col_b:
            st.metric("Kardashev Index", f"{k_score:.4f}")

    if run_advisor:
        st.session_state["advisor_data"] = {
            "solar": solar, "fusion": fusion, "ai_boost": ai_boost,
            "dyson": dyson, "harvesters": harvesters,
            "stars": stars, "blackholes": blackholes,
            "k_score": k_score, "total_watts": total_watts,
            "tier_type": tier_type, "tier_desc": tier_desc
        }
        st.session_state["page"] = "orb_view"
        st.rerun()

    st.markdown("""
    <div style="text-align:center;margin-top:64px;padding-top:24px;border-top:1px solid #1a2540;font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.15em;color:#1e293b;">
        COSMOSEER  /  KARDASHEV SCALE SIMULATOR  /  NVIDIA NIM
    </div>
    """, unsafe_allow_html=True)