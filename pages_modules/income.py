"""Página: Módulo de ingresos (registro y listado)."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from components.forms import income_form
from database.repositories.transaction_repository import (
    create_transaction,
    delete_transaction,
    get_categories,
    list_transactions,
)
from utils.formatting import format_currency


def render(couple_id: str, user_id: str) -> None:
    st.title("💰 Ingresos")

    categories = get_categories("income", couple_id)
    if not categories:
        st.warning("No hay categorías de ingreso configuradas todavía.")
        return

    with st.expander("➕ Registrar nuevo ingreso", expanded=True):
        data = income_form(categories)
        if data:
            create_transaction(
                couple_id=couple_id,
                user_id=user_id,
                type_="income",
                **data,
            )
            st.success("Ingreso registrado correctamente.")
            st.rerun()

    st.divider()
    st.subheader("Historial de ingresos")

    transactions = list_transactions(couple_id, type_="income")
    if not transactions:
        st.info("No hay ingresos registrados todavía.")
        return

    total = sum(t["amount"] for t in transactions)
    st.metric("Total acumulado", format_currency(total))

    df = pd.DataFrame(transactions)[
        ["transaction_date", "category_name", "description", "amount", "scope", "is_recurring"]
    ]
    df.columns = ["Fecha", "Categoría", "Descripción", "Valor", "Tipo", "Recurrente"]
    df["Valor"] = df["Valor"].apply(format_currency)
    df["Tipo"] = df["Tipo"].map({"personal": "Personal", "shared": "Compartido"})
    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.expander("🗑️ Eliminar un ingreso"):
        options = {
            f"{t['transaction_date']} · {t['category_name']} · {format_currency(t['amount'])}": t["id"]
            for t in transactions
        }
        selected_label = st.selectbox("Selecciona el movimiento a eliminar", options.keys())
        if st.button("Eliminar movimiento seleccionado", type="secondary"):
            delete_transaction(options[selected_label])
            st.success("Movimiento eliminado.")
            st.rerun()
