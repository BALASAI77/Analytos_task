from typing import Dict, Any, List
from .base import BaseAgent, AgentContext
from .utils import http_request

class ProspectSearchAgent(BaseAgent):
    name = "ProspectSearchAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        self.log("starting", inputs=inputs)
        icp = inputs.get("icp", {})
        signals = inputs.get("signals", [])
        use_mock = self.is_mock(ctx)
        if use_mock:
            leads = [
                {"company": "Acme Corp", "contact_name": "Jane Doe", "email": "jane@acme.com", "linkedin": "https://lnkd.in/jane", "signal": "recent_funding"},
                {"company": "BetaSoft", "contact_name": "John Smith", "email": "john@betasoft.io", "linkedin": "https://lnkd.in/john", "signal": "hiring_for_sales"}
            ]
            return {"leads": leads}
        clay = next((t for t in ctx.tools if t.get("name")=="ClayAPI"), None)
        apollo = next((t for t in ctx.tools if t.get("name")=="ApolloAPI"), None)
        results: List[Dict[str, Any]] = []
        if clay:
            conf = clay.get("config", {})
            data = http_request("POST", conf.get("endpoint"), headers={"Authorization": f"Bearer {conf.get('api_key','')}"}, json_body={"icp": icp, "signals": signals})
            self.log("clay_response", size=len(data) if isinstance(data, list) else 1)
        if apollo:
            conf = apollo.get("config", {})
            data2 = http_request("POST", conf.get("endpoint"), headers={"Authorization": conf.get('api_key','')}, json_body={"q_organization_num_employees": icp.get("employee_count", {}), "q_organization_locations": icp.get("location")})
            self.log("apollo_response", got=bool(data2))
        # Here we just return mock-shaped merged results for demo
        if not results:
            results = [
                {"company": "Acme Corp", "contact_name": "Jane Doe", "email": "jane@acme.com", "linkedin": "https://lnkd.in/jane", "signal": signals[0] if signals else ""}
            ]
        return {"leads": results}
