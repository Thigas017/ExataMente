import json
import re  # Importar regex para extração segura de JSON
from .knowledge_loader import PROFESSOR_KB
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

def execute(state: dict) -> dict:
    print("\n" + "="*70)
    print("FASE 2: PROFESSOR (Analise e Coordenacao)")
    print("="*70)

    problema_normalizado = state["problema_normalizado"]

    prompt = f"""{PROFESSOR_KB}

O Orquestrador já normalizou o seguinte problema:
"{problema_normalizado}"

Tua tarefa como Professor:
1. Analisa o problema e CLASSIFICA OBRIGATORIAMENTE em UM dos domínios matemáticos abaixo:
   - 'integration' -> se contiver derivadas, integrais ou primitivas.
   - 'trigonometry' -> se contiver senos, cossenos, tangentes, secantes, triângulos ou ângulos.
   - 'algebra' -> se contiver polinómios, equações, variáveis (x, y), raízes, logaritmos, funções de base, ou algebra geral.
   - 'geral' -> usar APENAS para questões não matemáticas ou aritmética crua e muito básica.
2. Extrai a equação ou expressão principal.
3. Estrutura uma abordagem pedagógica clara.

Responde APENAS em JSON com o seguinte formato EXACTO:
{{
    "equacao": "APENAS a formula no formato puro SymPy (ex: 1/x). NUNCA texto natural. Se nao houver, deixe vazio",
    "tema": "algebra|trigonometry|integration|geral",
    "estrutura_pedagogica": "breve descrio da abordagem"
}}"""

    try:
        msg = llm.invoke([("system", prompt), ("user", problema_normalizado)])
        
        # Extração Robusta do JSON usando Regex
        match = re.search(r'\{.*\}', msg.content, re.DOTALL)
        if not match:
            raise ValueError("O LLM não retornou um formato JSON válido.")
            
        texto_limpo = match.group(0)
        dados = json.loads(texto_limpo)

        tema = dados.get("tema", "geral").lower()
        equacao = dados.get("equacao", "")

        print(f"[OK] Problema analisado pelo Professor")
        print(f"  - Tema identificado: {tema}")
        print(f"  - Equacao: {equacao}")

        return {
            "tema_identificado": tema,
            "equacao": equacao
        }
    except Exception as e:
        print(f"[ERRO] Erro no Professor: {str(e)}")
        return {
            "tema_identificado": "geral",
            "equacao": problema_normalizado
        }