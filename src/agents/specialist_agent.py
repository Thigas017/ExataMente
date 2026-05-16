"""
AGENTE ESPECIALISTA
Responsabilidade: Fetch de conhecimento específico (Algebra/Trigonometry/Integration)
Entrada: tema_identificado, equacao
Saída: conhecimento_especialista
"""

from .knowledge_loader import ALGEBRA_KB, TRIGONOMETRY_KB, INTEGRATION_KB, PROFESSOR_KB
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def execute(state: dict) -> dict:
    """
    Agentes especialistas fornecem conhecimento específico
    - Carregam a base de conhecimento adequada
    - Fazem matching com padrões conhecidos
    - Fornecem fórmulas e métodos de resolução
    - Estruturam o conhecimento de forma técnica
    """
    print("\n" + "="*70)
    print("FASE 3: ESPECIALISTA (Fetch de Conhecimento Especifico)")
    print("="*70)

    tema = state["tema_identificado"]
    equacao = state["equacao"]

    # Selecionar a base de conhecimento apropriada
    bases_conhecimento = {
        "algebra": ALGEBRA_KB,
        "trigonometry": TRIGONOMETRY_KB,
        "integration": INTEGRATION_KB,
    }

    conhecimento_base = bases_conhecimento.get(tema, PROFESSOR_KB)

    prompt = f"""{conhecimento_base}

Equacao/Expresso a resolver:
"{equacao}"

Tua tarefa como Especialista:
1.  OBRIGATORIAMENTE, baseia-te estritamente nos documentos PDF fornecidos virtualmente antes de procurares qualquer informacao externa. O teu conhecimento basilar DEVE vir dos documentos da tua base de conhecimento (.md) e das formulas listadas ai.
2. Identifica o padro ou tipo de problema.
3. Seleciona a frmula ou mtodo apropriado usando os dados do teu sistema de conhecimento (`algebra-formulas-table.pdf`, `trig-identities-table.pdf`, `integration-rules-table.pdf` etc descritos nos manuais). 
4. Estrutura a soluao passo a passo seguindo rigidamente o modelo tecnico fornecido nos exemplos do teu MD.
5. Prepara a informacao para o Professor usar pedagogicamente

Responde de forma tcnica e estruturada, como exemplificado no MD."""

    try:
        msg = llm.invoke([("system", prompt), ("user", equacao)])
        conhecimento = msg.content.strip()

        print(f"[OK] Especialista em {tema.upper()} forneceu conhecimento")

        return {"conhecimento_especialista": conhecimento}
    except Exception as e:
        print(f"[ERRO] Erro no Especialista: {str(e)}")
        return {"conhecimento_especialista": ""}
