"""
AGENTE ORQUESTRADOR
Responsabilidade: Triagem e normalização do input do utilizador
Entrada: pergunta bruta
Saída: problema_normalizado
"""

from .knowledge_loader import ORCHESTRATOR_KB
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def execute(state: dict) -> dict:
    """
    Processa o input bruto do utilizador
    - Normaliza a entrada (LaTeX, formatação)
    - Valida se é problem matemático válido
    - Reformula de forma clara e estruturada
    """
    print("\n" + "="*70)
    print("FASE 1: ORQUESTRADOR (Triagem e Normalizacao)")
    print("="*70)

    pergunta = state["pergunta"]

    prompt = f"""{ORCHESTRATOR_KB}

Tu recebeste o seguinte input do utilizador:
"{pergunta}"

Tua tarefa: 
1. Se for uma imagem, extrai o texto com precisão
2. Se for texto, normaliza para formato matemático padrão
3. Valida se é um problema matemático válido
4. Reformula o problema de forma clara e estruturada

Responde APENAS com o problema reformulado e validado, sem explicações adicionais."""

    try:
        msg = llm.invoke([("system", prompt), ("user", pergunta)])
        problema_normalizado = msg.content.strip()
        print(f"[OK] Problema normalizado pelo Orquestrador")
        return {"problema_normalizado": problema_normalizado}
    except Exception as e:
        print(f"[ERRO] Erro no Orquestrador: {str(e)}")
        return {"problema_normalizado": pergunta}

