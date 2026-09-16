"""
Repositorio de transacciones (ingresos y gastos).

Todas las funciones asumen que las políticas RLS de Supabase ya
restringen el acceso a la pareja del usuario autenticado; aun así,
siempre filtramos explícitamente por couple_id como defensa en
profundidad y para mantener las consultas legibles.
"""
from __future__ import annotations

from datetime import date
from typing import Optional

from database.supabase_client import get_authenticated_client

TABLE = "transactions"


def create_transaction(
    *,
    couple_id: str,
    user_id: str,
    type_: str,  # "income" | "expense"
    scope: str,  # "personal" | "shared"
    category_name: str,
    amount: float,
    transaction_date: date,
    fixed_variable: Optional[str] = None,
    subcategory: Optional[str] = None,
    description: Optional[str] = None,
    payment_method: str = "otro",
    is_recurring: bool = False,
    notes: Optional[str] = None,
) -> dict:
    client = get_authenticated_client()
    payload = {
        "couple_id": couple_id,
        "user_id": user_id,
        "type": type_,
        "scope": scope,
        "category_name": category_name,
        "amount": amount,
        "transaction_date": transaction_date.isoformat(),
        "fixed_variable": fixed_variable,
        "subcategory": subcategory,
        "description": description,
        "payment_method": payment_method,
        "is_recurring": is_recurring,
        "notes": notes,
    }
    resp = client.table(TABLE).insert(payload).execute()
    return resp.data[0]


def list_transactions(
    couple_id: str,
    *,
    type_: Optional[str] = None,
    year: Optional[int] = None,
    month: Optional[int] = None,
    user_id: Optional[str] = None,
) -> list[dict]:
    client = get_authenticated_client()
    query = (
        client.table(TABLE)
        .select("*")
        .eq("couple_id", couple_id)
        .is_("deleted_at", "null")
        .order("transaction_date", desc=True)
    )
    if type_:
        query = query.eq("type", type_)
    if year:
        query = query.eq("year", year)
    if month:
        query = query.eq("month", month)
    if user_id:
        query = query.eq("user_id", user_id)
    resp = query.execute()
    return resp.data or []


def update_transaction(transaction_id: str, fields: dict) -> dict:
    client = get_authenticated_client()
    resp = client.table(TABLE).update(fields).eq("id", transaction_id).execute()
    return resp.data[0] if resp.data else {}


def delete_transaction(transaction_id: str) -> None:
    """Borrado lógico: marca deleted_at en lugar de eliminar la fila."""
    from datetime import datetime, timezone

    client = get_authenticated_client()
    client.table(TABLE).update(
        {"deleted_at": datetime.now(timezone.utc).isoformat()}
    ).eq("id", transaction_id).execute()


def get_categories(kind: str, couple_id: str) -> list[dict]:
    """kind: 'income' o 'expense'. Devuelve categorías del sistema + propias."""
    client = get_authenticated_client()
    table = "income_categories" if kind == "income" else "expense_categories"
    resp = (
        client.table(table)
        .select("*")
        .or_(f"couple_id.is.null,couple_id.eq.{couple_id}")
        .order("name")
        .execute()
    )
    return resp.data or []
