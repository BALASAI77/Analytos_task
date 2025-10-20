from .base import BaseAgent, AgentContext
from .prospect_search import ProspectSearchAgent
from .enrichment import DataEnrichmentAgent
from .scoring import ScoringAgent
from .outreach_content import OutreachContentAgent
from .outreach_executor import OutreachExecutorAgent
from .response_tracker import ResponseTrackerAgent
from .feedback_trainer import FeedbackTrainerAgent

AGENT_REGISTRY = {
    "ProspectSearchAgent": ProspectSearchAgent,
    "DataEnrichmentAgent": DataEnrichmentAgent,
    "ScoringAgent": ScoringAgent,
    "OutreachContentAgent": OutreachContentAgent,
    "OutreachExecutorAgent": OutreachExecutorAgent,
    "ResponseTrackerAgent": ResponseTrackerAgent,
    "FeedbackTrainerAgent": FeedbackTrainerAgent,
}
