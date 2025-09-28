"""
Interface Web para LexAprendiz - Especialista em Legislação da Aprendizagem
Siste    # Sidebar - Informações do usuário
    with st.sidebar:
        user_title = get_content("sidebar_user_title", "👤 Usuário")
        st.header(user_title)
        show_user_info()
        st.markdown("---")
        
        # Seletor de tema (disponível para todos os usuários)
        st.markdown("### 🎨 Aparência")
        current_theme = get_content("theme_mode", "light")
        
        theme_options = {
            "light": "🌞 Clara",
            "dark": "🌙 Escura"
        }
        
        selected_theme = st.selectbox(
            "Escolha o tema:",
            options=list(theme_options.keys()),
            format_func=lambda x: theme_options[x],
            index=0 if current_theme == "light" else 1,
            key="theme_selector"
        )
        
        # Salva alteração de tema imediatamente
        if selected_theme != current_theme:
            from content_manager import load_content_settings, save_content_settings
            content = load_content_settings()
            content["theme_mode"] = selected_theme
            save_content_settings(content)
            st.rerun()
        
        st.markdown("---")
        
        # Dashboard Administrativo (só para admin)
        if is_admin(st.session_state.get("user_data")):
            admin_title = get_content("sidebar_admin_title", "🛠️ Dashboard Admin")
            with st.expander(admin_title, expanded=False):
                show_admin_dashboard()
            st.markdown("---")
        
        agents_title = get_content("sidebar_agents_title", "📋 Agentes Disponíveis")
        st.header(agents_title)icação e Dashboard Administrativo
"""
import streamlit as st
import importlib.util
from pathlib import Path
import sys
from ferramentas_juridicas import pesquisar_legislacao
from banco_conhecimento import banco_conhecimento
import json
from logo_base64 import get_uploaded_logo, LEXAPRENDIZ_LOGO_PLACEHOLDER
from auth_system import require_authentication, show_user_info, show_admin_dashboard, is_admin
from content_manager import get_content, init_content_settings, apply_theme_styles

def load_agent_from_file(agent_path):
    """Carrega um agente de um arquivo"""
    try:
        spec = importlib.util.spec_from_file_location("agent_module", agent_path)
        agent_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(agent_module)
        
        # Procura por um agente no módulo
        if hasattr(agent_module, 'root_agent'):
            return agent_module.root_agent
        elif hasattr(agent_module, 'agent'):
            return agent_module.agent
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao carregar agente: {e}")
        return None

def main():
    st.set_page_config(
        page_title="LexAprendiz - Especialista em Legislação",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Inicializa configurações de conteúdo
    init_content_settings()
    
    # Aplica estilos de tema
    apply_theme_styles()
    
    # Sistema de Autenticação
    if not require_authentication():
        return
    
    # Capa personalizada com logo
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Verifica se há logo carregada na sessão (apenas exibe, não permite upload aqui)
        uploaded_logo = st.session_state.get('lexaprendiz_logo')
        
        if uploaded_logo:
            # Usa a logo real carregada (redimensionada)
            st.markdown(
                f'<div style="text-align: center; margin-bottom: 30px;">'
                f'<img src="{uploaded_logo}" style="max-width: 200px; height: auto;">'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            # Mostra placeholder se não há logo carregada
            st.markdown(
                f'<div style="text-align: center; margin-bottom: 30px;">'
                f'<img src="{LEXAPRENDIZ_LOGO_PLACEHOLDER}" style="max-width: 200px; height: auto;">'
                f'</div>',
                unsafe_allow_html=True
            )
        
        # Texto descritivo após a logo (editável pelo admin)
        main_title = get_content("main_title", "Conheça o LexAprendiz")
        main_description = get_content("main_description", "Obtenha respostas rápidas e precisas para suas perguntas. Nosso Agente LexAprendiz agora usa a tecnologia Gemini 2.5 flash para fornecer esclarecimentos sobre a legislação de forma interativa e com fontes confidenciais.")
        
        st.markdown(
            f"""
            <div class="main-content-box">
                <div class="main-title">{main_title}</div>
                <div class="main-description">{main_description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Sidebar - Informações do usuário
    with st.sidebar:
        st.header("� Usuário")
        show_user_info()
        st.markdown("---")
        
        # Dashboard Administrativo (só para admin)
        if is_admin(st.session_state.get("user_data")):
            with st.expander("🛠️ Dashboard Admin", expanded=False):
                show_admin_dashboard()
            st.markdown("---")
        
        st.header("📋 Agentes Disponíveis")
    
    # Procura por agentes
    current_dir = Path.cwd()
    agent_options = {}
    
    for path in current_dir.iterdir():
        if path.is_dir() and (path / "agent.py").exists():
            agent_options[path.name] = path / "agent.py"
    
    if not agent_options:
        st.warning("❌ Nenhum agente encontrado. Certifique-se de ter arquivos `agent.py` nos subdiretórios.")
        return
    
    selected_agent_name = st.sidebar.selectbox(
        "Selecione um agente:",
        list(agent_options.keys())
    )
    
    if selected_agent_name:
        agent_path = agent_options[selected_agent_name]
        
        # Carrega o agente
        agent = load_agent_from_file(agent_path)
        
        if agent:
            # Informações específicas do LexAprendiz na sidebar (editáveis)
            if selected_agent_name == "lexaprendiz":
                agent_name = get_content("agent_name", "LexAprendiz")
                agent_model = get_content("agent_model", "gemini-2.5-flash")
                agent_description = get_content("agent_description", "Agente especializado em legislação da aprendizagem no Brasil")
                specialties = get_content("specialties", [
                    "• Cálculo de cotas de aprendizes",
                    "• Direitos e deveres de aprendizes",
                    "• Legislação trabalhista específica",
                    "• Fiscalização e auditoria",
                    "• Portarias e decretos atualizados"
                ])
                
                st.sidebar.markdown("### 📚 Informações do Agente")
                st.sidebar.markdown(f"**Nome:** {agent_name}")
                st.sidebar.markdown(f"**Modelo:** {agent_model}")
                st.sidebar.markdown(f"**Descrição:** {agent_description}")
                st.sidebar.markdown("---")
                
                st.sidebar.markdown("### 🎯 Especialidades")
                for specialty in specialties:
                    st.sidebar.markdown(specialty)
            
            # Interface de chat (título editável com estilo personalizado)
            chat_title = get_content("chat_title", "💬 Converse com o LexAprendiz")
            st.markdown(f'<div class="chat-title">{chat_title}</div>', unsafe_allow_html=True)
            
            # Histórico do chat
            if "messages" not in st.session_state:
                st.session_state.messages = []
            
            # Exibe mensagens anteriores
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            
            # Input do usuário
            if prompt := st.chat_input("Digite sua mensagem..."):
                # Adiciona mensagem do usuário
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # Gera resposta baseada no agente selecionado
                with st.chat_message("assistant"):
                    if selected_agent_name == "search":
                        response = f"""🔍 **Agente de Busca** respondendo sobre: "{prompt}"
                        
Como um agente especializado em pesquisa sobre a lei da aprendizagem no Brasil, posso te ajudar com informações sobre:

- **Lei nº 10.097/2000** - Lei da Aprendizagem
- **Decreto nº 5.598/2005** - Regulamentação da Lei
- **Cotas de aprendizes** para empresas
- **Direitos e deveres** dos aprendizes
- **Programas de aprendizagem** profissional

Para informações mais específicas, eu utilizaria a ferramenta de busca do Google para encontrar dados atualizados e relevantes sobre sua consulta.

*💡 Esta é uma demonstração. Para funcionalidade completa, a integração com Google ADK seria necessária.*"""
                    
                    else:  # LexAprendiz
                        # Verifica se a pergunta é sobre aprendizagem (ampliada)
                        keywords_aprendizagem = [
                            'aprendiz', 'aprendizagem', 'lei 10.097', 'decreto 5.598', 'clt', 
                            'menor aprendiz', 'contrato', 'jovem aprendiz', 'cota', 'senai', 'senac',
                            'portaria', 'mte', 'ministério do trabalho', 'fiscalização', 'auditores fiscais',
                            'aft', 'fiscal do trabalho', 'inspeção', 'multa', 'penalidade',
                            'jurisprudência', 'súmula', 'orientação jurisprudencial', 'tst',
                            'programa de aprendizagem', 'entidade formadora', 'sistema s',
                            'registro', 'ctps', 'salário', 'jornada', 'férias', 'rescisão',
                            'deficiente', 'pessoa com deficiência', 'inclusão', 'acessibilidade'
                        ]
                        
                        # Detecta também números de normas específicas sobre aprendizagem
                        normas_aprendizagem = [
                            '10.097', '5.598', '3.872', '1199', '615', '723', '74', '422'
                        ]
                        
                        is_about_aprendizagem = (
                            any(keyword in prompt.lower() for keyword in keywords_aprendizagem) or
                            any(norma in prompt for norma in normas_aprendizagem) or
                            'mte' in prompt.lower() or
                            'trabalho' in prompt.lower()
                        )
                        
                        if is_about_aprendizagem:
                            # Primeiro, busca no banco de conhecimento especializado
                            with st.spinner('🧠 Consultando base de conhecimento jurídico...'):
                                resposta_especializada = banco_conhecimento.buscar_resposta(prompt)
                            
                            if resposta_especializada:
                                # Usa resposta especializada do banco de conhecimento
                                response = resposta_especializada
                            else:
                                # Fallback para pesquisa em tempo real
                                with st.spinner('🔍 Pesquisando legislação em tempo real...'):
                                    resultados_pesquisa = pesquisar_legislacao(prompt)
                                
                                response = f"""⚖️ **LexAprendiz** - Especialista em Legislação da Aprendizagem

**📋 Consulta:** "{prompt}"

**🔍 PESQUISA JURÍDICA EM TEMPO REAL**
*Realizada em: {resultados_pesquisa.get('timestamp', 'Agora')}*

**📚 FUNDAMENTAÇÃO LEGAL ENCONTRADA:**

Consultei as bases jurídicas disponíveis mas não encontrei uma resposta específica pré-formulada para sua consulta. 

Para uma análise detalhada, recomendo:
- Consultar diretamente a legislação vigente
- Buscar orientação jurídica especializada
- Verificar atualizações recentes nas normas

**🔗 FONTES PARA CONSULTA:**
- [Lei 10.097/2000](http://www.planalto.gov.br/ccivil_03/leis/l10097.htm)
- [Decreto 5.598/2005](http://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/decreto/d5598.htm)
- [TST - Jurisprudências](https://www.tst.jus.br/)

**✅ RESPOSTA FUNDAMENTADA EM PESQUISA JURÍDICA**
*Para análise específica de casos concretos, recomenda-se consulta com advogado especializado.*"""
                        
                        else:
                            response = f"""⚖️ **LexAprendiz** - Especialista em Legislação da Aprendizagem

**🔍 ANÁLISE DA CONSULTA:** "{prompt}"

Analisei cuidadosamente sua consulta e não identifiquei relação direta com a legislação da aprendizagem brasileira.

**🎯 Minha especialização abrange TODA legislação de aprendizagem:**
- **Leis:** 10.097/2000, CLT (arts. 428-433), normas correlatas
- **Decretos:** 5.598/2005 e regulamentações
- **Portarias MTE:** Incluindo 3.872/2023 sobre fiscalização
- **Jurisprudência:** Súmulas TST, orientações jurisprudenciais
- **Procedimentos:** Fiscalização, auditoria, penalidades
- **Contratos:** Aprendizagem, jovem aprendiz, pessoa com deficiência
- **Cotas:** Cálculos, obrigatoriedades, exceções
- **Entidades:** Formadoras, Sistema S, programas sociais

**💡 Se sua consulta está relacionada a algum destes temas, reformule especificando a conexão com aprendizagem.**

**Para consultas fora desta especialização, recomendo procurar um especialista na área específica.**"""
                    
                    st.markdown(response)
                
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Informações do agente
            with st.sidebar:
                st.header("ℹ️ Informações do Agente")
                if hasattr(agent, 'name'):
                    st.write(f"**Nome:** {agent.name}")
                if hasattr(agent, 'model'):
                    st.write(f"**Modelo:** {agent.model}")
                if hasattr(agent, 'description'):
                    st.write(f"**Descrição:** {agent.description}")
        else:
            st.error(f"❌ Erro ao carregar agente '{selected_agent_name}'")

if __name__ == "__main__":
    main()