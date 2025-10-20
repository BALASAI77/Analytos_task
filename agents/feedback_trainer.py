import json
import os
from typing import Dict, Any, List
from .base import BaseAgent, AgentContext

class FeedbackTrainerAgent(BaseAgent):
    name = "FeedbackTrainerAgent"

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        responses: List[Dict[str, Any]] = inputs.get("responses", [])
        opens = sum(r.get("opens", 0) for r in responses)
        clicks = sum(r.get("clicks", 0) for r in responses)
        replies = sum(r.get("replies", 0) for r in responses)
        total = max(len(responses), 1)
        open_rate = opens / total
        reply_rate = replies / total
        recs = []
        if open_rate < 0.5:
            recs.append({"type": "subject_line", "action": "test_more_curiosity", "reason": "low open rate"})
        if reply_rate < 0.2:
            recs.append({"type": "body", "action": "shorten_and_add_specific_value_prop", "reason": "low reply rate"})
        recs.append({"type": "icp", "action": "narrow_employee_range", "reason": "optimize fit"})
        self._write_to_sheets(recs, ctx)
        return {"recommendations": recs}

    def _write_to_sheets(self, recs: List[Dict[str, Any]], ctx: AgentContext):
        use_mock = self.is_mock(ctx)
        if use_mock:
            self.log("sheets_write_skipped_mock", count=len(recs))
            return
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            sheet_id = next((t.get("config", {}).get("sheet_id") for t in ctx.tools if t.get("name") == "GoogleSheets"), None)
            if not sheet_id:
                return
            sa_path = os.getenv("GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON")
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            creds = Credentials.from_service_account_file(sa_path, scopes=scopes)
            gc = gspread.authorize(creds)
            sh = gc.open_by_key(sheet_id)
            ws = sh.sheet1
            for r in recs:
                ws.append_row([r.get("type"), r.get("action"), r.get("reason")])
        except Exception as e:
            self.log("sheets_write_error", error=str(e))
