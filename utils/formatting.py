"""
Funciones de formato para presentar valores en la interfaz.
"""
from __future__ import annotations

MONTH_NAMES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


def format_currency(value: float, currency: str = "COP") -> str:
    """Formatea un número como moneda, con separador de miles con punto
    (estilo colombiano) y sin decimales para montos grandes."""
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0
    symbol = "$" if currency == "COP" else f"{currency} "
    formatted = f"{value:,.0f}".replace(",", ".")
    return f"{symbol}{formatted}"


def format_percentage(value: float) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        value = 0.0
    return f"{value:.1f}%"


def month_name(month: int) -> str:
    return MONTH_NAMES_ES.get(month, str(month))


def month_label(year: int, month: int) -> str:
    return f"{month_name(month)} {year}"
