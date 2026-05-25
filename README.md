# 🤖 SauceDemo — Automatización con Selenium WebDriver + Python

> **Pre-Entrega de Proyecto · Curso de Testing Automatizado**  
> Automatización de pruebas funcionales sobre [saucedemo.com](https://www.saucedemo.com)  
> Tecnologías: Python · Pytest · Selenium WebDriver · Git & GitHub

---

## 📋 Tabla de contenidos

1. [Propósito del proyecto](#propósito-del-proyecto)
2. [Tecnologías utilizadas](#tecnologías-utilizadas)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Instalación de dependencias](#instalación-de-dependencias)
5. [Cómo ejecutar las pruebas](#cómo-ejecutar-las-pruebas)
6. [Generar reporte HTML](#generar-reporte-html)
7. [Casos de prueba implementados](#casos-de-prueba-implementados)
8. [Evidencias y capturas automáticas](#evidencias-y-capturas-automáticas)
9. [Patrón de diseño: Page Object Model](#patrón-de-diseño-page-object-model)
10. [Usuarios de prueba disponibles](#usuarios-de-prueba-disponibles)
11. [Nombre del repositorio y commits](#nombre-del-repositorio-y-commits)

---

## Propósito del proyecto

Este proyecto automatiza las pruebas funcionales de la aplicación web demo [saucedemo.com](https://www.saucedemo.com), demostrando el uso de **Selenium WebDriver + Python + Pytest** para validar los flujos principales de una tienda online.

Cubre **32 casos de prueba** organizados en 4 módulos:

- **Login:** autenticación válida, usuarios bloqueados, validación de errores y URL.
- **Inventario / Catálogo:** título, presencia de productos, nombre/precio, elementos de UI.
- **Carrito:** agregar producto, badge, navegación y verificación de ítem en carrito.
- **Checkout:** formulario, validaciones de error, resumen de pedido y compra E2E.

El código sigue el patrón **Page Object Model (POM)** con funciones auxiliares en `utils/helpers.py`, garantizando tests independientes, legibles y fáciles de mantener.

---

## Tecnologías utilizadas

| Tecnología | Versión | Rol en el proyecto |
|---|---|---|
| **Python** | 3.10+ | Lenguaje principal |
| **Selenium WebDriver** | 4.18.1 | Automatización del navegador Chrome |
| **pytest** | 8.1.1 | Framework de testing y organización de suites |
| **pytest-html** | 4.1.1 | Generación de reportes HTML con resultados |
| **webdriver-manager** | 4.0.1 | Gestión automática del ChromeDriver |
| **Git + GitHub** | — | Control de versiones y entrega del proyecto |

---

## Estructura del proyecto

```
pre-entrega-automation-testing-[nombre-apellido]/
│
├── 📄 conftest.py              # Fixtures globales y hook de captura en fallos
├── 📄 pytest.ini               # Configuración de pytest (reporte HTML, marcas)
├── 📄 requirements.txt         # Dependencias (pip install -r requirements.txt)
├── 📄 README.md                # Este archivo
├── 📄 .gitignore               # Archivos excluidos del repositorio
│
├── 📁 pages/                   # Page Objects — Patrón POM
│   ├── base_page.py            # Clase base con WebDriverWait y métodos comunes
│   ├── login_page.py           # Página de autenticación
│   ├── inventory_page.py       # Página de productos/inventario
│   ├── cart_page.py            # Página del carrito de compras
│   └── checkout_page.py        # Páginas del flujo de checkout
│
├── 📁 tests/                   # Suites de pruebas por módulo
│   ├── test_login.py           # TC-001 al TC-010: Login y autenticación
│   ├── test_inventory.py       # TC-011 al TC-025: Inventario y catálogo
│   ├── test_carrito.py         # TC-026 al TC-032: Carrito de compras
│   └── test_checkout.py        # TC-033 al TC-041: Checkout completo
│
├── 📁 utils/                   # Funciones auxiliares reutilizables
│   ├── constants.py            # URLs, credenciales y datos de prueba
│   └── helpers.py              # Helpers: esperas, capturas, validaciones
│
├── 📁 datos/                   # Datos externos de prueba (CSV/JSON si aplica)
│
└── 📁 reports/                 # Generado automáticamente al ejecutar pytest
    ├── reporte.html            # Reporte HTML con todos los resultados
    └── screenshots/            # Capturas PNG automáticas de tests fallidos
```

> **Nota:** `reports/` y `datos/` se incluyen en el repo con `.gitkeep`.  
> El reporte HTML y las capturas se generan al ejecutar `pytest`.

---

## Instalación de dependencias

### Prerrequisitos

- Python 3.10 o superior → [python.org](https://www.python.org/downloads/)
- Google Chrome instalado (cualquier versión reciente)
- Git → [git-scm.com](https://git-scm.com/)

### Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/pre-entrega-automation-testing-nombre-apellido.git
cd pre-entrega-automation-testing-nombre-apellido
```

### Paso 2 — Crear entorno virtual

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows (CMD)
python -m venv venv
venv\Scripts\activate

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

### Paso 3 — Instalar dependencias

```bash
pip install -r requirements.txt
```

> `webdriver-manager` descarga el ChromeDriver automáticamente. No se requiere instalación manual.

---

## Cómo ejecutar las pruebas

### ▶️ Comando principal (genera reporte HTML automáticamente)

```bash
pytest tests/ -v --html=reports/reporte.html --self-contained-html
```

### ▶️ Comando exacto de la consigna

```bash
pytest pre-entrega-final/test_saucedemo.py -v --html=reporte.html
```

### ▶️ Ejecutar toda la suite (usa configuración de pytest.ini)

```bash
pytest
```

### ▶️ Ejecutar un módulo específico

```bash
pytest tests/test_login.py
pytest tests/test_inventory.py
pytest tests/test_carrito.py
pytest tests/test_checkout.py
```

### ▶️ Ejecutar un test por nombre

```bash
pytest -k "test_login_exitoso"
pytest -k "test_flujo_completo"
```

### ▶️ Output detallado con prints visibles

```bash
pytest -v -s
```

### ▶️ Modo headless (sin abrir el navegador — ideal para CI/CD)

Editar `conftest.py` y descomentar:

```python
chrome_options.add_argument("--headless")
```

---

## Generar reporte HTML

El reporte se genera automáticamente con cada ejecución de `pytest` gracias a la configuración en `pytest.ini`:

```ini
addopts =
    --html=reports/reporte.html
    --self-contained-html
    -v
```

También se puede generar manualmente:

```bash
pytest tests/ -v --html=reports/reporte.html --self-contained-html
```

### Abrir el reporte

```bash
# macOS
open reports/reporte.html

# Linux
xdg-open reports/reporte.html

# Windows
start reports/reporte.html
```

El reporte muestra:
- ✅ Tests aprobados (PASSED)
- ❌ Tests fallidos (FAILED) con traceback completo
- ⏭️ Tests omitidos (SKIPPED)
- Tiempo de ejecución por test y total de la suite

---

## Casos de prueba implementados

### 🔐 Login — `tests/test_login.py`

| ID | Test | Tipo | Descripción |
|---|---|---|---|
| TC-001 | `test_login_exitoso_valida_url_inventario` | ✅ Positivo | Valida redirección a /inventory.html |
| TC-002 | `test_login_exitoso_valida_titulo_contenido_products` | ✅ Positivo | Valida H1 "Products" |
| TC-003 | `test_login_exitoso_valida_titulo_pestaña_swag_labs` | ✅ Positivo | Valida `<title>` "Swag Labs" |
| TC-004 | `test_login_exitoso_triple_validacion_completa` | 🎯 Integrado | URL + título + pestaña en un test |
| TC-005 | `test_login_sin_credenciales_muestra_error_username` | ❌ Negativo | Error campos vacíos |
| TC-006 | `test_login_sin_password_muestra_error_password` | ❌ Negativo | Error sin contraseña |
| TC-007 | `test_login_credenciales_invalidas_muestra_error` | ❌ Negativo | Error credenciales incorrectas |
| TC-008 | `test_login_usuario_bloqueado_muestra_error_locked` | ❌ Negativo | Error usuario bloqueado |
| TC-009 | `test_login_fallido_no_redirige_al_inventario` | ❌ Negativo | URL no cambia |
| TC-010 | `test_login_negativo_parametrizado` | 🔄 Parametrizado | 4 casos negativos |

### 🛒 Inventario / Catálogo — `tests/test_inventory.py`

| ID | Test | Tipo | Descripción |
|---|---|---|---|
| TC-011 | `test_pagina_inventario_muestra_titulo_correcto` | 🔍 Validación | Título "Products" |
| TC-012 | `test_inventario_muestra_exactamente_seis_productos` | 🔍 Validación | 6 productos listados |
| TC-013 | `test_todos_los_productos_tienen_nombre_visible` | 🔍 Validación | Nombres no vacíos |
| TC-014 | `test_todos_los_productos_tienen_precio_valido` | 🔍 Validación | Precios > $0 |
| TC-015 | `test_agregar_producto_actualiza_badge_carrito` | ⚡ Interacción | Badge muestra 1 |
| TC-016 | `test_agregar_multiples_productos_actualiza_badge` | ⚡ Interacción | Badge muestra 2 |
| TC-017 | `test_quitar_producto_elimina_badge_carrito` | ⚡ Interacción | Badge desaparece |
| TC-018 | `test_click_en_icono_carrito_navega_a_cart` | 🧭 Navegación | Navegar al carrito |
| TC-019 | `test_logout_desde_menu_redirige_a_login` | 🧭 Navegación | Logout correcto |
| TC-020 | `test_agregar_cada_producto_al_carrito` | 🔄 Parametrizado | 3 productos |
| TC-021 | `test_titulo_pagina_inventario_es_correcto` *(Segundo commit)* | 🔍 Validación | Título catálogo |
| TC-022 | `test_catalogo_tiene_al_menos_un_producto_visible` *(Segundo commit)* | 🔍 Validación | ≥1 producto |
| TC-023 | `test_primer_producto_tiene_nombre_y_precio_visibles` *(Segundo commit)* | 🔍 Validación | Nombre + precio del primero |
| TC-024 | `test_menu_hamburguesa_esta_presente_en_la_interfaz` *(Segundo commit)* | 🖥️ UI | Menú visible |
| TC-025 | `test_filtro_ordenamiento_esta_presente_en_la_interfaz` *(Segundo commit)* | 🖥️ UI | Filtros visibles |
| TC-026 | `test_icono_carrito_esta_presente_en_la_interfaz` *(Segundo commit)* | 🖥️ UI | Ícono carrito visible |

### 🛍️ Carrito de Compras — `tests/test_carrito.py` *(Tercer commit)*

| ID | Test | Tipo | Descripción |
|---|---|---|---|
| TC-027 | `test_badge_carrito_es_cero_antes_de_agregar` | 🔍 Precondición | Badge = 0 inicial |
| TC-028 | `test_agregar_primer_producto_incrementa_badge_a_uno` | ⚡ Interacción | Badge = 1 tras agregar |
| TC-029 | `test_navegar_al_carrito_muestra_url_correcta` | 🧭 Navegación | URL /cart.html |
| TC-030 | `test_carrito_muestra_titulo_your_cart` | 🔍 Validación | Título "Your Cart" |
| TC-031 | `test_producto_agregado_aparece_en_el_carrito` | ✅ Criterio mínimo | Ítem en carrito |
| TC-032 | `test_nombre_del_primer_item_en_carrito_es_correcto` | 🔍 Validación | Nombre exacto del ítem |
| TC-033 | `test_flujo_completo_agregar_y_verificar_en_carrito` | 🎯 Integrado | Flujo completo |

### 💳 Checkout — `tests/test_checkout.py`

| ID | Test | Tipo | Descripción |
|---|---|---|---|
| TC-034 | `test_carrito_muestra_titulo_correcto` | 🔍 Validación | Título "Your Cart" |
| TC-035 | `test_carrito_contiene_exactamente_un_item` | 🔍 Validación | 1 ítem en carrito |
| TC-036 | `test_carrito_contiene_el_producto_correcto` | 🔍 Validación | Nombre del producto |
| TC-037 | `test_click_checkout_navega_al_formulario` | 🧭 Navegación | Ir al formulario |
| TC-038 | `test_formulario_error_sin_first_name` | ❌ Negativo | Error First Name |
| TC-039 | `test_formulario_error_sin_last_name` | ❌ Negativo | Error Last Name |
| TC-040 | `test_formulario_error_sin_postal_code` | ❌ Negativo | Error Postal Code |
| TC-041 | `test_resumen_muestra_total_mayor_a_cero` | 🔍 Validación | Total > $0 |
| TC-042 | `test_flujo_completo_de_compra_end_to_end` | 🎯 E2E | **Compra completa** |

---

## Evidencias y capturas automáticas

El proyecto genera **capturas de pantalla automáticas** cuando un test falla, sin necesidad de configuración adicional.

El hook `pytest_runtest_makereport` en `conftest.py` intercepta cada test fallido y guarda la captura en:

```
reports/screenshots/FALLA_nombre_del_test_20240101_143022.png
```

Las capturas se nombran con el nombre del test y un timestamp, evitando sobreescrituras entre ejecuciones.

---

## Patrón de diseño: Page Object Model

```
┌──────────────────────────────────────────────────────┐
│                 TESTS (qué verificar)                 │
│  test_login · test_inventory · test_carrito · checkout│
└─────────────────────┬────────────────────────────────┘
                      │ usan
┌─────────────────────▼────────────────────────────────┐
│            PAGE OBJECTS (cómo interactuar)            │
│  LoginPage · InventoryPage · CartPage · CheckoutPage  │
│               heredan de BasePage                     │
└─────────────────────┬────────────────────────────────┘
                      │ usan
┌─────────────────────▼────────────────────────────────┐
│          SELENIUM WEBDRIVER + CHROME                  │
└──────────────────────────────────────────────────────┘
```

Cada Page Object encapsula localizadores y acciones de una sola pantalla. Los tests solo llaman métodos de alto nivel (`login()`, `add_product_to_cart()`, `click_checkout()`), sin conocer los detalles de implementación.

---

## Usuarios de prueba disponibles

| Usuario | Contraseña | Comportamiento |
|---|---|---|
| `standard_user` | `secret_sauce` | Flujo normal ✅ |
| `locked_out_user` | `secret_sauce` | Bloqueado al hacer login ❌ |
| `problem_user` | `secret_sauce` | Imágenes rotas, bugs visuales ⚠️ |
| `performance_glitch_user` | `secret_sauce` | Carga lenta 🐢 |
| `error_user` | `secret_sauce` | Errores al modificar carrito 🔴 |
| `visual_user` | `secret_sauce` | Layout con diferencias visuales 👁️ |

---

## Nombre del repositorio y commits

### Nombre del repositorio

El repositorio debe nombrarse siguiendo el formato requerido por la consigna:

```
pre-entrega-automation-testing-[nombre-apellido]
```

Ejemplo: `pre-entrega-automation-testing-juan-perez`

### Historial de commits sugerido

```
git commit -m "Primer commit: estructura del proyecto, conftest y Page Objects base"
git commit -m "Primer commit: tests de login con esperas explícitas y triple validación"
git commit -m "Segundo commit: tests de navegación y verificación del catálogo (TC-021 al TC-026)"
git commit -m "Tercer commit: tests de interacción con carrito (TC-027 al TC-033)"
git commit -m "docs: README completo con propósito, tecnologías, instalación y ejecución"
```

### Subir al repositorio

```bash
git init
git add .
git commit -m "Primer commit: estructura inicial del proyecto"
git branch -M main
git remote add origin https://github.com/tu-usuario/pre-entrega-automation-testing-nombre-apellido.git
git push -u origin main
```
