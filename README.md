# 💑 Finanzas en Pareja — MVP (Fase 1)

Sistema de gestión financiera para parejas. Este repositorio contiene el
**MVP (Fase 1)** del roadmap: autenticación, gestión de la pareja/hogar,
registro de ingresos y gastos, y un dashboard con el balance del período.

## Stack

- **Python 3.11+**
- **Streamlit** (interfaz)
- **Supabase** (Auth + PostgreSQL + Row Level Security)
- **Pandas / Plotly** (datos y gráficos)

## 1. Configurar Supabase

1. Crea un proyecto en [supabase.com](https://supabase.com).
2. Ve a **SQL Editor** y ejecuta el contenido de `../supabase/schema_mvp.sql`
   (crea las tablas, los índices, las políticas RLS y las categorías base).
3. En **Project Settings → API**, copia:
   - `Project URL` → `SUPABASE_URL`
   - `anon public key` → `SUPABASE_ANON_KEY`
4. En **Authentication → Providers**, confirma que el proveedor de
   Email/Password esté habilitado. Si quieres evitar el paso de
   confirmación por correo durante las pruebas, puedes desactivar
   "Confirm email" en **Authentication → Settings**.

## 2. Configurar credenciales localmente

Elige **una** de estas dos opciones:

**Opción A — archivo `.env`:**
```bash
cp .env.example .env
# edita .env con tus credenciales reales
```

**Opción B — Streamlit secrets:**
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edita .streamlit/secrets.toml con tus credenciales reales
```

Ninguno de estos archivos se sube al repositorio (ver `.gitignore`).

## 3. Instalar dependencias y ejecutar

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate

pip install -r requirements.txt

streamlit run main.py
```

La aplicación abrirá en `http://localhost:8501`.

## 4. Primer uso

1. **Crea una cuenta** para Juan José (o el primer usuario).
2. Al ingresar por primera vez, se te pedirá **crear un hogar** (pareja).
   Copia el `ID del hogar` que se genera (puedes consultarlo luego en la
   tabla `couples` de Supabase).
3. **Crea una segunda cuenta** para Alejandra y, en la pantalla de
   onboarding, elige **"Unirme a un hogar existente"** pegando ese ID.
4. Desde ahí, ambos comparten el mismo hogar financiero: pueden registrar
   ingresos y gastos propios o compartidos, y ver el dashboard consolidado.

## 5. Ejecutar las pruebas

```bash
pytest tests/ -v
```

## Estructura del proyecto

```
app/
├── main.py                  # Punto de entrada: auth + onboarding + routing
├── pages_modules/            # Páginas del MVP (dashboard, income, expenses)
├── database/
│   ├── supabase_client.py    # Cliente Supabase (cacheado, con sesión)
│   └── repositories/         # Acceso a datos por entidad
├── services/
│   └── financial_analysis.py # Orquesta los cálculos para el dashboard
├── components/                # UI reutilizable (cards, charts, forms, nav)
├── utils/                     # Funciones puras: cálculos, validadores, formato
├── config/settings.py         # Carga de credenciales (.env / secrets)
├── tests/                     # Pruebas unitarias (pytest)
└── requirements.txt
```

> Nota: la carpeta se llama `pages_modules/` (no `pages/`) porque
> `pages/` es un nombre reservado por Streamlit para su sistema de
> multipágina automático, y este MVP controla la navegación manualmente
> para poder aplicar el flujo de autenticación/onboarding antes de
> mostrar cualquier página.

## Alcance de esta fase (MVP)

✅ Incluido:
- Autenticación (registro, login, logout, recuperación de contraseña)
- Modelo de pareja/hogar con múltiples miembros
- Registro de ingresos y gastos (con categorías fijas y personalizadas)
- Diferenciación fijo/variable y personal/compartido
- Dashboard con balance, tasa de ahorro y gráficos básicos
- Row Level Security en todas las tablas

🔜 Próximas fases (ver el prompt maestro del proyecto):
- Fase 2: Presupuestos, fondo de emergencia, metas de ahorro, proyecciones
- Fase 3: Deudas, patrimonio, calendario financiero, alertas, reportes avanzados
- Fase 4: Asistente con IA, simulador "¿Qué pasaría si...?"
- Fase 5: Importación/exportación de datos, auditoría, optimización

## Principios de seguridad aplicados

- Las contraseñas nunca se manejan en el código: las gestiona Supabase Auth.
- Las credenciales se cargan por variables de entorno o `st.secrets`, nunca
  hardcodeadas.
- RLS garantiza que cada pareja solo pueda leer/escribir sus propios datos.
- Los borrados de transacciones son lógicos (`deleted_at`), no físicos,
  para mantener trazabilidad.
