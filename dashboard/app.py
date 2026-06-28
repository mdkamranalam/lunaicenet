import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="LunaIceNet",
    page_icon="🌙",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1,h2,h3{
    font-weight:700;
}

[data-testid="metric-container"]{
    background:#111827;
    border:1px solid #374151;
    padding:20px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# LOAD DATA
# =====================================================

hazard = np.load("data/dem/hazard.npy")
sites = pd.read_csv("data/mission_report.csv")
ellipse = pd.read_csv("data/landing_ellipses.csv")

display = hazard[::20, ::20]

# =====================================================
# HEADER
# =====================================================

st.title("🌙 LunaIceNet")

st.markdown("""
# AI-Powered Lunar South Pole Landing Site Selection

Autonomous terrain assessment,
hazard analysis,
ice detection,
landing ellipse validation,
and mission ranking for future lunar missions.
""")

st.divider()

# =====================================================
# EXECUTIVE SUMMARY
# =====================================================

best = sites.iloc[0]

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Best Landing Site",
        int(best.site_id)
    )

with c2:
    st.metric(
        "Mission Score",
        f"{best.mission_score:.3f}"
    )

with c3:
    st.metric(
        "Confidence",
        f"{best.ellipse_confidence:.3f}"
    )

with c4:
    st.metric(
        "Hazard",
        f"{best.hazard:.4f}"
    )

# =====================================================
# MISSION DECISION
# =====================================================

st.success("""
🚀 MISSION DECISION

PRIMARY LANDING TARGET APPROVED

STATUS: GO FOR LANDING
""")

st.divider()

# =====================================================
# HAZARD MAP
# =====================================================

st.header("🛰 Lunar Hazard Map")

fig = px.imshow(
    display,
    color_continuous_scale="Inferno",
    aspect="auto"
)

# only show top 10 labels
for _, row in sites.head(10).iterrows():

    fig.add_trace(
        go.Scatter(
            x=[row.x/20],
            y=[row.y/20],

            mode="markers+text",

            text=[
                str(int(row.site_id))
            ],

            textposition="top center",

            marker=dict(
                size=10,
                color="cyan",
                symbol="x"
            ),

            showlegend=False
        )
    )

fig.update_layout(
    title="Top Ranked Lunar Landing Sites",

    height=700,

    paper_bgcolor="#030712",
    plot_bgcolor="#030712",

    font=dict(
        color="white",
        size=14
    ),

    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    ),

    xaxis_title="Longitude",
    yaxis_title="Latitude"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# TOP SITES
# =====================================================

st.header("🏆 Top Landing Sites")

table = sites[
    [
        "site_id",
        "mission_score",
        "ellipse_confidence",
        "hazard",
        "ice",
        "recommendation"
    ]
].copy()

table.columns = [
    "Site",
    "Score",
    "Confidence",
    "Hazard",
    "Ice",
    "Status"
]

st.dataframe(
    table.head(20),
    use_container_width=True,
    hide_index=True
)

# =====================================================
# SITE ANALYSIS
# =====================================================

st.header("🎯 Site Analysis")

selected = st.selectbox(
    "Select Site",
    sites.site_id.astype(int)
)

site = sites[
    sites.site_id == selected
].iloc[0]

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Mission Score",
        f"{site.mission_score:.3f}"
    )

    st.metric(
        "Hazard",
        f"{site.hazard:.4f}"
    )

with c2:

    st.metric(
        "Ellipse Confidence",
        f"{site.ellipse_confidence:.3f}"
    )

    st.metric(
        "Safe",
        str(site.safe)
    )

with c3:

    st.metric(
        "Ice",
        site.ice
    )

    st.metric(
        "Recommendation",
        site.recommendation
    )

# =====================================================
# AI MISSION ASSESSMENT
# =====================================================

st.divider()

st.header("🤖 AI Mission Assessment")

messages = []

if site.hazard < 0.01:
    messages.append(
        "✓ Extremely low terrain hazard"
    )

if site.safe:
    messages.append(
        "✓ Safe landing region confirmed"
    )

if site.ice == "High":
    messages.append(
        "✓ High confidence ice deposit"
    )

if site.ice == "Medium":
    messages.append(
        "✓ Medium confidence ice deposit"
    )

if site.ellipse_confidence > 0.99:
    messages.append(
        "✓ Landing ellipse confidence >99%"
    )

if site.recommendation == "EXCELLENT":
    messages.append(
        "🚀 PRIMARY LANDING TARGET"
    )

for m in messages:
    st.success(m)

# =====================================================
# LANDING ELLIPSE
# =====================================================

st.divider()

st.header("🛰 Landing Ellipse")

theta = np.linspace(
    0,
    2*np.pi,
    200
)

fig2 = go.Figure()

fig2.add_trace(
    go.Scatter(
        x=[0],
        y=[0],

        mode="markers",

        marker=dict(
            size=18,
            color="cyan"
        )
    )
)

fig2.add_trace(
    go.Scatter(
        x=50*np.cos(theta),
        y=25*np.sin(theta),

        mode="lines",

        line=dict(
            width=3
        )
    )
)

fig2.update_layout(

    title="Landing Ellipse",

    xaxis_title="Cross-range (meters)",

    yaxis_title="Down-range (meters)",

    height=500,

    paper_bgcolor="#030712",

    plot_bgcolor="#030712",

    font=dict(
        color="white"
    ),

    showlegend=False
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# =====================================================
# PIPELINE
# =====================================================

st.divider()

st.header("⚙ AI Processing Pipeline")

st.code("""
DEM
 ↓
Slope Analysis
 ↓
Surface Roughness
 ↓
Hazard Mapping
 ↓
Safe Zone Extraction
 ↓
Ice Detection
 ↓
Landing Score
 ↓
Candidate Selection
 ↓
Mission Ranking
 ↓
Landing Ellipse Validation
 ↓
Mission Recommendation
""")

# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "LunaIceNet • AI-Powered Lunar South Pole Landing Site Selection • Hackathon 2026"
)