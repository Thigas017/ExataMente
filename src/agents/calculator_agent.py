"""
AGENTE CALCULADORA
Responsabilidade: Resolução matemática exata com SymPy
Entrada: equacao
Saída: resultado
"""

from src.tools.math_engine import resolver_equacao


def execute(state: dict) -> dict:
    """
    Calculadora faz a resolução matemática exata
    - Usa SymPy para resolver a equação
    - Fornece resultado numérico/simbólico
    - Garante precisão matemática
    """
    print("\n" + "="*70)
    print("FASE 4: CALCULADORA (Resolucao Matematica Exata)")
    print("="*70)

    equacao = state["equacao"]

    try:
        resultado = resolver_equacao(equacao)
        print(f"[OK] Calculo realizado: {resultado}")
        return {"resultado": resultado}
    except Exception as e:
        print(f"[WARN] Erro no calculo: {str(e)}")
        return {"resultado": f"Nao foi possivel calcular: {str(e)}"}

