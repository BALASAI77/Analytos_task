import os
import json
import time
import random
import requests
from typing import Dict, Any, List

RETRYABLE = (requests.exceptions.Timeout, requests.exceptions.ConnectionError)

def resolve_config_placeholders(config: Dict[str, Any]) -> Dict[str, Any]:
    def repl(val):
        if isinstance(val, str) and val.startswith("{{") and val.endswith("}}"): 
            key = val.strip("{} ")
            return os.getenv(key, "")
        return val
    if isinstance(config, dict):
        return {k: resolve_config_placeholders(v) for k, v in config.items()}
    if isinstance(config, list):
        return [resolve_config_placeholders(v) for v in config]
    return repl(config)

def http_request(method: str, url: str, headers: Dict[str, str] | None = None, params=None, json_body=None, retries: int = 3, backoff: float = 0.5):
    for i in range(retries):
        try:
            resp = requests.request(method, url, headers=headers, params=params, json=json_body, timeout=30)
            if resp.status_code >= 400:
                raise requests.HTTPError(f"HTTP {resp.status_code}: {resp.text}")
            return resp.json()
        except RETRYABLE:
            time.sleep(backoff * (2 ** i))
    raise

def pick_tech_stack() -> List[str]:
    pools = [["Salesforce", "HubSpot"], ["AWS", "GCP", "Azure"], ["Snowflake", "Databricks"], ["Segment", "Rudderstack"], ["Amplitude", "Mixpanel"]]
    return [random.choice(p) for p in pools]
