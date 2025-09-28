# Mock da biblioteca google.adk para demonstração
class Agent:
    def __init__(self, name, model, description, instruction, tools=None):
        self.name = name
        self.model = model
        self.description = description
        self.instruction = instruction
        self.tools = tools or []

# Mock da ferramenta google_search
def google_search(query):
    return f"Resultado de busca simulado para: {query}"

root_agent = Agent(
    name="search",
    model="gemini-2.5-flash",
    description="Você é um agente buscador do google",
    instruction="""Você é um agente que usa a ferramenta do google para buscar e encontrar informações relevantes sobre a lei da aprendizagem 
    no Brasil. Seja específico e forneça detalhes importantes que possam ajudar na compreensão do tema, para o usuário, 
    usando a tool:
    - Google Search
    """,
    tools=[google_search]
)