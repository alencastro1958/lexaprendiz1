"""
Sistema de Gerenciamento de Conteúdo Editável do LexAprendiz
Permite ao administrador editar textos da interface
"""

import json
from pathlib import Path
import streamlit as st

# Arquivo para armazenar conteúdos editáveis
CONTENT_FILE = Path("content_settings.json")

def init_content_settings():
    """Inicializa configurações de conteúdo com valores padrão"""
    if not CONTENT_FILE.exists():
        default_content = {
            "main_title": "Conheça o LexAprendiz",
            "main_description": "Obtenha respostas rápidas e precisas para suas perguntas. Nosso Agente LexAprendiz agora usa a tecnologia Gemini 2.5 flash para fornecer esclarecimentos sobre a legislação de forma interativa e com fontes confidenciais.",
            "chat_title": "💬 Converse com o LexAprendiz",
            "sidebar_agents_title": "📋 Agentes Disponíveis",
            "sidebar_user_title": "👤 Usuário",
            "sidebar_admin_title": "🛠️ Dashboard Admin",
            "agent_name": "LexAprendiz",
            "agent_model": "gemini-2.5-flash",
            "agent_description": "Agente especializado em legislação da aprendizagem no Brasil",
            "specialties": [
                "• Cálculo de cotas de aprendizes",
                "• Direitos e deveres de aprendizes", 
                "• Legislação trabalhista específica",
                "• Fiscalização e auditoria",
                "• Portarias e decretos atualizados"
            ],
            "login_title": "🔒 Acesso Restrito",
            "login_subtitle": "Esta área requer autenticação. Faça login ou crie uma conta para continuar.",
            # Configurações de Aparência
            "theme_mode": "light",  # light ou dark
            "main_title_font_size": "2.2em",
            "main_description_font_size": "1.1em",
            "chat_title_font_size": "2.0em",  # Corrigido para estar na lista
            "content_max_width": "800px",
            "description_height": "auto",
            "last_updated": "2025-09-28"
        }
        
        with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_content, f, indent=4, ensure_ascii=False)
    
    return load_content_settings()

def load_content_settings():
    """Carrega configurações de conteúdo do arquivo"""
    try:
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return init_content_settings()

def save_content_settings(content):
    """Salva configurações de conteúdo no arquivo"""
    content["last_updated"] = "2025-09-28"
    with open(CONTENT_FILE, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=4, ensure_ascii=False)

def show_content_editor():
    """Exibe interface de edição de conteúdo para admin"""
    st.markdown("### ✏️ Editor de Conteúdo")
    st.markdown("*Edite os textos que aparecem na interface do LexAprendiz*")
    
    content = load_content_settings()
    
    with st.form("content_editor_form"):
        st.markdown("#### 🏠 Página Principal")
        
        new_main_title = st.text_input(
            "Título Principal:",
            value=content.get("main_title", ""),
            help="Título que aparece após a logo"
        )
        
        new_main_description = st.text_area(
            "Descrição Principal:",
            value=content.get("main_description", ""),
            height=100,
            help="Texto descritivo que aparece abaixo do título"
        )
        
        new_chat_title = st.text_input(
            "Título da Área de Chat:",
            value=content.get("chat_title", ""),
            help="Título da seção de conversa"
        )
        
        st.markdown("#### 📋 Sidebar")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_sidebar_user_title = st.text_input(
                "Título Seção Usuário:",
                value=content.get("sidebar_user_title", "")
            )
            
            new_sidebar_agents_title = st.text_input(
                "Título Agentes Disponíveis:",
                value=content.get("sidebar_agents_title", "")
            )
        
        with col2:
            new_sidebar_admin_title = st.text_input(
                "Título Dashboard Admin:",
                value=content.get("sidebar_admin_title", "")
            )
        
        st.markdown("#### 🤖 Informações do Agente")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_agent_name = st.text_input(
                "Nome do Agente:",
                value=content.get("agent_name", "")
            )
            
            new_agent_model = st.text_input(
                "Modelo do Agente:",
                value=content.get("agent_model", "")
            )
        
        with col2:
            new_agent_description = st.text_area(
                "Descrição do Agente:",
                value=content.get("agent_description", ""),
                height=80
            )
        
        st.markdown("#### 🎯 Especialidades do Agente")
        
        current_specialties = content.get("specialties", [])
        specialty_text = "\n".join(current_specialties)
        
        new_specialties_text = st.text_area(
            "Especialidades (uma por linha, use • no início):",
            value=specialty_text,
            height=120,
            help="Cada linha será uma especialidade. Use • no início de cada linha."
        )
        
        st.markdown("#### 🔐 Tela de Login")
        
        new_login_title = st.text_input(
            "Título da Tela de Login:",
            value=content.get("login_title", "")
        )
        
        new_login_subtitle = st.text_area(
            "Subtítulo da Tela de Login:",
            value=content.get("login_subtitle", ""),
            height=60
        )
        
        st.markdown("#### 🎨 Configurações de Aparência")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_theme_mode = st.selectbox(
                "Tema da Página:",
                options=["light", "dark"],
                index=0 if content.get("theme_mode", "light") == "light" else 1,
                format_func=lambda x: "🌞 Clara" if x == "light" else "🌙 Escura"
            )
            
            width_options = ["600px", "700px", "800px", "900px", "1000px"]
            current_width = content.get("content_max_width", "800px")
            if current_width not in width_options:
                current_width = "800px"
            
            new_content_max_width = st.selectbox(
                "Largura do Conteúdo:",
                options=width_options,
                index=width_options.index(current_width)
            )
        
        with col2:
            title_font_options = ["1.8em", "2.0em", "2.2em", "2.5em", "2.8em", "3.0em"]
            current_title_font = content.get("main_title_font_size", "2.2em")
            if current_title_font not in title_font_options:
                current_title_font = "2.2em"
            
            new_main_title_font_size = st.selectbox(
                "Tamanho Título Principal:",
                options=title_font_options,
                index=title_font_options.index(current_title_font)
            )
            
            desc_font_options = ["0.9em", "1.0em", "1.1em", "1.2em", "1.3em", "1.4em"]
            current_desc_font = content.get("main_description_font_size", "1.1em")
            if current_desc_font not in desc_font_options:
                current_desc_font = "1.1em"
            
            new_main_description_font_size = st.selectbox(
                "Tamanho Descrição:",
                options=desc_font_options,
                index=desc_font_options.index(current_desc_font)
            )
        
        chat_title_options = ["1.5em", "1.8em", "2.0em", "2.2em", "2.5em"]
        current_chat_title_size = content.get("chat_title_font_size", "2.0em")
        # Se o valor atual não estiver na lista, usa o padrão
        if current_chat_title_size not in chat_title_options:
            current_chat_title_size = "2.0em"
        
        new_chat_title_font_size = st.selectbox(
            "Tamanho Título do Chat:",
            options=chat_title_options,
            index=chat_title_options.index(current_chat_title_size)
        )
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            save_button = st.form_submit_button("💾 Salvar Alterações", use_container_width=True)
        
        with col2:
            preview_button = st.form_submit_button("👁️ Pré-visualizar", use_container_width=True)
        
        with col3:
            reset_button = st.form_submit_button("🔄 Restaurar Padrão", use_container_width=True)
        
        if save_button:
            # Salva as alterações
            updated_content = {
                "main_title": new_main_title,
                "main_description": new_main_description,
                "chat_title": new_chat_title,
                "sidebar_user_title": new_sidebar_user_title,
                "sidebar_agents_title": new_sidebar_agents_title,
                "sidebar_admin_title": new_sidebar_admin_title,
                "agent_name": new_agent_name,
                "agent_model": new_agent_model,
                "agent_description": new_agent_description,
                "specialties": [line.strip() for line in new_specialties_text.split('\n') if line.strip()],
                "login_title": new_login_title,
                "login_subtitle": new_login_subtitle,
                # Configurações de Aparência
                "theme_mode": new_theme_mode,
                "main_title_font_size": new_main_title_font_size,
                "main_description_font_size": new_main_description_font_size,
                "chat_title_font_size": new_chat_title_font_size,
                "content_max_width": new_content_max_width,
                "description_height": "auto"
            }
            
            save_content_settings(updated_content)
            st.success("✅ Conteúdo atualizado com sucesso!")
            st.info("🔄 Recarregue a página para ver as alterações.")
            
        elif preview_button:
            # Mostra pré-visualização
            st.markdown("---")
            st.markdown("### 👁️ Pré-visualização das Alterações")
            
            with st.container():
                st.markdown(f"**Título Principal:** {new_main_title}")
                st.markdown(f"**Descrição:** {new_main_description}")
                st.markdown(f"**Título Chat:** {new_chat_title}")
                st.markdown(f"**Nome Agente:** {new_agent_name}")
                st.markdown(f"**Modelo:** {new_agent_model}")
                st.markdown(f"**Descrição Agente:** {new_agent_description}")
                
                st.markdown("**Especialidades:**")
                for specialty in new_specialties_text.split('\n'):
                    if specialty.strip():
                        st.markdown(f"  {specialty.strip()}")
        
        elif reset_button:
            # Restaura configurações padrão
            if st.confirm("Tem certeza que deseja restaurar todas as configurações padrão?"):
                CONTENT_FILE.unlink(missing_ok=True)
                init_content_settings()
                st.success("✅ Configurações restauradas para o padrão!")
                st.rerun()

def get_content(key, default=""):
    """Obtém conteúdo editável por chave"""
    content = load_content_settings()
    return content.get(key, default)

def apply_theme_styles():
    """Aplica estilos de tema (claro/escuro) e configurações de aparência"""
    content = load_content_settings()
    theme_mode = content.get("theme_mode", "light")
    
    # Cores baseadas no tema
    if theme_mode == "dark":
        bg_color = "#0e1117"
        text_color = "#fafafa"
        card_bg = "#262730"
        border_color = "#404040"
        accent_color = "#ff6b6b"
    else:
        bg_color = "#ffffff"
        text_color = "#262730"
        card_bg = "#f8f9fa"
        border_color = "#e0e0e0"
        accent_color = "#194b75"
    
    # CSS personalizado
    custom_css = f"""
    <style>
    /* Tema geral da aplicação */
    .stApp {{
        background-color: {bg_color};
        color: {text_color};
    }}
    
    /* Customização das caixas de texto principais */
    .main-content-box {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 10px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        max-width: {content.get("content_max_width", "800px")};
        margin-left: auto;
        margin-right: auto;
    }}
    
    /* Estilo para títulos principais */
    .main-title {{
        color: {accent_color};
        font-size: {content.get("main_title_font_size", "2.2em")};
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }}
    
    /* Estilo para descrições */
    .main-description {{
        font-size: {content.get("main_description_font_size", "1.1em")};
        color: {text_color};
        line-height: 1.6;
        text-align: center;
        margin-bottom: 25px;
    }}
    
    /* Estilo para título do chat */
    .chat-title {{
        font-size: {content.get("chat_title_font_size", "2.0em")};
        color: {accent_color};
        margin: 30px 0 20px 0;
    }}
    
    /* Personalização da sidebar */
    .css-1d391kg {{
        background-color: {card_bg};
        border-right: 1px solid {border_color};
    }}
    
    /* Botões personalizados */
    .stButton > button {{
        background-color: {accent_color};
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {accent_color}dd;
        transform: translateY(-1px);
    }}
    
    /* Chat input personalizado */
    .stChatInput > div {{
        border: 2px solid {border_color};
        border-radius: 10px;
        background-color: {card_bg};
    }}
    
    /* Mensagens do chat */
    .stChatMessage {{
        background-color: {card_bg};
        border: 1px solid {border_color};
        border-radius: 10px;
        margin: 10px 0;
    }}
    </style>
    """
    
    st.markdown(custom_css, unsafe_allow_html=True)

def get_theme_colors():
    """Retorna cores baseadas no tema atual"""
    content = load_content_settings()
    theme_mode = content.get("theme_mode", "light")
    
    if theme_mode == "dark":
        return {
            "bg_color": "#0e1117",
            "text_color": "#fafafa",
            "card_bg": "#262730",
            "border_color": "#404040",
            "accent_color": "#ff6b6b"
        }
    else:
        return {
            "bg_color": "#ffffff",
            "text_color": "#262730",
            "card_bg": "#f8f9fa",
            "border_color": "#e0e0e0",
            "accent_color": "#194b75"
        }