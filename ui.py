import streamlit as st

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

:root {
    --bg-primary: #04060f;
    --bg-secondary: #080d1a;
    --bg-card: #0c1221;
    --bg-card-hover: #111827;
    --border: #1a2540;
    --border-accent: #1e3a5f;
    --cyan: #00d4ff;
    --cyan-dim: rgba(0, 212, 255, 0.12);
    --cyan-mid: rgba(0, 212, 255, 0.25);
    --violet: #7c3aed;
    --violet-dim: rgba(124, 58, 237, 0.12);
    --amber: #f59e0b;
    --amber-dim: rgba(245, 158, 11, 0.12);
    --text-primary: #e2e8f0;
    --text-secondary: #64748b;
    --text-muted: #334155;
    --green: #10b981;
    --red: #ef4444;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stSidebar"] {
    background-color: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Tabs */
[data-testid="stTabs"] [role="tablist"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 4px;
    gap: 4px;
}

[data-testid="stTabs"] [role="tab"] {
    color: var(--text-secondary) !important;
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    letter-spacing: 0.05em;
    border-radius: 6px;
    padding: 8px 16px;
    transition: all 0.2s;
}

[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: var(--cyan-dim) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border-accent) !important;
}

/* Sliders */
[data-testid="stSlider"] .stSlider > div > div > div {
    background: var(--cyan) !important;
}

[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: var(--cyan) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 10px var(--cyan) !important;
}

/* Buttons */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.15), rgba(124, 58, 237, 0.15)) !important;
    color: var(--cyan) !important;
    border: 1px solid var(--border-accent) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 13px !important;
    letter-spacing: 0.08em !important;
    padding: 12px 32px !important;
    border-radius: 6px !important;
    transition: all 0.25s !important;
    width: 100%;
}

[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, rgba(0, 212, 255, 0.25), rgba(124, 58, 237, 0.25)) !important;
    border-color: var(--cyan) !important;
    box-shadow: 0 0 20px rgba(0, 212, 255, 0.2) !important;
}

/* Number inputs */
[data-testid="stNumberInput"] input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-primary) !important;
    font-family: 'Space Mono', monospace !important;
}

/* Metric cards */
[data-testid="stMetric"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
}

[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 11px !important;
    font-family: 'Space Mono', monospace !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

[data-testid="stMetricValue"] {
    color: var(--cyan) !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 22px !important;
}

/* Progress bar */
[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--violet), var(--cyan)) !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
}

/* Spinner */
[data-testid="stSpinner"] {
    color: var(--cyan) !important;
}

/* Label text */
label, .stMarkdown p {
    color: var(--text-secondary) !important;
    font-size: 13px;
}

/* Hide default streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
"""


def inject_css():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div style="
        padding: 48px 0 32px;
        text-align: center;
        border-bottom: 1px solid #1a2540;
        margin-bottom: 40px;
    ">
        <div style="
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            letter-spacing: 0.3em;
            color: #00d4ff;
            text-transform: uppercase;
            margin-bottom: 16px;
        ">Kardashev Scale Simulator</div>
        <h1 style="
            font-family: 'Space Grotesk', sans-serif;
            font-size: 56px;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, #e2e8f0 30%, #00d4ff 70%, #7c3aed 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0 0 12px;
            line-height: 1;
        ">CosmoSeer</h1>
        <p style="
            color: #475569;
            font-size: 14px;
            letter-spacing: 0.02em;
            margin: 0;
        ">Quantify your civilization's position on the cosmic energy ladder</p>
    </div>
    """, unsafe_allow_html=True)


def render_k_gauge(k_score, tier_type, tier_desc):
    clamped = min(max(k_score, 0), 3.0)
    pct = (clamped / 3.0) * 100

    if k_score < 1.0:
        color = "#f59e0b"
        glow = "rgba(245, 158, 11, 0.3)"
    elif k_score < 2.0:
        color = "#00d4ff"
        glow = "rgba(0, 212, 255, 0.3)"
    elif k_score < 3.0:
        color = "#7c3aed"
        glow = "rgba(124, 58, 237, 0.3)"
    else:
        color = "#ef4444"
        glow = "rgba(239, 68, 68, 0.3)"

    st.markdown(f"""
    <div style="
        background: #0c1221;
        border: 1px solid #1a2540;
        border-radius: 12px;
        padding: 32px;
        text-align: center;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute;
            top: -40px; left: 50%;
            transform: translateX(-50%);
            width: 200px; height: 200px;
            background: radial-gradient(circle, {glow} 0%, transparent 70%);
            pointer-events: none;
        "></div>
        <div style="
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 0.25em;
            color: #475569;
            text-transform: uppercase;
            margin-bottom: 8px;
        ">Kardashev Index</div>
        <div style="
            font-family: 'Space Mono', monospace;
            font-size: 72px;
            font-weight: 700;
            color: {color};
            text-shadow: 0 0 30px {glow};
            line-height: 1;
            margin-bottom: 4px;
        ">{k_score:.3f}</div>
        <div style="
            font-family: 'Space Grotesk', sans-serif;
            font-size: 16px;
            font-weight: 600;
            color: {color};
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        ">{tier_type}</div>
        <div style="
            font-size: 12px;
            color: #475569;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 24px;
        ">{tier_desc}</div>
        <div style="
            background: #080d1a;
            border: 1px solid #1a2540;
            border-radius: 4px;
            height: 6px;
            overflow: hidden;
        ">
            <div style="
                width: {pct}%;
                height: 100%;
                background: linear-gradient(90deg, #f59e0b, {color});
                box-shadow: 0 0 12px {glow};
                transition: width 0.6s ease;
            "></div>
        </div>
        <div style="
            display: flex;
            justify-content: space-between;
            margin-top: 6px;
            font-family: 'Space Mono', monospace;
            font-size: 9px;
            color: #334155;
            letter-spacing: 0.1em;
        ">
            <span>TYPE 0</span><span>TYPE I</span><span>TYPE II</span><span>TYPE III</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_power_breakdown(type_1, type_2, type_3, total):
    tiers = [
        ("TYPE I", "Planetary", type_1, "#f59e0b", "rgba(245,158,11,0.12)"),
        ("TYPE II", "Stellar", type_2, "#00d4ff", "rgba(0,212,255,0.12)"),
        ("TYPE III", "Galactic", type_3, "#7c3aed", "rgba(124,58,237,0.12)"),
    ]

    cols = st.columns(3)
    for col, (tier, label, watts, color, bg) in zip(cols, tiers):
        with col:
            st.markdown(f"""
            <div style="
                background: {bg};
                border: 1px solid {color}30;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
            ">
                <div style="
                    font-family: 'Space Mono', monospace;
                    font-size: 9px;
                    letter-spacing: 0.2em;
                    color: {color};
                    margin-bottom: 8px;
                ">{tier}</div>
                <div style="
                    font-size: 11px;
                    color: #475569;
                    margin-bottom: 12px;
                ">{label}</div>
                <div style="
                    font-family: 'Space Mono', monospace;
                    font-size: 16px;
                    font-weight: 700;
                    color: {color};
                ">{watts:.2e}</div>
                <div style="font-size: 10px; color: #334155; margin-top: 2px;">Watts</div>
            </div>
            """, unsafe_allow_html=True)


def render_advisor_panel(response_text):
    st.markdown(f"""
    <div style="
        background: #0c1221;
        border: 1px solid #1e3a5f;
        border-left: 3px solid #00d4ff;
        border-radius: 8px;
        padding: 24px 28px;
        margin-top: 24px;
    ">
        <div style="
            font-family: 'Space Mono', monospace;
            font-size: 10px;
            letter-spacing: 0.2em;
            color: #00d4ff;
            text-transform: uppercase;
            margin-bottom: 14px;
        ">CosmoSeer Advisory Report</div>
        <p style="
            font-size: 14px;
            color: #94a3b8;
            line-height: 1.7;
            margin: 0;
            font-family: 'Space Grotesk', sans-serif;
        ">{response_text}</p>
    </div>
    """, unsafe_allow_html=True)


def render_input_label(text):
    st.markdown(f"""
    <div style="
        font-family: 'Space Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.15em;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 4px;
        margin-top: 16px;
    ">{text}</div>
    """, unsafe_allow_html=True)