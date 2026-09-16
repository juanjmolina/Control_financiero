"""
Configuración centralizada de la aplicación.

Las credenciales NUNCA se escriben directamente en el código.
Se obtienen, en este orden de prioridad:
    1. st.secrets (Streamlit Cloud / .streamlit/secrets.toml)
    2. Variables de entorno (.env vía python-dotenv)
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

try:
    import streamlit as st
    _HAS_STREAMLIT_SECRETS = hasattr(st, "secrets")
except Exception:  # pragma: no cover
    _HAS_STREAMLIT_SECRETS = False


def _get_setting(key: str, default: str | None = None) -> str | None:
    """Busca una variable primero en st.secrets, luego en el entorno."""
    if _HAS_STREAMLIT_SECRETS:
        try:
            if key in st.secrets:
                return st.secrets[key]
        except Exception:
            pass
    return os.getenv(key, default)


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_anon_key: str
    app_name: str = "Finanzas en Pareja"
    default_currency: str = "COP"

    def validate(self) -> None:
        missing = [
            name
            for name, value in [
                ("SUPABASE_URL", self.supabase_url),
                ("SUPABASE_ANON_KEY", self.supabase_anon_key),
            ]
            if not value
        ]
        if missing:
            raise RuntimeError(
                "Faltan variables de configuración requeridas: "
                f"{', '.join(missing)}. Defínelas en .streamlit/secrets.toml "
                "o en un archivo .env (ver .env.example)."
            )


def get_settings() -> Settings:
    settings = Settings(
        supabase_url=_get_setting("SUPABASE_URL", ""),
        supabase_anon_key=_get_setting("SUPABASE_ANON_KEY", ""),
        app_name=_get_setting("APP_NAME", "Finanzas en Pareja"),
        default_currency=_get_setting("DEFAULT_CURRENCY", "COP"),
    )
    settings.validate()
    return settings
