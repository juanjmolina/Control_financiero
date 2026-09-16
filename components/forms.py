"""
Formularios reutilizables para el registro de ingresos y gastos.
Devuelven un diccionario con los datos validados, o None si el
usuario aún no ha enviado el formulario o si hay errores.
"""
from __future__ import annotations

from datetime import date

import streamlit as st

from utils.validators import is_valid_amount, is_valid_category, is_valid_date

PAYMENT_METHODS = {
    "efectivo": "Efectivo",
    "cuenta_bancaria": "Cuenta bancaria",
    "tarjeta_debito": "Tarjeta débito",
    "tarjeta_credito": "Tarjeta crédito",
    "transferencia": "Transferencia",
    "otro": "Otro",
}


def income_form(categories: list[dict]) -> dict | None:
    with st.form("income_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Categoría",
                options=[c["name"] for c in categories],
                key="income_category",
            )
            amount = st.number_input("Valor", min_value=0, step=1000, key="income_amount")
            tx_date = st.date_input("Fecha", value=date.today(), key="income_date")
        with col2:
            scope = st.radio("Tipo", ["personal", "shared"], format_func=lambda v: "Personal" if v == "personal" else "Compartido", key="income_scope")
            is_recurring = st.checkbox("¿Es un ingreso recurrente?", key="income_recurring")
            description = st.text_input("Descripción (opcional)", key="income_description")

        submitted = st.form_submit_button("Guardar ingreso", type="primary", use_container_width=True)

        if not submitted:
            return None

        valid_amount, amount_msg = is_valid_amount(amount)
        valid_category, category_msg = is_valid_category(category)
        valid_date, date_msg = is_valid_date(tx_date)

        errors = [m for ok, m in [(valid_amount, amount_msg), (valid_category, category_msg), (valid_date, date_msg)] if not ok]
        if errors:
            for e in errors:
                st.error(e)
            return None

        return {
            "category_name": category,
            "amount": float(amount),
            "transaction_date": tx_date,
            "scope": scope,
            "is_recurring": is_recurring,
            "description": description or None,
        }


def expense_form(categories: list[dict]) -> dict | None:
    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            category_obj = st.selectbox(
                "Categoría",
                options=categories,
                format_func=lambda c: c["name"],
                key="expense_category",
            )
            amount = st.number_input("Valor", min_value=0, step=1000, key="expense_amount")
            tx_date = st.date_input("Fecha", value=date.today(), key="expense_date")
            payment_method = st.selectbox(
                "Método de pago",
                options=list(PAYMENT_METHODS.keys()),
                format_func=lambda k: PAYMENT_METHODS[k],
                key="expense_payment_method",
            )
        with col2:
            scope = st.radio("Tipo", ["personal", "shared"], format_func=lambda v: "Personal" if v == "personal" else "Compartido", key="expense_scope")
            is_recurring = st.checkbox("¿Es un gasto recurrente?", key="expense_recurring")
            description = st.text_input("Descripción (opcional)", key="expense_description")

        submitted = st.form_submit_button("Guardar gasto", type="primary", use_container_width=True)

        if not submitted:
            return None

        valid_amount, amount_msg = is_valid_amount(amount)
        valid_date, date_msg = is_valid_date(tx_date)

        errors = [m for ok, m in [(valid_amount, amount_msg), (valid_date, date_msg)] if not ok]
        if errors:
            for e in errors:
                st.error(e)
            return None

        return {
            "category_name": category_obj["name"],
            "fixed_variable": category_obj["fixed_variable"],
            "amount": float(amount),
            "transaction_date": tx_date,
            "payment_method": payment_method,
            "scope": scope,
            "is_recurring": is_recurring,
            "description": description or None,
        }
