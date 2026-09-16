"""
Pruebas unitarias de utils/calculations.py.
Ejecutar con: pytest desde la carpeta app/
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from utils.calculations import (  # noqa: E402
    calculate_balance,
    calculate_savings_rate,
    group_by_category,
    total_by_fixed_variable,
    total_by_scope,
    total_by_type,
)

SAMPLE_TRANSACTIONS = [
    {"type": "income", "amount": 4_000_000, "category_name": "Salario", "scope": "personal", "fixed_variable": None},
    {"type": "income", "amount": 800_000, "category_name": "Comisiones", "scope": "personal", "fixed_variable": None},
    {"type": "expense", "amount": 1_200_000, "category_name": "Arriendo", "scope": "shared", "fixed_variable": "fijo"},
    {"type": "expense", "amount": 650_000, "category_name": "Alimentación", "scope": "shared", "fixed_variable": "variable"},
    {"type": "expense", "amount": 300_000, "category_name": "Ocio", "scope": "personal", "fixed_variable": "variable"},
]


def test_total_by_type_income():
    assert total_by_type(SAMPLE_TRANSACTIONS, "income") == 4_800_000


def test_total_by_type_expense():
    assert total_by_type(SAMPLE_TRANSACTIONS, "expense") == 2_150_000


def test_calculate_balance():
    assert calculate_balance(4_800_000, 2_150_000) == 2_650_000


def test_calculate_savings_rate():
    rate = calculate_savings_rate(4_800_000, 2_150_000)
    assert round(rate, 2) == 55.21


def test_calculate_savings_rate_no_income():
    assert calculate_savings_rate(0, 500) == 0.0


def test_total_by_fixed_variable():
    assert total_by_fixed_variable(SAMPLE_TRANSACTIONS, "fijo") == 1_200_000
    assert total_by_fixed_variable(SAMPLE_TRANSACTIONS, "variable") == 950_000


def test_total_by_scope():
    assert total_by_scope(SAMPLE_TRANSACTIONS, "expense", "shared") == 1_850_000
    assert total_by_scope(SAMPLE_TRANSACTIONS, "expense", "personal") == 300_000


def test_group_by_category():
    result = group_by_category(SAMPLE_TRANSACTIONS, "expense")
    assert result == {
        "Arriendo": 1_200_000,
        "Alimentación": 650_000,
        "Ocio": 300_000,
    }
