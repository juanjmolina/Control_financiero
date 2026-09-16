"""
Validadores de entrada, usados en los formularios (components/forms.py)
antes de enviar datos a la base de datos.
"""
from __future__ import annotations

import re
from datetime import date

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_REGEX.match(email or ""))


def is_valid_password(password: str) -> tuple[bool, str]:
    if not password or len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    return True, ""


def is_valid_amount(amount) -> tuple[bool, str]:
    try:
        value = float(amount)
    except (TypeError, ValueError):
        return False, "El valor debe ser numérico."
    if value <= 0:
        return False, "El valor debe ser mayor a cero."
    return True, ""


def is_valid_date(value: date) -> tuple[bool, str]:
    if value is None:
        return False, "La fecha es obligatoria."
    if value > date.today():
        return False, "La fecha no puede ser futura."
    return True, ""


def is_valid_category(category_name: str) -> tuple[bool, str]:
    if not category_name or not category_name.strip():
        return False, "Debes seleccionar una categoría."
    return True, ""
