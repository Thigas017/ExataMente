# ExataMente

Aplicação Streamlit para resolver problemas de Matemática com ajuda de agentes baseados em LangGraph, LangChain, SymPy e Google Gemini.

## Funcionalidades

- Resolver problemas matemáticos em texto
- Aceitar anexos em PDF e imagem
- Extrair texto de PDFs e imagens
- Mostrar a resolução passo a passo
- Guardar histórico da sessão

## Requisitos

- Python 3.10+ recomendado
- Uma chave válida do Google Gemini no ambiente (`GOOGLE_API_KEY`)

## Instalação local

1. Criar e ativar um ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependências:

```powershell
python -m pip install -r requirements.txt
```

3. Criar um ficheiro `.env` na raiz do projeto com a tua chave:

```env
GOOGLE_API_KEY=coloca_a_tua_chave_aqui
```

4. Executar a aplicação:

```powershell
python -m streamlit run app.py
```

## Estrutura principal

- `app.py` — interface Streamlit
- `main.py` — grafo principal dos agentes
- `src/agents/` — agentes especializados
- `src/knowledge_base/` — bases de conhecimento em Markdown e PDF
