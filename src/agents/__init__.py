"""
AGENTS MODULE
Exporta todos os agentes para uso no main.py
"""

from . import orchestrator_agent
from . import professor_agent
from . import specialist_agent
from . import calculator_agent
from . import tutor_agent

__all__ = [
    "orchestrator_agent",
    "professor_agent",
    "specialist_agent",
    "calculator_agent",
    "tutor_agent"
]
