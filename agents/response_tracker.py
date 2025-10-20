from typing import Dict, Any
from .base import BaseAgent, AgentContext

class ResponseTrackerAgent(BaseAgent):
    name = "ResponseTrackerAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        campaign_id = inputs.get("campaign_id")
        use_mock = self.is_mock(ctx)
        if use_mock:
            responses = [
                {"lead": "Acme Corp", "opens": 2, "clicks": 1, "replies": 1},
                {"lead": "BetaSoft", "opens": 1, "clicks": 0, "replies": 0}
            ]
            return {"responses": responses}
        # Real tracking via Apollo API would be implemented here
        return {"responses": []}
