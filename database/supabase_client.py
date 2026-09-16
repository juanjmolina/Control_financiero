"""
Cliente Supabase para toda la aplicación.

Se expone una única función `get_client()` cacheada con st.cache_resource
para reutilizar la conexión entre reruns de Streamlit, y una función
`get_authenticated_client()` que adjunta la sesión del usuario logueado
para que las políticas RLS de Postgres puedan identificar a `auth.uid()`.
"""
from __future__ import annotations

import streamlit as st
from supabase import Client, create_client

from config.settings import get_settings


@st.cache_resource(show_spinner=False)
def get_client() -> Client:
    """Cliente base de Supabase (sin sesión de usuario)."""
    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


def get_authenticated_client() -> Client:
    """
    Devuelve el cliente de Supabase con la sesión del usuario actual
    adjunta, de modo que las consultas respeten RLS como ese usuario.

    Requiere que `st.session_state["auth_session"]` exista (se guarda
    al iniciar sesión, ver database/repositories/auth_repository.py).
    """
    client = get_client()
    session = st.session_state.get("auth_session")
    if session is not None:
        client.postgrest.auth(session.access_token)
    return client
