"""
KNOWLEDGE LOADER
Módulo para carregar e gerenciar a base de conhecimento (ficheiros MD)
"""

from pathlib import Path


def load_knowledge_base_file(filename: str) -> str:
    """Carrega um ficheiro MD da base de conhecimento"""
    base_dir = Path(__file__).parent.parent.parent
    filepath = base_dir / "src" / "knowledge_base" / filename

    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read().strip()
            if content:
                print(f"[OK] Base de conhecimento carregada: {filename}")
                return content

    print(f"[WARN] Ficheiro nao encontrado ou vazio: {filename}")
    return ""


# Carregar bases de conhecimento essenciais no startup
print("\n[INIT] Carregando bases de conhecimento...")
ORCHESTRATOR_KB = load_knowledge_base_file("orchestrator.md")
PROFESSOR_KB = load_knowledge_base_file("professor.md")
ALGEBRA_KB = load_knowledge_base_file("algebra.md")
TRIGONOMETRY_KB = load_knowledge_base_file("trigonometry.md")
INTEGRATION_KB = load_knowledge_base_file("integration.md")
print("[INIT] Bases de conhecimento carregadas com sucesso!\n")

