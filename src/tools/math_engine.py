from sympy import sympify, solve
import re

def resolver_equacao(equacao_str):
    try:
        # Se a string for vazia, não resolve
        if not equacao_str or equacao_str.strip() == "":
            return "Nenhuma equacao matematica isolada para calcular diretamente."

        # Proteção: Impede o SymPy de congelar com texto natural
        if re.search(r'[a-zA-Z]{5,}', equacao_str) and not any(func in equacao_str for func in ['sin', 'cos', 'tan', 'log', 'exp', 'sqrt']):
            return "Expressão contém texto inválido. Cálculo simbólico ignorado."

        # Transforma algo como "2x=10" em "2x - (10)" para o sympy calcular as raizes
        if "=" in equacao_str:
            lado_esq, lado_dir = equacao_str.split('=')
            expressao = f"({lado_esq}) - ({lado_dir})"
        else:
            expressao = equacao_str

        equacao = sympify(expressao)
        solucao = solve(equacao)
        return str(solucao[0]) if solucao else "Sem solucao obvia ou calculo algebrico nao aplicavel"
    except Exception as e:
        return "Calculo simbolico direto (SymPy) indisponivel para este formato."
