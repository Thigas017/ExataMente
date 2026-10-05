# ExataMente — AI Mathematical Tutor

## 1. Project Overview

**ExataMente** is an AI-powered mathematics tutoring application built with Streamlit, LangGraph, LangChain, Google Gemini, and SymPy.

The system allows users to submit mathematics problems as text, PDFs, or images. An agentic workflow then analyzes the problem, identifies the mathematical topic, retrieves relevant knowledge, performs or verifies calculations, and generates a clear, step-by-step pedagogical explanation.

The main goal is not simply to produce an answer, but to provide a reliable and educational solution, following the principle:

> **Understand → Structure → Analyze → Retrieve → Calculate → Explain**

## 2. Architecture & Input Processing

The application is organized into five main layers: Presentation, Input Processing, Agentic Workflow, Knowledge & Computation, and Educational Response.

### High-Level System Architecture

```bash
                    USER
                     │
                     ▼
            ┌─────────────────┐
            │  Streamlit UI   │
            └────────┬────────┘
                     │
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
┌───────┐        ┌───────┐        ┌───────┐
│ TEXT  │        │  PDF  │        │ IMAGE │
└───────┘        └───────┘        └───────┘
    │                │                │
    └────────────────┼────────────────┘
                     ▼
            ┌─────────────────┐
            │ Input Processing│
            │  & Extraction   │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   LangGraph     │
            │   Workflow      │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │  Step-by-Step   │
            │  Explanation    │
            └────────┬────────┘
                     │
                     ▼
                    USER
```

**Input Processing Methods:**

* **Text:** Direct input via the UI.
* **PDF:** Text is extracted using PyPDF2 and incorporated into the problem state.
* **Image:** Processed using Google Gemini to accurately extract text and complex mathematical expressions.

## 3. The Multi-Agent Workflow

The central concept of ExataMente is dividing the mathematical problem into specialized responsibilities instead of asking one large language model to perform the entire task.

### Agent Collaboration Flow

```bash
                    USER
                     │
                     ▼
            ┌─────────────────┐
            │  ORCHESTRATOR   │
            │  Normalize      │
            └────────┬────────┘
                     │
                     ▼
            ┌─────────────────┐
            │   PROFESSOR     │
            │  Analyze        │
            │  Classify       │
            └────────┬────────┘
                   /   \
                 /       \
               ▼           ▼
    ┌────────────┐       ┌────────────┐
    │ SPECIALIST │       │ CALCULATOR │
    │ Knowledge  │       │   SymPy    │
    └─────┬──────┘       └──────┬─────┘
          │                     │
          └──────────┬──────────┘
                     │
                     ▼
            ┌─────────────────┐
            │     TUTOR       │
            │  Explain        │
            │  Teach          │
            └────────┬────────┘
                     │
                     ▼
                FINAL ANSWER
```

### Specialized Responsibilities

1. **Orchestrator:** Coordinates the workflow, normalizes the raw problem statement, and maintains the LangGraph state.
2. **Professor:** Performs mathematical analysis. It identifies the specific mathematical topic and extracts the exact equation/expression to be solved.
3. **Specialist:** Interfaces with the project's local Knowledge Base (Markdown/PDF documents) to retrieve relevant definitions, formulas, and course-specific examples.
4. **Calculator:** Handles exact symbolic computation using **SymPy**. This deterministic engine ensures that calculations (derivatives, integrals, algebra) are mathematically sound, avoiding LLM hallucinations.
5. **Tutor:** Synthesizes the normalized problem, retrieved knowledge, and verified calculations into a step-by-step, student-friendly explanation.

### State-Based Workflow

The agents share and enrich a common state as the problem moves through the graph. Key state variables include: `pergunta`, `problema_normalizado`, `tema_identificado`, `equacao`, `conhecimento_especialista`, `resultado`, and `explicacao`. This transparent state makes the workflow highly inspectable and easy to debug.

## 4. Example Execution

**User Input:** *"Calculate the primitive of sin(x) \* cos(x)"*

1. **Orchestrator:** Normalizes to "Find the indefinite integral of sin(x) \* cos(x)."
2. **Professor:** Identifies Topic: `Integration`, Expression: `sin(x) * cos(x)`.
3. **Specialist:** Retrieves integration rules and trigonometric identities from the knowledge base.
4. **Calculator:** Uses SymPy to compute the exact symbolic result.
5. **Tutor:** Combines all data into a pedagogical explanation, walking the student through the substitution method, verifying the result, and presenting the final answer.

## 5. Technology Stack

| Technology | Role | 
| ----- | ----- | 
| **Python** (3.10+) | Core programming language | 
| **Streamlit** | Interactive web interface | 
| **LangGraph** | Agent and state/workflow orchestration | 
| **LangChain** | LLM abstractions and message handling | 
| **Google Gemini** | Core LLM for language and image understanding | 
| **SymPy** | Symbolic mathematics and deterministic verification | 
| **PyPDF2** | Document text extraction | 

## 6. Installation & Quick Start Guide

### Requirements

* Python 3.10+
* A valid Google Gemini API key

### Step-by-Step Setup

1. **Create and activate a virtual environment** (Using PowerShell):

   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. **Install the required dependencies**:

   ```bash
   python -m pip install -r requirements.txt
   pip install python-dotenv
   ```

3. **Configure Environment Variables**:
   Create a `.env` file in the project root directory and add your API key:

   ```env
   GOOGLE_API_KEY=your_google_gemini_api_key
   ```

   *(Warning: Do not commit the `.env` file or your API key to Git).*

4. **Run the application**:

   ```bash
   python -m streamlit run app.py
   ```

   Streamlit will start and provide a local address (e.g., `http://localhost:8501`) that can be opened in your browser.

## 7. Project Structure

```bash
ExataMente/
│
├── app.py                     # Streamlit frontend & file ingestion
├── main.py                    # Exposes the main workflow (app_graph)
├── requirements.txt           # Dependencies
├── .env                       # Environment configuration
│
├── src/
│   ├── agents/
│   │   ├── orchestrator_agent.py
│   │   ├── professor_agent.py
│   │   ├── specialist_agent.py
│   │   ├── calculator_agent.py
│   │   ├── tutor_agent.py
│   │   └── knowledge_loader.py
│   │
│   └── knowledge_base/        # Directory for Markdown and PDF knowledge files
│
└── ...
```