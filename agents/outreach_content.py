import os
from typing import Dict, Any, List
from .base import BaseAgent, AgentContext

class OutreachContentAgent(BaseAgent):
    name = "OutreachContentAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        ranked = inputs.get("ranked_leads", [])
        persona = inputs.get("persona", "SDR")
        tone = inputs.get("tone", "friendly")
        use_mock = self.is_mock(ctx)
        if use_mock:
            msgs = [{"lead": r["lead"]["company"], "email_body": f"Hi {r['lead']['contact']}, quick idea for {r['lead']['company']}..."} for r in ranked]
            return {"messages": msgs}
        # Real LLM call via Google Gemini
        import google.generativeai as genai
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        outputs: List[Dict[str, str]] = []
        for r in ranked:
            company = r["lead"]["company"]
            contact = r["lead"].get("contact")
            techs = ", ".join(r["lead"].get("technologies", []))
            prompt = (
                f"Role: {persona}. Task: Write a concise, {tone} cold email (70-110 words) to {contact} at {company}. "
                f"Include value hypothesis and mention technologies: {techs}.\n"
                f"Think step-by-step to plan, but output ONLY the final email body."
            )
            resp = model.generate_content(prompt)
            email = (resp.text or "").strip()
            outputs.append({"lead": company, "email_body": email})
        return {"messages": outputs}
