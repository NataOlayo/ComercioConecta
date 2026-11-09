"""
Componente de barra lateral para el frontend de ComercioConecta
"""
import streamlit as st
from datetime import datetime


def render_sidebar():
    """Renderiza la barra lateral con controles y información"""
    st.header("🎯 Panel de Control")

    # Show current stats
    if st.session_state.get('last_update'):
        st.caption(f"Última actualización: {st.session_state.last_update}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📦 Productos", len(st.session_state.get('products', [])))
    with col2:
        st.metric("🔗 Relaciones", len(st.session_state.get('relationships', [])))

    # Getting started guide
    with st.expander("📖 Guía de inicio rápido", expanded=not st.session_state.get('products', [])):
        st.markdown("""
        **Para comenzar:**
        1. **Agregue productos** usando el formulario abajo
        2. **Conéctelos** creando relaciones entre ellos
        3. **Explore** descubriendo qué se compra con qué
        4. **Analice** los componentes para ver grupos de productos

        💡 *Tip: Empiece con productos comunes como Leche, Pan, Huevos*
        """)