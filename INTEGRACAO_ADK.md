# Instruções para Integração com Google ADK

## 🔧 Status Atual
Atualmente, o projeto está usando **mocks** (simulações) da biblioteca Google ADK para demonstração, pois a biblioteca real não está disponível no ambiente.

## 📋 Para usar a biblioteca Google ADK real:

### 1. Instalar a biblioteca
```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Instalar Google ADK (quando disponível)
pip install google-adk
# ou
uv add google-adk
```

### 2. Atualizar os arquivos de agentes

**search/agent.py:**
```python
# Remover a classe mock e usar a importação real:
from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="search",
    model="gemini-2.5-flash",
    description="Você é um agente buscador do google",
    instruction="""...""",
    tools=[google_search]
)
```

**base/agent.py:**
```python
# Remover a classe mock e usar a importação real:
from google.adk.agents import Agent

root_agent = Agent(
    name="base",
    model="gemini-2.5-flash",
    description="Você é um agente base assistente geral",
    instruction="""...""",
    tools=[]
)
```

### 3. Atualizar web_app.py
```python
# Adicionar lógica real de execução dos agentes
def execute_agent(agent, prompt):
    # Usar a API real do Google ADK
    response = agent.execute(prompt)
    return response
```

### 4. Configurar credenciais
- Configurar API keys necessárias
- Configurar autenticação do Google
- Definir variáveis de ambiente

## 🚀 Enquanto isso...
O projeto funciona perfeitamente como demonstração com as simulações implementadas!

- ✅ Interface web funcional
- ✅ Seleção de agentes
- ✅ Chat interativo
- ✅ Respostas simuladas personalizadas por agente

Execute `adk web` e acesse http://localhost:8501 para testar!