"""
Página: Dashboard principal.

NOTA: este archivo vive en `pages_modules/` (no en `pages/`) a propósito,
porque `pages/` es un nombre reservado por Streamlit para el sistema de
multipágina automático, y en el MVP la navegación se maneja manualmente
desde components/navigation.py para tener control total sobre el flujo
de autenticación. Ver main.py.
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from components.cards import render_kpi_row, render_secondary_kpis
from components.charts import (
    category_breakdown_chart,
    fixed_vs_variable_chart,
    income_vs_expense_chart,
)
from database.repositories.transaction_repository import list_transactions
from services.financial_analysis import build_period_summary
from utils.formatting import month_name


def render(couple_id: str) -> None:
    st.title("🏠 Dashboard financiero")

    today = date.today()
    col1, col2, col3 = st.columns(3)
    with col1:
        year = st.selectbox("Año", options=list(range(today.year - 2, today.year + 1)), index=2)
    with col2:
        month = st.selectbox(
            "Mes",
            options=list(range(1, 13)),
            index=today.month - 1,
            format_func=month_name,
        )
    with col3:
        st.write("")
        st.write("")
        st.caption(f"Mostrando datos de {month_name(month)} {year}")

    transactions = list_transactions(couple_id, year=year, month=month)

    if not transactions:
        st.info(
            "Aún no hay movimientos registrados para este período. "
            "Usa las secciones **Ingresos** y **Gastos** en el menú lateral para empezar."
        )
        return

    summary = build_period_summary(transactions)

    render_kpi_row(summary)
    st.divider()
    render_secondary_kpis(summary)
    st.divider()

    col_left, col_right = st.columns(2)
    with col_left:
        category_breakdown_chart(summary.expense_by_category, "Gastos por categoría")
    with col_right:
        category_breakdown_chart(summary.income_by_category, "Ingresos por categoría")

    fixed_vs_variable_chart(summary.fixed_expense, summary.variable_expense)

    st.caption(
        f"{summary.transaction_count} movimiento(s) registrados en este período. "
        "Los valores se calculan directamente a partir de tus registros."
    )
