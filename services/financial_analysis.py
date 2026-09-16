"""
Servicio de análisis financiero. Orquesta las funciones puras de
utils/calculations.py sobre un conjunto de transacciones ya cargado,
para producir el resumen que consume el dashboard.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from utils.calculations import (
    calculate_balance,
    calculate_savings_rate,
    group_by_category,
    group_by_month,
    group_by_user,
    total_by_fixed_variable,
    total_by_scope,
    total_by_type,
)


@dataclass
class PeriodSummary:
    total_income: float = 0.0
    total_expense: float = 0.0
    balance: float = 0.0
    savings_rate: float = 0.0
    fixed_expense: float = 0.0
    variable_expense: float = 0.0
    shared_expense: float = 0.0
    personal_expense: float = 0.0
    income_by_category: dict = field(default_factory=dict)
    expense_by_category: dict = field(default_factory=dict)
    expense_by_user: dict = field(default_factory=dict)
    income_by_user: dict = field(default_factory=dict)
    monthly_series: dict = field(default_factory=dict)
    transaction_count: int = 0


def build_period_summary(transactions: list[dict]) -> PeriodSummary:
    """
    Construye el resumen financiero de un conjunto de transacciones
    (ya filtradas por período/usuario en la capa de repositorio).
    No se conecta a la base de datos: es pura composición de cálculos.
    """
    total_income = total_by_type(transactions, "income")
    total_expense = total_by_type(transactions, "expense")

    return PeriodSummary(
        total_income=total_income,
        total_expense=total_expense,
        balance=calculate_balance(total_income, total_expense),
        savings_rate=calculate_savings_rate(total_income, total_expense),
        fixed_expense=total_by_fixed_variable(transactions, "fijo"),
        variable_expense=total_by_fixed_variable(transactions, "variable"),
        shared_expense=total_by_scope(transactions, "expense", "shared"),
        personal_expense=total_by_scope(transactions, "expense", "personal"),
        income_by_category=group_by_category(transactions, "income"),
        expense_by_category=group_by_category(transactions, "expense"),
        expense_by_user=group_by_user(transactions, "expense"),
        income_by_user=group_by_user(transactions, "income"),
        monthly_series=group_by_month(transactions),
        transaction_count=len(transactions),
    )
