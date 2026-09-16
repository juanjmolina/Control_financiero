"""
Repositorio para la entidad "pareja/hogar" (couples) y sus miembros.
"""
from __future__ import annotations

from typing import Optional

from database.supabase_client import get_authenticated_client


def get_couple_for_user(user_id: str) -> Optional[dict]:
    """Devuelve la pareja a la que pertenece el usuario (la primera, MVP)."""
    client = get_authenticated_client()
    membership = (
        client.table("couple_members")
        .select("couple_id, role, couples(id, name, created_by)")
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )
    if not membership.data:
        return None
    row = membership.data[0]
    couple = row.get("couples")
    if couple:
        couple["role"] = row["role"]
    return couple


def create_couple(name: str, owner_id: str) -> dict:
    """Crea una pareja nueva y añade al usuario creador como owner."""
    client = get_authenticated_client()
    couple_resp = (
        client.table("couples").insert({"name": name, "created_by": owner_id}).execute()
    )
    couple = couple_resp.data[0]
    client.table("couple_members").insert(
        {"couple_id": couple["id"], "user_id": owner_id, "role": "owner"}
    ).execute()
    return couple


def join_couple(couple_id: str, user_id: str) -> None:
    """Une al usuario actual a una pareja existente por su ID."""
    client = get_authenticated_client()
    client.table("couple_members").insert(
        {"couple_id": couple_id, "user_id": user_id, "role": "member"}
    ).execute()


def get_couple_members(couple_id: str) -> list[dict]:
    client = get_authenticated_client()
    resp = (
        client.table("couple_members")
        .select("user_id, role, profiles(full_name, email)")
        .eq("couple_id", couple_id)
        .execute()
    )
    return resp.data or []
