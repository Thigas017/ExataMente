"""
AGENTE TUTOR
Responsabilidade: Explicação pedagógica final
Entrada: pergunta_original, equacao, resultado, conhecimento_especialista
Saída: explicacao
"""

from .knowledge_loader import PROFESSOR_KB
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


def execute(state: dict) -> dict:
    """
    Tutor fornece explicação pedagógica final
    - Integra todo o conhecimento
    - Cria explicação clara e didática
    - Guia passo a passo
    - Explica o "porque" não apenas o "como"
    """
    print("\n" + "="*70)
    print("FASE 5: TUTOR (Explicacao Pedagogica)")
    print("="*70)

    pergunta_original = state["pergunta"]
    equacao = state["equacao"]
    resultado = state["resultado"]
    conhecimento = state.get("conhecimento_especialista", "")

    prompt = f"""{PROFESSOR_KB}

Tu es o Tutor. Agora tens toda a informacao necessária:

PROBLEMA ORIGINAL DO ALUNO:
"{pergunta_original}"

EQUACAO/EXPRESSAO:
"{equacao}"

CONHECIMENTO ESPECIALIZADO DO DOMINIO:
{conhecimento}

RESULTADO EXATO (calculado):
{resultado}

Tua tarefa como Tutor:
1. Cria uma explicacao pedagógica clara e completa
2. Guia o aluno passo a passo
3. Explica o "porque" de cada passo, nao apenas o "como"
4. Usa a informacao especializada para enriquecer a explicacao
5. Termina com o resultado final em destaque

Comeca com um tom amigável e motivador.
NUNCA des a resposta no primeiro paragrafo - ensina o processo."""

    try:
        msg = llm.invoke([("system", prompt), ("user", pergunta_original)])
        explicacao = msg.content.strip()

        print(f"[OK] Explicacao pedagogica gerada pelo Tutor")

        return {"explicacao": explicacao}
    except Exception as e:
        print(f"[ERRO] Erro no Tutor: {str(e)}")
        return {"explicacao": f"Erro ao gerar explicacao: {str(e)}"}

