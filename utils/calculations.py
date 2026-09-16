"""
Funciones puras de cálculo financiero. Sin efectos secundarios,
sin llamadas a base de datos: reciben datos y devuelven números.
Esto facilita las pruebas unitarias (ver tests/).
"""
from __future__ import annotations

from typing import Iterable


def total_by_type(transactions: Iterable[dict], type_: str) -> float:
    """Suma el campo 'amount' de las transacciones de un tipo dado."""
    return round(sum(t["amount"] for t in transactions if t["type"] == type_), 2)


def calculate_balance(total_income: float, total_expense: float) -> float:
    """Balance neto = ingresos - egresos."""
    return round(total_income - total_expense, 2)


def calculate_savings_rate(total_income: float, total_expense: float) -> float:
    """
    Tasa de ahorro (%) = (ingresos - egresos) / ingresos * 100.
    Si no hay ingresos, se devuelve 0 para evitar división por cero.
    """
    if total_income <= 0:
        return 0.0
    savings = total_income - total_expense
    return round((savings / total_income) * 100, 2)


def total_by_fixed_variable(transactions: Iterable[dict], kind: str) -> float:
    """kind: 'fijo' o 'variable'. Solo considera gastos (type='expense')."""
    return round(
        sum(
            t["amount"]
            for t in transactions
            if t["type"] == "expense" and t.get("fixed_variable") == kind
        ),
        2,
    )


def total_by_scope(transactions: Iterable[dict], type_: str, scope: str) -> float:
    """Suma por 'personal' o 'shared', para un tipo dado de transacción."""
    return round(
        sum(
            t["amount"]
            for t in transactions
            if t["type"] == type_ and t.get("scope") == scope
        ),
        2,
    )


def group_by_category(transactions: Iterable[dict], type_: str) -> dict[str, float]:
    """Devuelve {categoria: total} para un tipo de transacción."""
    totals: dict[str, float] = {}
    for t in transactions:
        if t["type"] != type_:
            continue
        cat = t.get("category_name", "Sin categoría")
        totals[cat] = round(totals.get(cat, 0) + t["amount"], 2)
    return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))


def group_by_user(transactions: Iterable[dict], type_: str) -> dict[str, float]:
    """Devuelve {user_id: total} para un tipo de transacción."""
    totals: dict[str, float] = {}
    for t in transactions:
        if t["type"] != type_:
            continue
        uid = t.get("user_id", "desconocido")
        totals[uid] = round(totals.get(uid, 0) + t["amount"], 2)
    return totals


def group_by_month(transactions: Iterable[dict]) -> dict[str, dict[str, float]]:
    """
    Devuelve {"YYYY-MM": {"income": x, "expense": y}} para construir
    series de tiempo (ingresos vs egresos por mes).
    """
    series: dict[str, dict[str, float]] = {}
    for t in transactions:
        key = f"{t['year']:04d}-{t['month']:02d}"
        bucket = series.setdefault(key, {"income": 0.0, "expense": 0.0})
        bucket[t["type"]] = round(bucket[t["type"]] + t["amount"], 2)
    return dict(sorted(series.items()))
