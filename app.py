"""
NEXUS AI — Enterprise Intelligence Platform
Frontend foundation (Phase 2).

Run:
    streamlit run app.py

This is the UI foundation. Backend, OpenAI, PostgreSQL, Qdrant and agent
integrations will be connected in later development phases.
"""

from __future__ import annotations

import io
import json
import random
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ---------------------------------------------------------------------
# App configuration
# ---------------------------------------------------------------------
st.set_page_config(
    page_title="NEXUS AI | Enterprise Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------------------
# Theme and reusable styling
# ---------------------------------------------------------------------
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #080b14;
    --panel: #101625;
    --panel2: #131d30;
    --line: rgba(148,163,184,.15);
    --muted: #91a0b8;
    --text: #edf3ff;
    --cyan: #52d6e8;
    --violet: #9b8cff;
    --green: #48d6a0;
}
html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}
.stApp {
    background:
      radial-gradient(ellipse at 10% 0%, rgba(73,91,180,.16), transparent 35%),
      radial-gradient(ellipse at 90% 8%, rgba(40,185,205,.10), transparent 30%),
      var(--bg);
    color: var(--text);
}
[data-testid="stHeader"] { background: rgba(8,11,20,.75); }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1423 0%, #0a101c 100%);
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div { padding-top: 1.3rem; }
.block-container { padding-top: 1.8rem; padding-bottom: 3rem; max-width: 1500px; }
h1, h2, h3 { color: var(--text) !important; letter-spacing: -.035em; }
p, label, .stMarkdown { color: #c5d0e2; }
.smallcaps {
    color: var(--cyan); font-family: 'DM Mono', monospace;
    font-size: .69rem; letter-spacing: .16em; text-transform: uppercase;
}
.brand {
    font-size: 1.45rem; font-weight: 800; letter-spacing: -.06em;
    color: #f4f7ff; margin: 0;
}
.brand span { color: var(--cyan); }
.brand-sub {
    color: #8392aa; font-family: 'DM Mono', monospace;
    font-size: .61rem; letter-spacing: .17em; margin-top: .2rem;
}
.hero {
    padding: 1.7rem 1.8rem; border: 1px solid var(--line);
    border-radius: 22px;
    background: linear-gradient(115deg, rgba(23,36,61,.96), rgba(16,22,37,.92) 58%, rgba(27,34,64,.88));
    box-shadow: 0 18px 55px rgba(0,0,0,.22);
    margin-bottom: 1.15rem;
}
.hero h1 { font-size: clamp(2rem, 4vw, 3.25rem); margin: .35rem 0 .55rem; }
.hero p { color: #aebbd0; max-width: 760px; margin-bottom: 0; line-height: 1.7; }
.panel {
    border: 1px solid var(--line); border-radius: 17px;
    background: linear-gradient(145deg, rgba(19,29,48,.96), rgba(13,20,34,.96));
    padding: 1.1rem 1.2rem; min-height: 118px;
}
.metric-label {
    color: #92a2ba; font-size: .72rem; text-transform: uppercase;
    letter-spacing: .12em; font-family: 'DM Mono', monospace;
}
.metric-value { color: #f3f7ff; font-size: 1.9rem; font-weight: 800; margin-top: .35rem; }
.metric-foot { color: #7f90a9; font-size: .76rem; margin-top: .25rem; }
.section-title { font-size: 1.12rem; font-weight: 800; margin: .2rem 0 .2rem; }
.section-sub { color: #8797b0; font-size: .83rem; margin-bottom: .9rem; }
.pill {
    display: inline-block; border: 1px solid rgba(72,214,160,.28);
    background: rgba(72,214,160,.08); color: #70e5b6;
    padding: .28rem .6rem; border-radius: 99px; font-size: .68rem;
    font-family: 'DM Mono', monospace; letter-spacing: .08em;
}
.info-box {
    border: 1px solid rgba(82,214,232,.2); background: rgba(82,214,232,.06);
    border-radius: 13px; padding: .9rem 1rem; color: #b8dce5;
    font-size: .86rem; line-height: 1.6;
}
div.stButton > button, div.stDownloadButton > button {
    border-radius: 10px; border: 1px solid rgba(82,214,232,.35);
    background: linear-gradient(110deg, rgba(82,214,232,.16), rgba(155,140,255,.17));
    color: #effaff; font-weight: 700; min-height: 2.55rem;
}
div.stButton > button:hover, div.stDownloadButton > button:hover {
    border-color: var(--cyan); color: white;
}
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"],
.stNumberInput input, .stDateInput input {
    background: #0c1422 !important; color: #eaf1ff !important;
    border-color: var(--line) !important; border-radius: 10px !important;
}
[data-testid="stFileUploader"] {
    border: 1px dashed rgba(82,214,232,.35);
    border-radius: 14px; background: rgba(82,214,232,.035);
}
hr { border-color: var(--line); }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Session state and sample data
# ---------------------------------------------------------------------
PAGES = [
    "Overview",
    "Knowledge Library",
    "AI Workspace",
    "Agent Studio",
    "Data Intelligence",
    "Predictive Analytics",
    "Research Center",
    "Knowledge Graph",
    "Reports",
    "Settings",
]

if "page" not in st.session_state:
    st.session_state.page = "Overview"
if "chat" not in st.session_state:
    st.session_state.chat = [
        {
            "role": "assistant",
            "content": (
                "Welcome to NEXUS AI. I am the workspace interface. "
                "Connect the AI service in a later integration phase to enable live answers."
            ),
        }
    ]
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None
if "activities" not in st.session_state:
    st.session_state.activities = [
        ("Workspace initialized", "System", datetime.now()),
        ("Demo analytics loaded", "Analytics", datetime.now() - timedelta(minutes=4)),
        ("Agent workspace prepared", "Agents", datetime.now() - timedelta(minutes=9)),
    ]


def add_activity(message: str, category: str = "Workspace") -> None:
    st.session_state.activities.insert(0, (message, category, datetime.now()))
    st.session_state.activities = st.session_state.activities[:12]


def metric_card(label: str, value: str, foot: str, icon: str = "✦") -> None:
    st.markdown(
        f"""
        <div class="panel">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <div class="metric-label">{label}</div>
            <div style="color:#52d6e8;font-size:1.1rem">{icon}</div>
          </div>
          <div class="metric-value">{value}</div>
          <div class="metric-foot">{foot}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title: str, subtitle: str = "") -> None:
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="section-sub">{subtitle}</div>', unsafe_allow_html=True)


def demo_sales_data() -> pd.DataFrame:
    random.seed(21)
    start = date.today() - timedelta(days=179)
    rows = []
    countries = ["India", "United States", "United Kingdom", "Germany", "Singapore"]
    categories = ["Materials", "Equipment", "Safety", "Tools"]
    for i in range(180):
        d = start + timedelta(days=i)
        revenue = random.randint(18000, 85000)
        cost = int(revenue * random.uniform(.48, .79))
        rows.append(
            {
                "date": d,
                "country": random.choice(countries),
                "category": random.choice(categories),
                "revenue": revenue,
                "profit": revenue - cost,
                "orders": random.randint(12, 95),
            }
        )
    return pd.DataFrame(rows)


def read_uploaded_table(uploaded_file: Any) -> pd.DataFrame | None:
    if uploaded_file is None:
        return None
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            return pd.read_csv(uploaded_file)
        if uploaded_file.name.lower().endswith((".xlsx", ".xls")):
            return pd.read_excel(uploaded_file)
        st.error("Please upload a CSV or Excel file.")
    except Exception as exc:
        st.error(f"Could not read the file: {exc}")
    return None


# ---------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="padding:.2rem .35rem 1.35rem">
          <div class="brand">✦ NEXUS<span>AI</span></div>
          <div class="brand-sub">ENTERPRISE INTELLIGENCE PLATFORM</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="smallcaps">Workspace navigation</div>', unsafe_allow_html=True)
    selected_page = st.radio(
        "Navigation",
        PAGES,
        index=PAGES.index(st.session_state.page),
        label_visibility="collapsed",
        format_func=lambda x: {
            "Overview": "◈  Overview",
            "Knowledge Library": "▤  Knowledge Library",
            "AI Workspace": "✧  AI Workspace",
            "Agent Studio": "⌘  Agent Studio",
            "Data Intelligence": "▥  Data Intelligence",
            "Predictive Analytics": "⌁  Predictive Analytics",
            "Research Center": "◎  Research Center",
            "Knowledge Graph": "◇  Knowledge Graph",
            "Reports": "▧  Reports",
            "Settings": "⚙  Settings",
        }.get(x, x),
        key="sidebar_page",
    )
    st.session_state.page = selected_page
    st.markdown("---")
    st.markdown('<div class="smallcaps">Platform status</div>', unsafe_allow_html=True)
    st.markdown(
        '<div style="display:flex;align-items:center;gap:.5rem;margin:.65rem 0">'
        '<span style="height:8px;width:8px;border-radius:50%;background:#eabf64;display:inline-block"></span>'
        '<span style="font-size:.82rem;color:#c3cfe0">Frontend operational</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("AI services: not connected yet")
    st.markdown("---")
    st.caption("NEXUS AI · Foundation build")
    st.caption("Local development workspace")


# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------
st.markdown(
    f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:1rem">
      <div>
        <div class="smallcaps">NEXUS AI / ENTERPRISE WORKSPACE</div>
        <div style="font-size:.82rem;color:#8797b0;margin-top:.25rem">{st.session_state.page}</div>
      </div>
      <div class="pill">● FRONTEND ONLINE</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------
# Page: Overview
# ---------------------------------------------------------------------
if st.session_state.page == "Overview":
    st.markdown(
        """
        <div class="hero">
          <div class="smallcaps">Your unified intelligence environment</div>
          <h1>Turn information into<br><span style="color:#52d6e8">actionable intelligence.</span></h1>
          <p>
            A modular workspace for document intelligence, AI agents, business analytics
            and predictive insights. Your enterprise knowledge can live in one connected platform.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    docs_count = len(st.session_state.uploaded_docs)
    data_ready = st.session_state.uploaded_data is not None
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Documents added", str(docs_count), "Files in this session", "▤")
    with c2:
        metric_card("Datasets loaded", "1" if data_ready else "0", "CSV / Excel workspace", "▥")
    with c3:
        metric_card("AI queries", str(max(0, len(st.session_state.chat) - 1)), "Workspace messages", "✧")
    with c4:
        metric_card("Agents available", "8", "Workflow templates · demo", "⌘")

    st.write("")
    left, right = st.columns([1.55, 1])
    with left:
        section_heading("Intelligence activity", "Illustrative six-month business activity.")
        df = demo_sales_data()
        monthly = df.assign(month=pd.to_datetime(df["date"]).dt.to_period("M").astype(str))
        monthly = monthly.groupby("month", as_index=False)[["revenue", "profit"]].sum()
        fig = px.area(monthly, x="month", y=["revenue", "profit"], template="plotly_dark")
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=5, r=5, t=15, b=5), height=300,
            legend_title_text="", xaxis_title="", yaxis_title="Amount",
        )
        fig.update_traces(line=dict(width=2))
        st.plotly_chart(fig, use_container_width=True)
    with right:
        section_heading("Platform modules", "Your intelligence capabilities at a glance.")
        modules = [
            ("Knowledge intelligence", "Document ingestion and retrieval", "READY FOR INTEGRATION"),
            ("Agent workforce", "Specialist agent orchestration", "READY FOR INTEGRATION"),
            ("Business analytics", "Structured data exploration", "DEMO ENABLED"),
            ("Predictive intelligence", "Forecasting and trend analysis", "PLANNED"),
        ]
        for name, desc, status in modules:
            st.markdown(
                f"""
                <div class="panel" style="min-height:0;margin-bottom:.55rem;padding:.8rem 1rem">
                  <div style="display:flex;justify-content:space-between;gap:.5rem">
                    <b style="font-size:.87rem;color:#edf3ff">{name}</b>
                    <span style="font-size:.59rem;color:#52d6e8;font-family:'DM Mono'">{status}</span>
                  </div>
                  <div style="font-size:.75rem;color:#8797b0;margin-top:.3rem">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    section_heading("Recent activity", "Actions performed in this local session.")
    if st.session_state.activities:
        for message, category, timestamp in st.session_state.activities[:6]:
            st.markdown(
                f'<div style="padding:.65rem 0;border-bottom:1px solid rgba(148,163,184,.1)">'
                f'<b style="color:#dce7f7;font-size:.84rem">{message}</b>'
                f'<span style="color:#7789a3;font-size:.75rem"> · {category} · {timestamp.strftime("%H:%M:%S")}</span></div>',
                unsafe_allow_html=True,
            )


# ---------------------------------------------------------------------
# Page: Knowledge Library
# ---------------------------------------------------------------------
elif st.session_state.page == "Knowledge Library":
    st.markdown('<div class="smallcaps">01 / KNOWLEDGE INGESTION</div>', unsafe_allow_html=True)
    st.title("Knowledge Library")
    st.write("Add source files to prepare your enterprise knowledge base.")
    st.markdown(
        '<div class="info-box">Current foundation: files are tracked in this browser session only. '
        'Document extraction, chunking, embeddings and Qdrant indexing will be connected in the RAG phase.</div>',
        unsafe_allow_html=True,
    )
    uploaded = st.file_uploader(
        "Upload knowledge files",
        type=["pdf", "docx", "txt", "md", "csv"],
        accept_multiple_files=True,
        help="Supported foundation formats: PDF, DOCX, TXT, Markdown and CSV.",
    )
    if uploaded:
        existing = {item["name"] for item in st.session_state.uploaded_docs}
        for file in uploaded:
            if file.name not in existing:
                st.session_state.uploaded_docs.append(
                    {"name": file.name, "size": file.size, "type": file.type or "Unknown"}
                )
                add_activity(f"Added {file.name}", "Knowledge Library")
        st.success(f"{len(uploaded)} file(s) selected. Files are recorded for this session.")
    section_heading("Knowledge sources", "Files selected during this session.")
    if st.session_state.uploaded_docs:
        st.dataframe(pd.DataFrame(st.session_state.uploaded_docs), use_container_width=True, hide_index=True)
        if st.button("Clear session file list"):
            st.session_state.uploaded_docs = []
            add_activity("Cleared session file list", "Knowledge Library")
            st.rerun()
    else:
        st.info("No files added yet. Upload a document to begin.")


# ---------------------------------------------------------------------
# Page: AI Workspace
# ---------------------------------------------------------------------
elif st.session_state.page == "AI Workspace":
    st.markdown('<div class="smallcaps">02 / CONVERSATIONAL INTELLIGENCE</div>', unsafe_allow_html=True)
    st.title("AI Workspace")
    st.write("A unified conversation surface for your documents, datasets and AI tools.")
    st.markdown(
        '<div class="info-box">The chat interface is ready. Live model responses and RAG-grounded answers '
        'will be enabled after we connect the secured OpenAI and retrieval services.</div>',
        unsafe_allow_html=True,
    )
    for message in st.session_state.chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("Ask a question or describe a task...")
    if prompt:
        st.session_state.chat.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        response = (
            "Your request has been captured in the NEXUS AI workspace. "
            "Live AI generation is not connected in this foundation build. "
            "In the next integration phase, this message will be routed through the backend "
            "to the selected OpenAI model and, when appropriate, the RAG retrieval pipeline."
        )
        st.session_state.chat.append({"role": "assistant", "content": response})
        add_activity("Submitted a workspace query", "AI Workspace")
        with st.chat_message("assistant"):
            st.markdown(response)


# ---------------------------------------------------------------------
# Page: Agent Studio
# ---------------------------------------------------------------------
elif st.session_state.page == "Agent Studio":
    st.markdown('<div class="smallcaps">03 / ORCHESTRATED AI WORKFORCE</div>', unsafe_allow_html=True)
    st.title("Agent Studio")
    st.write("Specialist agents designed to collaborate on multi-step tasks.")
    agents = [
        ("Supervisor Agent", "Plans tasks and routes work to specialists.", "Coordinator"),
        ("Research Agent", "Collects and synthesizes research context.", "Research"),
        ("Document Agent", "Extracts and reasons over document content.", "Knowledge"),
        ("Data Analyst Agent", "Profiles datasets and calculates metrics.", "Analytics"),
        ("Financial Agent", "Examines revenue, cost and profitability.", "Finance"),
        ("Prediction Agent", "Builds forecasting workflows.", "Forecasting"),
        ("SQL Agent", "Creates constrained, read-only data queries.", "Data access"),
        ("Report Agent", "Produces structured summaries and reports.", "Reporting"),
    ]
    cols = st.columns(2)
    for i, (name, desc, tag) in enumerate(agents):
        with cols[i % 2]:
            st.markdown(
                f"""
                <div class="panel" style="margin-bottom:.8rem;min-height:125px">
                  <div class="smallcaps">{tag}</div>
                  <div style="font-size:1rem;font-weight:800;color:#eef4ff;margin:.35rem 0">{name}</div>
                  <div style="font-size:.8rem;color:#91a0b8">{desc}</div>
                  <div style="font-size:.63rem;color:#e8bd72;margin-top:.65rem;font-family:'DM Mono'">● TEMPLATE · NOT CONNECTED</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    section_heading("Task planner", "Preview the task you want the future supervisor agent to coordinate.")
    task = st.text_area("Describe your objective", placeholder="Example: Analyze the sales dataset and prepare a regional performance report.")
    if st.button("Prepare agent workflow", disabled=not bool(task.strip())):
        st.session_state["planned_task"] = task.strip()
        add_activity("Prepared an agent workflow request", "Agent Studio")
    if st.session_state.get("planned_task"):
        st.success("Task captured. Agent execution will be connected in the LangGraph phase.")
        st.code(st.session_state["planned_task"])


# ---------------------------------------------------------------------
# Page: Data Intelligence
# ---------------------------------------------------------------------
elif st.session_state.page == "Data Intelligence":
    st.markdown('<div class="smallcaps">04 / STRUCTURED DATA INTELLIGENCE</div>', unsafe_allow_html=True)
    st.title("Data Intelligence")
    st.write("Upload a CSV or Excel file to explore its structure and generate quick descriptive insights.")
    data_file = st.file_uploader("Upload dataset", type=["csv", "xlsx", "xls"], key="data_upload")
    if data_file:
        frame = read_uploaded_table(data_file)
        if frame is not None:
            st.session_state.uploaded_data = frame
            st.session_state.uploaded_data_name = data_file.name
            add_activity(f"Loaded dataset {data_file.name}", "Data Intelligence")
    frame = st.session_state.uploaded_data
    if frame is not None:
        st.markdown(f'<span class="pill">DATASET · {st.session_state.get("uploaded_data_name", "Uploaded file")}</span>', unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a:
            metric_card("Rows", f"{len(frame):,}", "Records loaded", "▤")
        with b:
            metric_card("Columns", str(len(frame.columns)), "Fields detected", "▥")
        with c:
            numeric_count = len(frame.select_dtypes(include="number").columns)
            metric_card("Numeric fields", str(numeric_count), "Available for analysis", "∑")
        section_heading("Dataset preview", "First 100 records.")
        st.dataframe(frame.head(100), use_container_width=True)
        section_heading("Column profile", "Data types and missing-value counts.")
        profile = pd.DataFrame({
            "column": frame.columns,
            "data_type": [str(frame[col].dtype) for col in frame.columns],
            "missing_values": [int(frame[col].isna().sum()) for col in frame.columns],
            "unique_values": [int(frame[col].nunique(dropna=True)) for col in frame.columns],
        })
        st.dataframe(profile, use_container_width=True, hide_index=True)
        numeric = frame.select_dtypes(include="number")
        if not numeric.empty:
            section_heading("Explore numeric fields", "Choose a field to visualize its distribution.")
            chosen = st.selectbox("Numeric field", numeric.columns.tolist())
            chart = px.histogram(frame, x=chosen, nbins=30, template="plotly_dark")
            chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=330)
            st.plotly_chart(chart, use_container_width=True)
            st.markdown("**Descriptive statistics**")
            st.dataframe(numeric.describe().T, use_container_width=True)
        csv_bytes = frame.to_csv(index=False).encode("utf-8")
        st.download_button("Download loaded dataset as CSV", csv_bytes, "nexus_dataset_export.csv", "text/csv")
    else:
        st.info("Upload a CSV or Excel file to activate dataset profiling.")


# ---------------------------------------------------------------------
# Page: Predictive Analytics
# ---------------------------------------------------------------------
elif st.session_state.page == "Predictive Analytics":
    st.markdown('<div class="smallcaps">05 / FORECASTING WORKSPACE</div>', unsafe_allow_html=True)
    st.title("Predictive Analytics")
    st.write("Explore a sample time series and preview a simple baseline forecast.")
    st.markdown(
        '<div class="info-box">This page currently uses illustrative sample data and a simple baseline. '
        'A validated forecasting pipeline, model selection and backtesting will be implemented later.</div>',
        unsafe_allow_html=True,
    )
    sample = demo_sales_data()
    daily = sample.groupby("date", as_index=False)["revenue"].sum()
    daily["date"] = pd.to_datetime(daily["date"])
    horizon = st.slider("Forecast horizon (days)", 7, 30, 14)
    baseline = float(daily["revenue"].tail(30).mean())
    future_dates = pd.date_range(daily["date"].max() + pd.Timedelta(days=1), periods=horizon)
    forecast = pd.DataFrame({"date": future_dates, "revenue": [baseline] * horizon, "series": ["Baseline forecast"] * horizon})
    history = daily.copy()
    history["series"] = "Historical"
    combined = pd.concat([history, forecast], ignore_index=True)
    fig = px.line(combined, x="date", y="revenue", color="series", template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=390)
    st.plotly_chart(fig, use_container_width=True)
    st.metric("Baseline daily revenue", f"{baseline:,.0f}")
    st.caption("Illustrative estimate only — not a business forecast.")


# ---------------------------------------------------------------------
# Page: Research Center
# ---------------------------------------------------------------------
elif st.session_state.page == "Research Center":
    st.markdown('<div class="smallcaps">06 / RESEARCH AND SYNTHESIS</div>', unsafe_allow_html=True)
    st.title("Research Center")
    st.write("Prepare a structured research brief for a topic.")
    topic = st.text_input("Research topic", placeholder="Example: Enterprise RAG architecture and evaluation")
    objective = st.text_area("Research objective", placeholder="What should the research establish?")
    depth = st.selectbox("Desired depth", ["Executive brief", "Technical overview", "Comprehensive research plan"])
    if st.button("Create research brief outline", disabled=not bool(topic.strip())):
        brief = {
            "topic": topic.strip(),
            "objective": objective.strip() or "Explore the topic and identify practical findings.",
            "depth": depth,
            "sections": [
                "Executive summary",
                "Background and key concepts",
                "Evidence and supporting sources",
                "Technical or business implications",
                "Risks, limitations and open questions",
                "Recommendations and next steps",
            ],
        }
        st.session_state["research_brief"] = brief
        add_activity("Created a research brief outline", "Research Center")
    if st.session_state.get("research_brief"):
        st.subheader("Research brief outline")
        st.json(st.session_state["research_brief"])
        st.download_button(
            "Download outline",
            json.dumps(st.session_state["research_brief"], indent=2).encode("utf-8"),
            "nexus_research_outline.json",
            "application/json",
        )


# ---------------------------------------------------------------------
# Page: Knowledge Graph
# ---------------------------------------------------------------------
elif st.session_state.page == "Knowledge Graph":
    st.markdown('<div class="smallcaps">07 / CONNECTED KNOWLEDGE</div>', unsafe_allow_html=True)
    st.title("Knowledge Graph")
    st.write("Preview how entities and relationships can be represented.")
    nodes = [
        ("NEXUS AI", "Platform"), ("Documents", "Source"), ("Datasets", "Source"),
        ("RAG", "Capability"), ("AI Agents", "Capability"), ("Reports", "Output"),
        ("Analytics", "Capability"),
    ]
    edges = [
        ("NEXUS AI", "Documents"), ("NEXUS AI", "Datasets"),
        ("Documents", "RAG"), ("RAG", "AI Agents"),
        ("Datasets", "Analytics"), ("AI Agents", "Reports"),
        ("Analytics", "Reports"),
    ]
    positions = {
        "NEXUS AI": (0, 0), "Documents": (-1.2, 1), "Datasets": (1.2, 1),
        "RAG": (-1.2, 0), "AI Agents": (0, -1), "Reports": (1.2, -1),
        "Analytics": (1.2, 0),
    }
    edge_x, edge_y = [], []
    for source, target in edges:
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode="lines", line=dict(width=1.5, color="#526782"), hoverinfo="none"))
    fig.add_trace(go.Scatter(
        x=[positions[n][0] for n, _ in nodes],
        y=[positions[n][1] for n, _ in nodes],
        text=[n for n, _ in nodes],
        mode="markers+text",
        textposition="bottom center",
        marker=dict(size=28, color=["#52d6e8", "#9b8cff", "#9b8cff", "#48d6a0", "#48d6a0", "#e8bd72", "#48d6a0"], line=dict(width=1, color="#dceaff")),
        hovertext=[f"{n} · {t}" for n, t in nodes],
        hoverinfo="text",
    ))
    fig.update_layout(
        template="plotly_dark", showlegend=False, height=480,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False), yaxis=dict(visible=False),
        margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Illustrative platform graph. Entity extraction and graph persistence will be added in a later phase.")


# ---------------------------------------------------------------------
# Page: Reports
# ---------------------------------------------------------------------
elif st.session_state.page == "Reports":
    st.markdown('<div class="smallcaps">08 / BUSINESS OUTPUTS</div>', unsafe_allow_html=True)
    st.title("Reports")
    st.write("Create a downloadable workspace activity snapshot.")
    report = {
        "platform": "NEXUS AI",
        "report_type": "Local workspace snapshot",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "documents_added_this_session": len(st.session_state.uploaded_docs),
        "chat_messages_this_session": len(st.session_state.chat),
        "dataset_loaded": st.session_state.uploaded_data is not None,
        "recent_activity": [
            {"message": m, "category": c, "timestamp": t.isoformat(timespec="seconds")}
            for m, c, t in st.session_state.activities[:10]
        ],
        "note": "This is a local UI snapshot, not an AI-generated enterprise report.",
    }
    st.markdown('<div class="info-box">This foundation version exports workspace metadata. '
                'PDF and Excel report generation will be added after analytics and backend integration.</div>',
                unsafe_allow_html=True)
    st.json(report)
    st.download_button(
        "Download workspace report (JSON)",
        json.dumps(report, indent=2).encode("utf-8"),
        f"nexus_workspace_report_{date.today().isoformat()}.json",
        "application/json",
    )


# ---------------------------------------------------------------------
# Page: Settings
# ---------------------------------------------------------------------
elif st.session_state.page == "Settings":
    st.markdown('<div class="smallcaps">09 / PLATFORM CONFIGURATION</div>', unsafe_allow_html=True)
    st.title("Settings")
    st.write("Review the current local frontend configuration.")
    st.subheader("Workspace")
    st.text_input("Application name", value="NEXUS AI", disabled=True)
    st.text_input("Application version", value="0.1.0 · Foundation", disabled=True)
    st.text_input("Frontend framework", value="Streamlit", disabled=True)
    st.subheader("Integration readiness")
    for label, status in [
        ("OpenAI API", "Not connected"),
        ("FastAPI backend", "Not connected"),
        ("PostgreSQL", "Not connected"),
        ("Qdrant vector database", "Not connected"),
        ("LangGraph agents", "Not connected"),
    ]:
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;padding:.65rem 0;border-bottom:1px solid rgba(148,163,184,.1)">'
            f'<span style="color:#dce7f7">{label}</span><span style="color:#e8bd72;font-size:.78rem">{status}</span></div>',
            unsafe_allow_html=True,
        )
    st.caption("API keys and credentials will be configured securely through environment variables or deployment secrets.")


# ---------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------
st.markdown("---")
st.markdown(
    """
    <div style="display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap;color:#71819a;font-size:.72rem">
      <span>✦ NEXUS AI · ENTERPRISE INTELLIGENCE PLATFORM</span>
      <span>Foundation build · Local session data · Backend integrations pending</span>
    </div>
    """,
    unsafe_allow_html=True,
)
