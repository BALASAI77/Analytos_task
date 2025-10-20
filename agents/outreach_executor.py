import os
from typing import Dict, Any
from .base import BaseAgent, AgentContext

class OutreachExecutorAgent(BaseAgent):
    name = "OutreachExecutorAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        messages = inputs.get("messages", [])
        use_mock = self.is_mock(ctx)
        if use_mock:
            status = [{"lead": m["lead"], "status": "sent"} for m in messages]
            return {"sent_status": status, "campaign_id": "CAMP-MOCK-001"}
        # Example SendGrid send (pseudo)
        import requests
        api_key = os.getenv("SENDGRID_API_KEY", "")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        status = []
        for m in messages:
            payload = {"personalizations": [{"to": [{"email": "prospect@example.com"}]}], "from": {"email": "sdr@yourdomain.com"}, "subject": f"Quick idea for {m['lead']}", "content": [{"type": "text/plain", "value": m['email_body']}]}
            r = requests.post("https://api.sendgrid.com/v3/mail/send", headers=headers, json=payload)
            status.append({"lead": m["lead"], "status": "sent" if r.status_code in (200, 202) else f"error:{r.status_code}"})
        return {"sent_status": status, "campaign_id": "CAMP-" + os.urandom(3).hex()}
