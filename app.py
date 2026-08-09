import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "Scripts"))

import streamlit as st
from logic import calculate_kardashev, get_tier_label
from ui import (
    inject_css, render_header, render_k_gauge,
    render_power_breakdown, render_advisor_panel, render_input_label
)
from ai import generate_advisor_response

st.set_page_config(
    page_title="CosmoSeer",
    page_icon="assets/favicon.ico" if os.path.exists("assets/favicon.ico") else None,
    layout="wide",
    initial_sidebar_state="collapsed"
)

inject_css()
render_header()

left, right = st.columns([1.1, 1], gap="large")

with left:
    st.markdown("""
    <div style="
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.2em;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #1a2540;
    ">Energy Infrastructure Configuration</div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["TYPE I  /  Planetary", "TYPE II  /  Stellar", "TYPE III  /  Galactic"])

    with tab1:
        render_input_label("Solar Panel Coverage (%)")
        solar = st.slider("solar", 0, 100, 10, label_visibility="collapsed")

        render_input_label("Fusion Reactor Plants")
        fusion = st.number_input("fusion", min_value=0, max_value=10000, value=100, step=10, label_visibility="collapsed")

        render_input_label("AI Optimization Boost (%)")
        ai_boost = st.slider("ai_boost", 0, 100, 5, label_visibility="collapsed")

    with tab2:
        render_input_label("Dyson Swarm Coverage (%)")
        dyson = st.slider("dyson", 0, 100, 0, label_visibility="collapsed")

        render_input_label("Stellar Harvesters")
        harvesters = st.number_input("harvesters", min_value=0, max_value=1000, value=0, step=1, label_visibility="collapsed")

    with tab3:
        render_input_label("Colonized Star Systems")
        stars = st.number_input("stars", min_value=0, max_value=100000, value=0, step=100, label_visibility="collapsed")

        render_input_label("Black Hole Extraction (%)")
        blackholes = st.slider("blackholes", 0, 100, 0, label_visibility="collapsed")

    st.markdown("<div style='margin-top: 28px;'></div>", unsafe_allow_html=True)
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
    <div style="
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.2em;
        color: #475569;
        text-transform: uppercase;
        margin: 24px 0 12px;
    ">Power Breakdown by Tier</div>
    """, unsafe_allow_html=True)

    render_power_breakdown(type_1, type_2, type_3, total_watts)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Total Output", f"{total_watts:.2e} W")
    with col_b:
        st.metric("Kardashev Index", f"{k_score:.4f}")

    if run_advisor:
        with st.spinner("Consulting CosmoSeer..."):
            tier_label = f"{tier_type} ({tier_desc})"
            response = generate_advisor_response(
                solar, fusion, ai_boost,
                dyson, harvesters,
                stars, blackholes,
                k_score, total_watts, tier_label
            )
        st.session_state["advisor_response"] = response
        st.write(response) #debug

    if "advisor_response" in st.session_state:
        render_advisor_panel(st.session_state["advisor_response"])

st.markdown("""
<div style="
    text-align: center;
    margin-top: 64px;
    padding-top: 24px;
    border-top: 1px solid #1a2540;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 0.15em;
    color: #1e293b;
">
    COSMOSEER  /  KARDASHEV SCALE SIMULATOR  /  NVIDIA NIM
</div>
""", unsafe_allow_html=True)