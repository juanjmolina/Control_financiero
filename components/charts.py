"""
Gráficos reutilizables construidos con Plotly, usados en el dashboard
y (en fases futuras) en el módulo de reportes.
"""
from __future__ import annotations

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def income_vs_expense_chart(monthly_series: dict) -> None:
    """Barras agrupadas: ingresos vs egresos por mes."""
    if not monthly_series:
        st.info("Aún no hay suficientes datos para graficar ingresos vs egresos.")
        return

    months = list(monthly_series.keys())
    income_values = [monthly_series[m]["income"] for m in months]
    expense_values = [monthly_series[m]["expense"] for m in months]

    fig = go.Figure()
    fig.add_bar(name="Ingresos", x=months, y=income_values, marker_color="#2E8B57")
    fig.add_bar(name="Egresos", x=months, y=expense_values, marker_color="#C0392B")
    fig.update_layout(
        barmode="group",
        title="Ingresos vs Egresos por mes",
        xaxis_title="Mes",
        yaxis_title="Valor",
        legend_title="",
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)


def category_breakdown_chart(category_totals: dict, title: str) -> None:
    """Gráfico de dona: distribución de gastos o ingresos por categoría."""
    if not category_totals:
        st.info(f"Aún no hay datos para '{title}'.")
        return

    fig = px.pie(
        names=list(category_totals.keys()),
        values=list(category_totals.values()),
        hole=0.45,
        title=title,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def fixed_vs_variable_chart(fixed: float, variable: float) -> None:
    """Barras horizontales: gastos fijos vs variables."""
    if fixed == 0 and variable == 0:
        st.info("Aún no hay gastos registrados para comparar fijos vs variables.")
        return

    fig = go.Figure(
        go.Bar(
            x=[fixed, variable],
            y=["Fijos", "Variables"],
            orientation="h",
            marker_color=["#34495E", "#F39C12"],
        )
    )
    fig.update_layout(title="Gastos fijos vs variables", height=300)
    st.plotly_chart(fig, use_container_width=True)
