import argparse
import json
import os
from copy import deepcopy
from typing import Any, Dict
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# LangGraph imports
try:
    from langgraph.graph import StateGraph, END
except Exception:
    StateGraph = None
    END = None

from agents import AGENT_REGISTRY, BaseAgent, AgentContext
from agents.utils import resolve_config_placeholders

class NodeState(BaseModel):
    data: Dict[str, Any] = {}

class Runner:
    def __init__(self, step: Dict[str, Any], globals_cfg: Dict[str, Any]):
        self.step = step
        self.agent: BaseAgent = AGENT_REGISTRY[step["agent"]]()
        self.ctx = AgentContext(
            step_id=step["id"],
            instructions=step.get("instructions", ""),
            tools=resolve_config_placeholders(deepcopy(step.get("tools", []))),
            globals=globals_cfg,
        )

    def __call__(self, state: Dict[str, Any]):
        # Resolve templated inputs from state
        inputs = _materialize_inputs(self.step.get("inputs", {}), state)
        out = self.agent.run(inputs, self.ctx)
        # Store under step id path
        new_state = deepcopy(state)
        new_state[self.step["id"]] = {"output": out}
        return new_state

def _materialize_inputs(spec: Any, state: Dict[str, Any]):
    if isinstance(spec, str) and spec.startswith("{{") and spec.endswith("}}"): 
        path = spec.strip("{} ")
        parts = path.split(".")
        cur = state
        for p in parts:
            cur = cur.get(p, {})
        return cur
    if isinstance(spec, dict):
        return {k: _materialize_inputs(v, state) for k, v in spec.items()}
    if isinstance(spec, list):
        return [_materialize_inputs(v, state) for v in spec]
    return spec

def build_and_run(workflow_path: str, persist: str | None = None):
    with open(workflow_path, "r", encoding="utf-8") as f:
        wf = json.load(f)
    steps = wf.get("steps", [])
    globals_cfg = wf.get("config", {})

    if StateGraph is None:
        # Fallback: sequential execution without LangGraph installed
        state: Dict[str, Any] = {"config": globals_cfg}
        for step in steps:
            runner = Runner(step, globals_cfg)
            state = runner(state)
        print(json.dumps(state.get(steps[-1]["id"], {}).get("output", {}), indent=2))
        return

    # With LangGraph
    graph = StateGraph(dict)
    runners = {s["id"]: Runner(s, globals_cfg) for s in steps}
    for s in steps:
        graph.add_node(s["id"], runners[s["id"]])
    # Add linear edges in given order
    for i in range(len(steps) - 1):
        graph.add_edge(steps[i]["id"], steps[i+1]["id"])
    graph.set_entry_point(steps[0]["id"])
    graph.add_edge(steps[-1]["id"], END)
    app = graph.compile()
    init = {"config": globals_cfg}
    final = app.invoke(init)
    last_out = final.get(steps[-1]["id"], {}).get("output", {})
    print(json.dumps(last_out, indent=2))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--workflow", default="workflow.json")
    p.add_argument("--persist", default=None)
    args = p.parse_args()
    build_and_run(args.workflow, args.persist)
