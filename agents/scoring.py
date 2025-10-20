from typing import Dict, Any, List
from .base import BaseAgent, AgentContext

class ScoringAgent(BaseAgent):
    name = "ScoringAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        enriched: List[Dict[str, Any]] = inputs.get("enriched_leads", [])
        criteria = inputs.get("scoring_criteria", {"weights": {}, "threshold": 0.5})
        weights = criteria.get("weights", {})
        ranked = []
        for e in enriched:
            # simple score: technologies match weight, presence of role, etc.
            tech_score = 1.0 if e.get("technologies") else 0.0
            role_score = 1.0 if e.get("role") and e.get("role") != "Unknown" else 0.0
            score = 0.5 * tech_score + 0.5 * role_score
            ranked.append({"lead": e, "score": score})
        ranked.sort(key=lambda x: x["score"], reverse=True)
        return {"ranked_leads": ranked}
