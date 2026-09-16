"""
Finanzas en Pareja — punto de entrada de la aplicación Streamlit.

Flujo:
    1. Si no hay sesión activa -> pantalla de login/registro.
    2. Si hay sesión pero el usuario no pertenece a ninguna pareja ->
       pantalla de onboarding (crear pareja / unirse a una existente).
    3. Si hay sesión y pareja -> navegación normal (dashboard/ingresos/gastos).
"""
from __future__ import annotations

import streamlit as st

from components.navigation import render_sidebar
from database.repositories import auth_repository, couple_repository
from pages_modules import dashboard, expenses, income
from utils.validators import is_valid_email, is_valid_password

st.set_page_config(page_title="Finanzas en Pareja", page_icon="💑", layout="wide")


def _render_login_screen() -> None:
    st.title("💑 Finanzas en Pareja")
    st.caption("Gestión financiera integral para tu hogar.")

    tab_login, tab_signup = st.tabs(["Iniciar sesión", "Crear cuenta"])

    with tab_login:
        with st.form("login_form"):
            email = st.text_input("Correo electrónico")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Iniciar sesión", type="primary", use_container_width=True)
            if submitted:
                result = auth_repository.sign_in(email, password)
                if result.success:
                    st.session_state["auth_session"] = result.session
                    st.session_state["user_id"] = result.user_id
                    st.session_state["user_email"] = email
                    st.rerun()
                else:
                    st.error(result.message)

        if st.button("¿Olvidaste tu contraseña?"):
            st.session_state["show_reset"] = True

        if st.session_state.get("show_reset"):
            with st.form("reset_form"):
                reset_email = st.text_input("Correo para recuperación")
                if st.form_submit_button("Enviar enlace de recuperación"):
                    result = auth_repository.request_password_reset(reset_email)
                    (st.success if result.success else st.error)(result.message)

    with tab_signup:
        with st.form("signup_form"):
            full_name = st.text_input("Nombre completo")
            email = st.text_input("Correo electrónico", key="signup_email")
            password = st.text_input("Contraseña", type="password", key="signup_password")
            submitted = st.form_submit_button("Crear cuenta", type="primary", use_container_width=True)
            if submitted:
                if not full_name.strip():
                    st.error("Ingresa tu nombre completo.")
                elif not is_valid_email(email):
                    st.error("Ingresa un correo electrónico válido.")
                else:
                    valid_pw, pw_msg = is_valid_password(password)
                    if not valid_pw:
                        st.error(pw_msg)
                    else:
                        result = auth_repository.sign_up(email, password, full_name)
                        if result.success:
                            st.success(result.message)
                            if result.session:
                                st.session_state["auth_session"] = result.session
                                st.session_state["user_id"] = result.user_id
                                st.session_state["user_email"] = email
                                st.rerun()
                        else:
                            st.error(result.message)


def _render_onboarding_screen(user_id: str) -> dict:
    st.title("👋 ¡Bienvenido a Finanzas en Pareja!")
    st.caption("Antes de continuar, crea tu hogar financiero o únete a uno existente.")

    tab_create, tab_join = st.tabs(["Crear un hogar nuevo", "Unirme a un hogar existente"])

    with tab_create:
        with st.form("create_couple_form"):
            couple_name = st.text_input("Nombre del hogar", value="Nuestro hogar")
            if st.form_submit_button("Crear hogar", type="primary", use_container_width=True):
                couple = couple_repository.create_couple(couple_name, user_id)
                st.success("¡Hogar creado! Ya puedes empezar a registrar tus finanzas.")
                st.rerun()
                return couple

    with tab_join:
        with st.form("join_couple_form"):
            couple_id = st.text_input("ID del hogar (compartido por tu pareja)")
            if st.form_submit_button("Unirme", use_container_width=True):
                try:
                    couple_repository.join_couple(couple_id.strip(), user_id)
                    st.success("Te uniste al hogar correctamente.")
                    st.rerun()
                except Exception as exc:  # noqa: BLE001
                    st.error(f"No se pudo unir al hogar: {exc}")

    return None


def main() -> None:
    if st.session_state.get("logout_requested"):
        auth_repository.sign_out(None)
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    if "auth_session" not in st.session_state or "user_id" not in st.session_state:
        _render_login_screen()
        return

    user_id = st.session_state["user_id"]
    couple = couple_repository.get_couple_for_user(user_id)

    if couple is None:
        _render_onboarding_screen(user_id)
        return

    couple_id = couple["id"]
    couple_name = couple.get("name", "Nuestro hogar")
    user_full_name = st.session_state.get("user_email", "Usuario")

    page = render_sidebar(user_full_name, couple_name)

    if page == "dashboard":
        dashboard.render(couple_id)
    elif page == "income":
        income.render(couple_id, user_id)
    elif page == "expenses":
        expenses.render(couple_id, user_id)


if __name__ == "__main__":
    main()
