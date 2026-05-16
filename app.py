import streamlit as st
import time
import base64
import PyPDF2
import os
from io import BytesIO
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from main import app_graph  # Importa o grafo atualizado

# ==========================================
# CONFIGURAÇÃO DA PÁGINA (Deve ser a primeira linha do Streamlit)
# ==========================================
st.set_page_config(
    page_title="Tutor de Matemática IA",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==========================================
# INICIALIZAÇÃO DE VARIÁVEIS DE SESSÃO
# ==========================================
if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# INJEÇÃO DE CSS: FUNDO, ANIMAÇÕES E DESIGN (GLASSMORPHISM)
# ==========================================
# ==========================================
# INJEÇÃO DE CSS: FUNDO E DESIGN (GLASSMORPHISM)
# ==========================================
custom_css = """
<style>
/* Forçar o fundo diretamente na classe principal da app e aumentar a intensidade das cores */
.stApp {
    background-color: #05070a !important;
    background-image: 
        radial-gradient(circle at 15% 25%, rgba(107, 70, 193, 0.4) 0%, transparent 55%),
        radial-gradient(circle at 85% 75%, rgba(14, 165, 233, 0.35) 0%, transparent 55%) !important;
    background-attachment: fixed !important;
}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.4);
}

/* Tornar o cabeçalho superior transparente */
[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Estilizar a caixa de texto para ter um efeito "vidro" (Glassmorphism) */
.stTextArea textarea {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px;
    color: #f8fafc !important;
    font-size: 16px;
    backdrop-filter: blur(10px);
}
.stTextArea textarea:focus {
    border-color: rgba(14, 165, 233, 0.6) !important;
    box-shadow: 0 0 15px rgba(14, 165, 233, 0.2) !important;
}

/* Estilizar o botão para ficar moderno e atrativo */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5 0%, #0ea5e9 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2) !important;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(14, 165, 233, 0.5) !important;
    background: linear-gradient(135deg, #4338ca 0%, #0284c7 100%) !important;
}

/* Ajustes gerais de tipografia */
h1, h2, h3, p, span, div {
    color: #e2e8f0;
}

/* Estilo do histórico */
.history-item {
    background-color: rgba(255, 255, 255, 0.03);
    border-left: 3px solid rgba(14, 165, 233, 0.5);
    padding: 10px 15px;
    margin-bottom: 15px;
    border-radius: 0 8px 8px 0;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)


# ==========================================
# BARRA LATERAL (HISTÓRICO)
# ==========================================
with st.sidebar:
    st.markdown("### Histórico de Sessão")
    if not st.session_state.history:
        st.markdown("<p style='font-size: 14px; color: #94a3b8;'>Ainda não foram resolvidos problemas.</p>", unsafe_allow_html=True)
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            st.markdown(f"<div class='history-item'><b>Q:</b> {item['pergunta'][:50]}...<br><b>Tema:</b> {item['tema']}</div>", unsafe_allow_html=True)

        if st.button("Limpar Histórico", use_container_width=True):
            st.session_state.history = []
            st.rerun()


# ==========================================
# INTERFACE DO UTILIZADOR
# ==========================================

# Cabeçalho
logo_path = os.path.join("src", "img", "logo.png")
if os.path.exists(logo_path):
    col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
    with col_logo2:
        st.image(logo_path, use_container_width=True)
else:
    st.markdown("<h1 style='text-align: center; color: white;'>Tutor de Matemática</h1>",
                unsafe_allow_html=True)

st.markdown(
    "<p style='text-align: center; color: #94a3b8;'>Trigonometria, Primitivação e Álgebra — Explicações passo a passo.</p>",
    unsafe_allow_html=True)

st.write("")  # Espaço em branco
st.write("")

# Upload de ficheiros
uploaded_file = st.file_uploader("Pretendes anexar uma Imagem ou PDF?", type=["png", "jpg", "jpeg", "pdf"])

# Caixa principal de entrada
problema = st.text_area(
    "Como te posso ajudar hoje?",
    placeholder="Ex: Qual é a derivada de x^2? ou Calcula a primitiva de sin(x)*cos(x)",
    height=120
)

st.write("")

# Botão de submissão (centrado através de colunas)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    submit = st.button("Resolver com IA", use_container_width=True)

# Lógica ao clicar no botão
if submit:
    if problema.strip() == "" and uploaded_file is None:
        st.warning("Por favor, escreve um problema matemático ou anexa um ficheiro antes de avançar.")
    else:
        # Estado de loading animado
        with st.spinner("A processar os dados..."):
            conteudo_extraido = ""

            if uploaded_file is not None:
                file_type = uploaded_file.type
                if "pdf" in file_type:
                    try:
                        reader = PyPDF2.PdfReader(uploaded_file)
                        for page in reader.pages:
                            text = page.extract_text()
                            if text:
                                conteudo_extraido += text + "\n"
                    except Exception as e:
                        st.error(f"Erro ao ler PDF: {e}")
                elif "image" in file_type:
                    try:
                        image_data = uploaded_file.getvalue()
                        encoded_image = base64.b64encode(image_data).decode("utf-8")

                        llm_vision = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
                        message = HumanMessage(
                            content=[
                                {"type": "text", "text": "Extrai detalhadamente todo o texto e expressões matemáticas presentes nesta imagem."},
                                {"type": "image_url", "image_url": {"url": f"data:{file_type};base64,{encoded_image}"}}
                            ]
                        )
                        response = llm_vision.invoke([message])
                        conteudo_extraido = response.content
                    except Exception as e:
                        st.error(f"Erro ao processar imagem: {e}")

            texto_final = problema.strip()
            if conteudo_extraido:
                texto_final += f"\n\n[CONTEÚDO DO FICHEIRO ANEXADO:]\n{conteudo_extraido}"

        with st.spinner("O Orquestrador e o Tutor estão a analisar o problema..."):

            # ==========================================
            # ÁREA DE INTEGRAÇÃO COM O MAIN.PY (GRAFO)
            # ==========================================
            inputs = {"pergunta": texto_final, "problema_normalizado": "", "tema_identificado": "",
                     "equacao": "", "conhecimento_especialista": "", "resultado": "", "explicacao": ""}
            config = {"configurable": {"thread_id": "1"}}
            out = app_graph.invoke(inputs, config)

            result = {
                "explicacao_final": out.get("explicacao", "Resposta gerada pela IA, mas no encontrada."),
                "resultado_exato": out.get("resultado", "N/A"),
                "problema_normalizado": out.get("problema_normalizado", "N/A"),
                "tema_identificado": out.get("tema_identificado", "N/A"),
                "equacao_extraida": out.get("equacao", "N/A"),
                "conhecimento_especialista": out.get("conhecimento_especialista", "N/A")
            }

            st.success("Problema analisado com sucesso!")

            # Guardar no histórico
            st.session_state.history.append({
                "pergunta": texto_final,
                "tema": result["tema_identificado"],
                "resposta": result["explicacao_final"]
            })

            # Expander para ver a linha de pensamento (validacao de MDs e PDFs)
            with st.expander("Ver Linha de Pensamento da IA (Validação de Bases de Conhecimento)"):
                st.markdown("Acompanhe como os agentes analisaram o problema consultando os `.md` e `PDFs` antes de gerar a resposta:")
                st.markdown(f"**Orquestrador (Normalização):**\n> {result['problema_normalizado']}")
                st.markdown(f"**Professor (Triagem Lógica):**\n> Tema Identificado: `{result['tema_identificado'].upper()}`\n>\n> Equação/Expressão SymPy: `{result['equacao_extraida']}`")
                st.markdown("**Especialista (Fetch de Conhecimento .md e .pdf):**")
                if result['conhecimento_especialista'].strip() == "":
                    st.warning("O especialista não gerou output ou o tema era geral.")
                else:
                    st.code(result['conhecimento_especialista'], language="markdown")

            # Exibir a resposta pedaggica
            st.markdown("### Resposta do Tutor:")
            st.info(result["explicacao_final"])

            # Botão de download da resolução
            st.download_button(
                label="Descarregar Explicação Completa",
                data=f"Pergunta:\n{texto_final}\n\nResposta do Tutor:\n{result['explicacao_final']}\n\nResultado Exato (Motor Math):\n{result['resultado_exato']}",
                file_name="explicacao_matematica.txt",
                mime="text/plain",
                use_container_width=True
            )

            # Área técnica expansível
            with st.expander("Ver cálculo nos bastidores (SymPy Engine)"):
                st.markdown("O agente verificou a resposta matematicamente para garantir precisão:")
                st.code(f"Output computado: {result['resultado_exato']}", language="python")

# Rodapé simples
st.markdown("---")
st.markdown(
    "<p style='text-align: center; font-size: 12px; color: #64748b;'>Desenvolvido pela Equipa no Hackathon • Potenciado por LangGraph e SymPy</p>",
    unsafe_allow_html=True)