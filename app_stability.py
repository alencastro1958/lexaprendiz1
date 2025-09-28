"""
Sistema de Estabilidade da Aplicação
Previne conflitos de DOM e gerencia reruns de forma segura
"""
import streamlit as st
import time
from typing import Optional, Callable

class AppStabilityManager:
    """Gerencia a estabilidade da aplicação prevenindo conflitos"""
    
    def __init__(self):
        self.last_rerun = 0
        self.rerun_cooldown = 1.0  # 1 segundo entre reruns
        
    def safe_rerun(self, delay: float = 0.5):
        """Executa rerun de forma segura com cooldown"""
        current_time = time.time()
        
        if current_time - self.last_rerun < self.rerun_cooldown:
            st.info("🕐 Aguarde um momento para processar a alteração...")
            return False
            
        if delay > 0:
            time.sleep(delay)
            
        self.last_rerun = current_time
        st.rerun()
        return True
    
    def safe_state_update(self, key: str, value, auto_rerun: bool = False):
        """Atualiza session state de forma segura"""
        try:
            st.session_state[key] = value
            
            if auto_rerun:
                st.info(f"✅ {key} atualizado com sucesso!")
                st.info("🔄 Recarregue a página para ver as mudanças.")
                st.balloons()
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao atualizar {key}: {str(e)}")
            return False
    
    def safe_logout(self):
        """Executa logout de forma segura"""
        try:
            # Remove chaves de autenticação
            auth_keys = ['logged_in', 'user_data', 'user_email', 
                        'user_name', 'user_type', 'show_register']
            
            for key in auth_keys:
                if key in st.session_state:
                    del st.session_state[key]
            
            st.success("🚪 Logout realizado com sucesso!")
            st.info("🔄 Recarregue a página para continuar.")
            st.balloons()
            st.stop()
            
        except Exception as e:
            st.error(f"Erro no logout: {str(e)}")
            return False
    
    def safe_theme_change(self, new_theme: str):
        """Muda tema de forma segura"""
        try:
            from content_manager import load_content_settings, save_content_settings
            
            content = load_content_settings()
            content["theme_mode"] = new_theme
            save_content_settings(content)
            
            st.success(f"🎨 Tema alterado para: {new_theme}")
            st.info("🔄 Recarregue a página para aplicar o novo tema.")
            st.balloons()
            
            return True
            
        except Exception as e:
            st.error(f"Erro ao alterar tema: {str(e)}")
            return False
    
    def prevent_dom_conflicts(self):
        """Previne conflitos de DOM"""
        # Adiciona estilo CSS para prevenir conflitos
        st.markdown("""
        <style>
            /* Previne conflitos de DOM */
            .stApp {
                transition: none !important;
            }
            
            .stButton button {
                transition: all 0.2s ease !important;
            }
            
            /* Estabiliza componentes durante updates */
            .element-container {
                position: relative !important;
            }
            
            /* Previne flicker durante mudanças */
            .stSelectbox, .stTextInput, .stTextArea {
                transition: none !important;
            }
        </style>
        """, unsafe_allow_html=True)

# Instância global do gerenciador
stability_manager = AppStabilityManager()

def get_stability_manager():
    """Retorna instância do gerenciador de estabilidade"""
    return stability_manager

def safe_rerun(delay: float = 0.5):
    """Função helper para rerun seguro"""
    return stability_manager.safe_rerun(delay)

def safe_state_update(key: str, value, auto_rerun: bool = False):
    """Função helper para update seguro do state"""
    return stability_manager.safe_state_update(key, value, auto_rerun)

def safe_logout():
    """Função helper para logout seguro"""
    return stability_manager.safe_logout()

def safe_theme_change(new_theme: str):
    """Função helper para mudança segura de tema"""
    return stability_manager.safe_theme_change(new_theme)

def prevent_dom_conflicts():
    """Função helper para prevenir conflitos de DOM"""
    return stability_manager.prevent_dom_conflicts()

def check_app_health():
    """Verifica saúde geral da aplicação"""
    try:
        # Verifica session state
        if not hasattr(st, 'session_state'):
            return False, "Session state não disponível"
        
        # Verifica componentes críticos
        critical_imports = ['streamlit', 'json', 'hashlib']
        for module in critical_imports:
            try:
                __import__(module)
            except ImportError:
                return False, f"Módulo crítico não encontrado: {module}"
        
        return True, "Aplicação saudável"
        
    except Exception as e:
        return False, f"Erro na verificação: {str(e)}"