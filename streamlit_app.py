import json
import os
from typing import Any, Dict

import streamlit as st
from dotenv import load_dotenv

# Local imports
from langgraph_builder import Runner

load_dotenv()

st.set_page_config(page_title="Analytos.ai - Workflow", layout="wide")

# Header
st.markdown(
    """
    <style>
      html, body, [data-testid="stAppViewContainer"], [class^="st-"] { font-size: 18px; }
      .hero {background: linear-gradient(135deg, #6D28D9, #0EA5E9); color: #fff; border-radius: 14px; padding: 22px 24px; margin: 8px 0 18px 0; box-shadow: 0 8px 24px rgba(109,40,217,0.25);} 
      .hero h2 { font-size: 28px; }
      .step-h {font-weight:900; font-size:22px; color:#111827; margin: 12px 0 8px 0; background:#F3F4F6; padding:10px 12px; border-radius:10px; border:1px solid #E5E7EB}
      .card {border:1px solid #e5e7eb; border-radius:12px; padding:16px; background:#fff; box-shadow: 0 6px 16px rgba(2,6,23,0.06); margin-bottom:14px}
      .muted {color:#111827; font-weight:700; font-size:18px}
      pre {white-space: pre-wrap; word-wrap: break-word; font-size: 16px;}
    </style>
    <div class="hero">
      <h2 style="margin:0 0 6px 0">Prospect-to-Lead Workflow</h2>
      <div>Analytos.ai · Execution Console</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Controls")
    workflow_path = st.text_input("Workflow JSON path", value="workflow.json")
    run_button = st.button("Run Workflow")

# Load workflow
wf: Dict[str, Any] = {}
try:
    with open(workflow_path, "r", encoding="utf-8") as f:
        wf = json.load(f)
except Exception as e:
    st.error(f"Failed to load workflow.json: {e}")
    st.stop()

steps = wf.get("steps", [])
config = wf.get("config", {})

# Overview
c1, c2 = st.columns([1, 1])
with c1:
    st.subheader("Workflow")
    st.json({"name": wf.get("workflow_name"), "description": wf.get("description", "")})
with c2:
    st.subheader("Config")
    st.json(config)

st.subheader("Steps")
for i, s in enumerate(steps, start=1):
    st.markdown(f"<div class='card'><div class='step-h'>{i}. {s.get('id')}</div><div class='muted'>{s.get('agent')}</div></div>", unsafe_allow_html=True)

# Run section
if run_button:
    total = max(len(steps), 1)
    progress = st.progress(0, text="Starting...")
    state: Dict[str, Any] = {"config": config}

    for idx, step in enumerate(steps, start=1):
        progress.progress(int((idx - 1) / total * 100), text=f"Running {step['id']} ({idx}/{total})")
        runner = Runner(step, config)

        out: Dict[str, Any]
        try:
            state = runner(state)
            out = state.get(step["id"], {}).get("output", {})
        except Exception as e:
            out = {"error": str(e)}

        # Per-step heading and output
        st.markdown(f"<div class='step-h'>{step['id']} ({step['agent']})</div>", unsafe_allow_html=True)
        st.json(out)

    progress.progress(100, text="Workflow completed")
    st.success("Done")
