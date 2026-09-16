"""
Tarjetas de indicadores (KPIs) para el dashboard principal.
"""
from __future__ import annotations

import streamlit as st

from utils.formatting import format_currency, format_percentage


def render_kpi_row(summary) -> None:
    """Fila con los 4 indicadores principales del período."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Ingresos", format_currency(summary.total_income))
    with col2:
        st.metric("💳 Egresos", format_currency(summary.total_expense))
    with col3:
        delta_color = "normal" if summary.balance >= 0 else "inverse"
        st.metric("⚖️ Balance", format_currency(summary.balance))
    with col4:
        st.metric("📈 Tasa de ahorro", format_percentage(summary.savings_rate))


def render_secondary_kpis(summary) -> None:
    """Fila con el desglose fijo/variable y personal/compartido."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏠 Gastos fijos", format_currency(summary.fixed_expense))
    with col2:
        st.metric("🛍️ Gastos variables", format_currency(summary.variable_expense))
    with col3:
        st.metric("🤝 Gastos compartidos", format_currency(summary.shared_expense))
    with col4:
        st.metric("👤 Gastos personales", format_currency(summary.personal_expense))
