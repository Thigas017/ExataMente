"""
MAIN - ORQUESTRADOR PRINCIPAL DO GRAFO
Este ficheiro coordena o fluxo entre os 5 agentes especializados.
Cada agente é um módulo independente em src/agents/
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Carregar variáveis de ambiente ANTES de importar os agentes que instanciam o LLM
load_dotenv()

# Importar todos os agentes
from src.agents import (
    orchestrator_agent,
    professor_agent,
    specialist_agent,
    calculator_agent,
    tutor_agent
)

# ============================================================================
# 1. DEFINIR O ESTADO COMPARTILHADO
# ============================================================================

class MathState(TypedDict):
    """Estado que flui através de todos os agentes"""
    pergunta: str                          # Input original do utilizador
    problema_normalizado: str              # Output do Orquestrador
    tema_identificado: str                 # Output do Professor
    equacao: str                           # Output do Professor
    conhecimento_especialista: str         # Output do Especialista
    resultado: str                         # Output da Calculadora
    explicacao: str                        # Output do Tutor


# ============================================================================
# 2. DEFINIR OS NOS DO GRAFO (DELEGAM PARA OS AGENTES)
# ============================================================================

def node_orquestrador(state: MathState):
    """No que chama o agente Orquestrador"""
    return orchestrator_agent.execute(state)


def node_professor(state: MathState):
    """No que chama o agente Professor"""
    return professor_agent.execute(state)


def node_especialista(state: MathState):
    """No que chama o agente Especialista"""
    return specialist_agent.execute(state)


def node_calculadora(state: MathState):
    """No que chama o agente Calculadora"""
    return calculator_agent.execute(state)


def node_tutor(state: MathState):
    """No que chama o agente Tutor"""
    return tutor_agent.execute(state)


# ============================================================================
# 3. CONSTRUIR O GRAFO
# ============================================================================

workflow = StateGraph(MathState)

# Adicionar os nos
workflow.add_node("orquestrador", node_orquestrador)
workflow.add_node("professor", node_professor)
workflow.add_node("especialista", node_especialista)
workflow.add_node("calculadora", node_calculadora)
workflow.add_node("tutor", node_tutor)

# Definir o fluxo
workflow.set_entry_point("orquestrador")
workflow.add_edge("orquestrador", "professor")
workflow.add_edge("professor", "especialista")
workflow.add_edge("especialista", "calculadora")
workflow.add_edge("calculadora", "tutor")
workflow.add_edge("tutor", END)

# Compilar
app_graph = workflow.compile()

print("[OK] GRAFO COMPILADO COM SUCESSO")
