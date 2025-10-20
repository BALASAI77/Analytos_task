import os
import json
import logging
from dataclasses import dataclass
from typing import Any, Dict
from dotenv import load_dotenv

load_dotenv()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger("agents")

@dataclass
class AgentContext:
    step_id: str
    instructions: str
    tools: list
    globals: Dict[str, Any]

class BaseAgent:
    name: str = "BaseAgent"

    def __init__(self):
        # 'true' -> force mock, 'false' -> force live, 'auto' or unset -> per-step autodetect
        self._mock_mode_raw = os.getenv("MOCK_MODE", "auto").lower()

    def log(self, msg: str, **kwargs):
        logger.info(f"[{self.name}] {msg} | {json.dumps(kwargs, default=str)}")

    def run(self, inputs: Dict[str, Any], ctx: AgentContext) -> Dict[str, Any]:
        raise NotImplementedError

    def is_mock(self, ctx: AgentContext) -> bool:
        """Decide mock vs live per step.
        - If MOCK_MODE=true -> mock
        - If MOCK_MODE=false -> live
        - Else (auto/unset): mock if any required credential for the step's tools is missing.
        """
        if self._mock_mode_raw == "true":
            return True
        if self._mock_mode_raw == "false":
            return False
        # auto mode: inspect tools' configs
        tools = ctx.tools or []
        if not tools:
            # No external tools -> run live computations
            return False
        def requires_value(key: str) -> bool:
            k = key.lower()
            return (
                k == "api_key"
                or "api" in k and "endpoint" not in k
                or "key" in k
                or k == "sheet_id"
                or "service_account" in k
            )
        for t in tools:
            conf = (t or {}).get("config", {})
            for k, v in (conf or {}).items():
                if requires_value(k):
                    if not isinstance(v, str) or len(v.strip()) == 0:
                        return True  # missing credential -> mock
                    # For service account path, ensure file exists
                    if "service_account" in k.lower():
                        if not os.path.isfile(v):
                            return True
        return False
