from typing import Dict, Any
from .base import BaseAgent, AgentContext
from .utils import http_request, pick_tech_stack

class DataEnrichmentAgent(BaseAgent):
    name = "DataEnrichmentAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        self.log("starting", inputs=list(inputs.keys()))
        leads = inputs.get("leads", [])
        use_mock = self.is_mock(ctx)
        if use_mock:
            enriched = [{"company": l["company"], "contact": l["contact_name"], "role": "Head of Sales", "technologies": pick_tech_stack()} for l in leads]
            return {"enriched_leads": enriched}
        clearbit = next((t for t in ctx.tools if t.get("name") == "Clearbit"), None)
        enriched = []
        for l in leads:
            if clearbit:
                conf = clearbit.get("config", {})
                resp = http_request("GET", "https://person.clearbit.com/v2/combined/find", headers={"Authorization": f"Bearer {conf.get('api_key','')}"}, params={"email": l.get("email")})
                self.log("clearbit_resp", company=l.get("company"))
                enriched.append({"company": l.get("company"), "contact": l.get("contact_name"), "role": resp.get("person", {}).get("employment", {}).get("title", "Unknown"), "technologies": pick_tech_stack()})
            else:
                enriched.append({"company": l.get("company"), "contact": l.get("contact_name"), "role": "Unknown", "technologies": pick_tech_stack()})
        return {"enriched_leads": enriched}
