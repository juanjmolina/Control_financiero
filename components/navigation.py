"""
Navegación lateral de la aplicación. En el MVP solo están activas
las páginas de Fase 1; el resto se muestra deshabilitado como
adelanto del roadmap, para que la pareja vea hacia dónde va creciendo.
"""
from __future__ import annotations

import streamlit as st

MVP_PAGES = [
    ("🏠 Dashboard", "dashboard"),
    ("💰 Ingresos", "income"),
    ("💳 Gastos", "expenses"),
]

UPCOMING_PAGES = [
    "📊 Presupuesto",
    "🚨 Fondo de emergencia",
    "🎯 Mis proyectos",
    "🏦 Deudas",
    "🏠 Patrimonio",
    "📈 Reportes",
    "🔮 Proyecciones",
    "🤖 Asistente financiero",
]


def render_sidebar(user_full_name: str, couple_name: str) -> str:
    """Dibuja la barra lateral y devuelve la clave de la página elegida."""
    with st.sidebar:
        st.markdown(f"### 💑 {couple_name}")
        st.caption(f"Sesión: {user_full_name}")
        st.divider()

        current_page = st.session_state.get("current_page", "dashboard")

        for label, key in MVP_PAGES:
            button_type = "primary" if current_page == key else "secondary"
            if st.button(label, use_container_width=True, type=button_type, key=f"nav_{key}"):
                st.session_state["current_page"] = key
                current_page = key

        st.divider()
        st.caption("Próximamente")
        for label in UPCOMING_PAGES:
            st.markdown(f"<span style='color:gray'>{label}</span>", unsafe_allow_html=True)

        st.divider()
        if st.button("🚪 Cerrar sesión", use_container_width=True):
            st.session_state["logout_requested"] = True

    return current_page
