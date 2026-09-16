"""
Repositorio de autenticación. Encapsula todas las llamadas a
Supabase Auth (registro, login, logout, recuperación de contraseña)
y la creación del perfil asociado en public.profiles.
"""
from __future__ import annotations

from dataclasses import dataclass

from database.supabase_client import get_client


@dataclass
class AuthResult:
    success: bool
    message: str
    user_id: str | None = None
    session: object | None = None


def sign_up(email: str, password: str, full_name: str) -> AuthResult:
    client = get_client()
    try:
        response = client.auth.sign_up({"email": email, "password": password})
        user = response.user
        if user is None:
            return AuthResult(False, "No se pudo crear el usuario. Intenta de nuevo.")

        # Crear el perfil asociado. Si hay sesión (confirmación de email
        # deshabilitada), insertamos autenticados; si no, se completará
        # en el primer login.
        if response.session is not None:
            client.postgrest.auth(response.session.access_token)
            client.table("profiles").insert(
                {"id": user.id, "full_name": full_name, "email": email}
            ).execute()

        return AuthResult(
            True,
            "Cuenta creada. Revisa tu correo si se requiere confirmación.",
            user_id=user.id,
            session=response.session,
        )
    except Exception as exc:  # noqa: BLE001
        return AuthResult(False, f"Error al registrar: {exc}")


def sign_in(email: str, password: str) -> AuthResult:
    client = get_client()
    try:
        response = client.auth.sign_in_with_password(
            {"email": email, "password": password}
        )
        if response.session is None or response.user is None:
            return AuthResult(False, "Credenciales inválidas.")

        # Asegura que exista el perfil (por si el registro no lo creó)
        client.postgrest.auth(response.session.access_token)
        existing = (
            client.table("profiles")
            .select("id")
            .eq("id", response.user.id)
            .execute()
        )
        if not existing.data:
            client.table("profiles").insert(
                {
                    "id": response.user.id,
                    "full_name": response.user.email.split("@")[0],
                    "email": response.user.email,
                }
            ).execute()

        return AuthResult(True, "Bienvenido de nuevo.", user_id=response.user.id, session=response.session)
    except Exception as exc:  # noqa: BLE001
        return AuthResult(False, f"No se pudo iniciar sesión: {exc}")


def sign_out(session_access_token: str | None) -> AuthResult:
    client = get_client()
    try:
        client.auth.sign_out()
        return AuthResult(True, "Sesión cerrada.")
    except Exception as exc:  # noqa: BLE001
        return AuthResult(False, f"Error al cerrar sesión: {exc}")


def request_password_reset(email: str) -> AuthResult:
    client = get_client()
    try:
        client.auth.reset_password_for_email(email)
        return AuthResult(True, "Si el correo existe, se envió un enlace de recuperación.")
    except Exception as exc:  # noqa: BLE001
        return AuthResult(False, f"No se pudo enviar la recuperación: {exc}")
