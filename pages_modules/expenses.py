"""Página: Módulo de gastos (registro y listado, fijos/variables)."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from components.forms import expense_form
from database.repositories.transaction_repository import (
    create_transaction,
    delete_transaction,
    get_categories,
    list_transactions,
)
from utils.formatting import format_currency


def render(couple_id: str, user_id: str) -> None:
    st.title("💳 Gastos")

    categories = get_categories("expense", couple_id)
    if not categories:
        st.warning("No hay categorías de gasto configuradas todavía.")
        return

    with st.expander("➕ Registrar nuevo gasto", expanded=True):
        data = expense_form(categories)
        if data:
            create_transaction(
                couple_id=couple_id,
                user_id=user_id,
                type_="expense",
                **data,
            )
            st.success("Gasto registrado correctamente.")
            st.rerun()

    st.divider()
    st.subheader("Historial de gastos")

    tab_all, tab_fixed, tab_variable = st.tabs(["Todos", "Fijos", "Variables"])

    transactions = list_transactions(couple_id, type_="expense")
    if not transactions:
        st.info("No hay gastos registrados todavía.")
        return

    def _render_table(rows: list[dict]) -> None:
        if not rows:
            st.info("No hay gastos en esta categoría.")
            return
        total = sum(t["amount"] for t in rows)
        st.metric("Total", format_currency(total))
        df = pd.DataFrame(rows)[
            ["transaction_date", "category_name", "description", "amount", "fixed_variable", "scope", "payment_method"]
        ]
        df.columns = ["Fecha", "Categoría", "Descripción", "Valor", "Fijo/Variable", "Tipo", "Método de pago"]
        df["Valor"] = df["Valor"].apply(format_currency)
        df["Tipo"] = df["Tipo"].map({"personal": "Personal", "shared": "Compartido"})
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab_all:
        _render_table(transactions)
    with tab_fixed:
        _render_table([t for t in transactions if t.get("fixed_variable") == "fijo"])
    with tab_variable:
        _render_table([t for t in transactions if t.get("fixed_variable") == "variable"])

    with st.expander("🗑️ Eliminar un gasto"):
        options = {
            f"{t['transaction_date']} · {t['category_name']} · {format_currency(t['amount'])}": t["id"]
            for t in transactions
        }
        selected_label = st.selectbox("Selecciona el movimiento a eliminar", options.keys())
        if st.button("Eliminar movimiento seleccionado", type="secondary"):
            delete_transaction(options[selected_label])
            st.success("Movimiento eliminado.")
            st.rerun()
