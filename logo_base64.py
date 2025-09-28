"""
Logo LexAprendiz - Upload da Logo Oficial
Sistema para carregar a logo real do LexAprendiz
"""

import base64
import streamlit as st

def get_uploaded_logo():
    """Retorna logo carregada (apenas para exibição)"""
    return st.session_state.get('lexaprendiz_logo', None)

def show_logo_uploader():
    """Interface de upload de logo para dashboard administrativo"""
    st.markdown("**Upload da Logo Oficial do LexAprendiz**")
    st.markdown("*Faça upload do logotipo real do LexAprendiz para substituir este espaço*")
    
    # Mostra logo atual se existir
    current_logo = st.session_state.get('lexaprendiz_logo')
    if current_logo:
        st.markdown("**Logo Atual:**")
        st.markdown(
            f'<div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">'
            f'<img src="{current_logo}" style="max-width: 200px; height: auto;">'
            f'</div>',
            unsafe_allow_html=True
        )
        
        if st.button("🗑️ Remover Logo Atual", use_container_width=True):
            if 'lexaprendiz_logo' in st.session_state:
                del st.session_state.lexaprendiz_logo
            st.success("Logo removida com sucesso!")
            st.rerun()
    
    # Uploader sempre visível no dashboard
    uploaded_file = st.file_uploader(
        "Selecione um novo logotipo:", 
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg'],
        help="Limite de 200 MB por arquivo • PNG, JPG, JPEG, GIF, BMP, SVG",
        key="admin_logo_uploader"
    )
    
    if uploaded_file is not None:
        # Processa o upload
        encoded_string = base64.b64encode(uploaded_file.read()).decode()
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg', 
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'svg': 'image/svg+xml'
        }
        
        mime_type = mime_types.get(file_extension, 'image/png')
        logo_data = f"data:{mime_type};base64,{encoded_string}"
        
        # Salva na sessão
        st.session_state.lexaprendiz_logo = logo_data
        
        st.success(f"✅ Logo '{uploaded_file.name}' carregada com sucesso!")
        st.info("A logo foi aplicada automaticamente. Você pode ver o resultado na página principal.")
        
        # Preview da nova logo
        st.markdown("**Preview da Nova Logo:**")
        st.markdown(
            f'<div style="text-align: center; background-color: white; padding: 10px; border-radius: 5px; margin: 10px 0;">'
            f'<img src="{logo_data}" style="max-width: 200px; height: auto;">'
            f'</div>',
            unsafe_allow_html=True
        )
        
        return logo_data
    
    return current_logo

def get_initial_logo():
    """Função para upload inicial (apenas se não há logo)"""
    # Verifica se já existe uma logo salva na sessão
    if 'lexaprendiz_logo' in st.session_state:
        return st.session_state.lexaprendiz_logo
    
    # Só mostra o uploader se não há logo carregada
    st.markdown("### 📎 Upload da Logo Oficial do LexAprendiz")
    st.markdown("*Faça upload do logotipo real do LexAprendiz para substituir este espaço*")
    
    uploaded_file = st.file_uploader(
        "Selecione um logotipo:", 
        type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
        help="Limite de 200 MB por arquivo • PNG, JPG, JPEG, GIF, BMP"
    )
    
    if uploaded_file is not None:
        encoded_string = base64.b64encode(uploaded_file.read()).decode()
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        mime_types = {
            'png': 'image/png',
            'jpg': 'image/jpeg', 
            'jpeg': 'image/jpeg',
            'gif': 'image/gif',
            'bmp': 'image/bmp'
        }
        
        mime_type = mime_types.get(file_extension, 'image/png')
        logo_data = f"data:{mime_type};base64,{encoded_string}"
        
        # Salva na sessão para persistir
        st.session_state.lexaprendiz_logo = logo_data
        return logo_data
    
    return None

# Logo padrão (fundo branco simples) até o upload da logo real
LEXAPRENDIZ_LOGO_PLACEHOLDER = """
data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjE1MCIgdmlld0JveD0iMCAwIDMwMCAxNTAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgPHJlY3Qgd2lkdGg9IjMwMCIgaGVpZ2h0PSIxNTAiIGZpbGw9IndoaXRlIiBzdHJva2U9IiNkZGQiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWRhc2hhcnJheT0iNSw1Ii8+CiAgPHRleHQgeD0iMTUwIiB5PSI3MCIgZm9udC1mYW1pbHk9IkFyaWFsLCBzYW5zLXNlcmlmIiBmb250LXNpemU9IjE2IiBmaWxsPSIjOTk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIj5Mb2dvIExleEFwcmVuZGl6PC90ZXh0PgogIDx0ZXh0IHg9IjE1MCIgeT0iOTAiIGZvbnQtZmFtaWx5PSJBcmlhbCwgc2Fucy1zZXJpZiIgZm9udC1zaXplPSIxMiIgZmlsbD0iIzk5OSIgdGV4dC1hbmNob3I9Im1pZGRsZSI+RmHDp2EgdXBsb2FkIGRhIGxvZ28gcmVhbDwvdGV4dD4KPC9zdmc+
"""