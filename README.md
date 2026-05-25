 **Pre-Entrega de Proyecto · Curso de Testing Automatizado**  
> Automatización de pruebas funcionales sobre [saucedemo.com](https://www.saucedemo.com)  
> Tecnologías: Python · Pytest · Selenium WebDriver · Git & GitHub

---

## 📋 Tabla de contenidos

1. [Descripción del proyecto](#descripción-del-proyecto)
2. [Tecnologías utilizadas](#tecnologías-utilizadas)
3. [Estructura del proyecto](#estructura-del-proyecto)
4. [Instalación y configuración](#instalación-y-configuración)
5. [Cómo ejecutar los tests](#cómo-ejecutar-los-tests)
6. [Casos de prueba implementados](#casos-de-prueba-implementados)
7. [Módulo de funciones auxiliares](#módulo-de-funciones-auxiliares)
8. [Patrón de diseño: Page Object Model](#patrón-de-diseño-page-object-model)
9. [Usuarios de prueba disponibles](#usuarios-de-prueba-disponibles)
10. [Reporte de resultados](#reporte-de-resultados)

---

## Descripción del proyecto

Este proyecto implementa una suite de **casos de prueba automatizados** sobre la aplicación web demo [saucedemo.com](https://www.saucedemo.com), cubriendo los flujos principales de la aplicación:

- **Autenticación:** login válido, usuarios bloqueados, campos vacíos, credenciales incorrectas.
- **Inventario:** visualización de productos, agregar/quitar del carrito, navegación.
- **Checkout:** formulario de datos, validación de errores, resumen de compra y confirmación.

El código está organizado siguiendo el patrón **Page Object Model (POM)**, con funciones auxiliares centralizadas en un módulo separado (`utils/helpers.py`), asegurando reutilización, legibilidad y facilidad de mantenimiento.

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
saucedemo_automation/
│
├── 📄 conftest.py              # Fixtures globales de pytest (driver, driver_sesion, hooks)
├── 📄 pytest.ini               # Configuración de pytest (opciones, marcas, directorios)
├── 📄 requirements.txt         # Dependencias del proyecto (pip install -r)
├── 📄 README.md                # Este archivo
├── 📄 .gitignore               # Archivos excluidos del control de versiones
│
├── 📁 pages/                   # Page Objects (Patrón POM)
│   ├── __init__.py
│   ├── base_page.py            # Clase base con métodos reutilizables (click, send_keys...)
│   ├── login_page.py           # Página de autenticación
│   ├── inventory_page.py       # Página de productos/inventario
│   ├── cart_page.py            # Página del carrito de compras
│   └── checkout_page.py        # Páginas del flujo de checkout (Info, Overview, Complete)
│
├── 📁 tests/                   # Suites de tests organizadas por módulo
│   ├── __init__.py
│   ├── test_login.py           # TC-001 al TC-009: Tests de autenticación
│   ├── test_inventory.py       # TC-010 al TC-019: Tests de inventario
│   └── test_checkout.py        # TC-020 al TC-028: Tests de checkout
│
├── 📁 utils/                   # Módulo de funciones auxiliares
│   ├── __init__.py
│   ├── constants.py            # Constantes: URLs, credenciales, textos esperados
│   └── helpers.py              # Funciones auxiliares reutilizables (ver sección abajo)
│
└── 📁 reports/                 # Generado automáticamente al ejecutar los tests
    ├── reporte.html            # Reporte HTML con resultados detallados
    └── screenshots/            # Capturas automáticas de tests fallidos
```

> **Nota:** La carpeta `reports/` se crea automáticamente al ejecutar `pytest`.

---

## Instalación y configuración

### Prerrequisitos

- Python 3.10 o superior instalado → [python.org](https://www.python.org/downloads/)
- Google Chrome instalado (cualquier versión reciente)
- Git instalado → [git-scm.com](https://git-scm.com/)

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/saucedemo-automation.git
cd saucedemo-automation
```

### Paso 2: Crear entorno virtual

Un entorno virtual aísla las dependencias del proyecto del sistema global.

```bash
# En macOS / Linux
python3 -m venv venv
source venv/bin/activate

# En Windows (CMD)
python -m venv venv
venv\Scripts\activate

# En Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
```

Cuando el entorno está activo, verás `(venv)` al inicio del prompt.

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

`webdriver-manager` descarga automáticamente el ChromeDriver compatible
con tu versión de Chrome. **No es necesario instalarlo manualmente.**

---

## Cómo ejecutar los tests

### ▶️ Ejecutar toda la suite

```bash
pytest
```

### ▶️ Ejecutar un archivo específico

```bash
pytest tests/test_login.py
pytest tests/test_inventory.py
pytest tests/test_checkout.py
```

### ▶️ Ejecutar un test por nombre

```bash
pytest -k "test_login_exitoso"
pytest -k "test_flujo_completo"
```

### ▶️ Ejecutar por ID de caso de prueba

```bash
pytest -k "TC-028"   # El test E2E completo
```

### ▶️ Ejecutar solo tests parametrizados

```bash
pytest -k "parametrizado"
```

### ▶️ Ver output detallado (recomendado)

```bash
pytest -v -s
```

- `-v` → Verbose: muestra nombre completo de cada test
- `-s` → Muestra los `print()` del código en consola

### ▶️ Modo headless (sin abrir el navegador)

Ideal para servidores CI/CD. Editar `conftest.py` y descomentar:

```python
chrome_options.add_argument("--headless")
```

---

## Casos de prueba implementados

### 🔐 Módulo Login — `tests/test_login.py`

| ID | Nombre del test | Tipo | Descripción |
|---|---|---|---|
| TC-001 | `test_login_exitoso_con_credenciales_validas` | ✅ Positivo | Login exitoso con standard_user |
| TC-002 | `test_titulo_pestaña_navegador_es_swag_labs` | 🔍 Validación | Título de pestaña del navegador |
| TC-003 | `test_url_correcta_despues_del_login_exitoso` | 🔍 Validación | URL /inventory.html post-login |
| TC-004 | `test_login_falla_sin_completar_ningún_campo` | ❌ Negativo | Error con campos vacíos |
| TC-005 | `test_login_falla_sin_ingresar_password` | ❌ Negativo | Error sin contraseña |
| TC-006 | `test_login_falla_con_credenciales_incorrectas` | ❌ Negativo | Error con password incorrecto |
| TC-007 | `test_login_falla_con_usuario_bloqueado` | ❌ Negativo | Error con locked_out_user |
| TC-008 | `test_url_no_cambia_despues_de_login_fallido` | 🔍 Validación | URL permanece en raíz |
| TC-009 | `test_login_parametrizado_casos_negativos` | 🔄 Parametrizado | 4 escenarios negativos en 1 test |

### 🛒 Módulo Inventario — `tests/test_inventory.py`

| ID | Nombre del test | Tipo | Descripción |
|---|---|---|---|
| TC-010 | `test_pagina_inventario_muestra_titulo_correcto` | 🔍 Validación | Título 'Products' |
| TC-011 | `test_inventario_muestra_exactamente_seis_productos` | 🔍 Validación | 6 productos listados |
| TC-012 | `test_todos_los_productos_tienen_nombre_visible` | 🔍 Validación | Nombres no vacíos |
| TC-013 | `test_todos_los_productos_tienen_precio_valido` | 🔍 Validación | Precios > $0 |
| TC-014 | `test_agregar_producto_actualiza_badge_carrito` | ⚡ Interacción | Badge muestra '1' |
| TC-015 | `test_agregar_multiples_productos_actualiza_badge` | ⚡ Interacción | Badge muestra '2' |
| TC-016 | `test_quitar_producto_elimina_badge_carrito` | ⚡ Interacción | Badge desaparece |
| TC-017 | `test_click_en_icono_carrito_navega_a_cart` | 🧭 Navegación | Ir al carrito |
| TC-018 | `test_logout_desde_menu_redirige_a_login` | 🧭 Navegación | Logout correcto |
| TC-019 | `test_agregar_cada_producto_al_carrito` | 🔄 Parametrizado | 3 productos distintos |

### 💳 Módulo Checkout — `tests/test_checkout.py`

| ID | Nombre del test | Tipo | Descripción |
|---|---|---|---|
| TC-020 | `test_carrito_muestra_titulo_correcto` | 🔍 Validación | Título 'Your Cart' |
| TC-021 | `test_carrito_contiene_exactamente_un_item` | 🔍 Validación | 1 ítem en carrito |
| TC-022 | `test_carrito_contiene_el_producto_correcto` | 🔍 Validación | Nombre del producto |
| TC-023 | `test_click_checkout_navega_al_formulario` | 🧭 Navegación | Ir al formulario |
| TC-024 | `test_formulario_error_sin_first_name` | ❌ Negativo | Error First Name |
| TC-025 | `test_formulario_error_sin_last_name` | ❌ Negativo | Error Last Name |
| TC-026 | `test_formulario_error_sin_postal_code` | ❌ Negativo | Error Postal Code |
| TC-027 | `test_resumen_muestra_total_mayor_a_cero` | 🔍 Validación | Total > $0 |
| TC-028 | `test_flujo_completo_de_compra_end_to_end` | 🎯 E2E | **Flujo completo de compra** |

---

## Módulo de funciones auxiliares

`utils/helpers.py` centraliza funciones reutilizables organizadas en 5 secciones:

### Sección 1 — Helpers de espera
| Función | Descripción |
|---|---|
| `esperar_url_contiene(driver, texto, timeout)` | Espera hasta que la URL contenga el texto |
| `esperar_elemento_desaparece(driver, by, locator)` | Espera hasta que un elemento desaparezca |

### Sección 2 — Capturas de pantalla
| Función | Descripción |
|---|---|
| `tomar_captura(driver, nombre, directorio)` | Guarda captura con timestamp |
| `tomar_captura_en_falla(driver, nombre)` | Wrapper para capturas de tests fallidos |

### Sección 3 — Validaciones genéricas
| Función | Descripción |
|---|---|
| `verificar_titulo_pagina(driver, titulo)` | Verifica el `<title>` de la pestaña |
| `elemento_existe_en_pagina(driver, by, locator)` | Verifica presencia en el DOM |
| `contar_elementos(driver, by, locator)` | Cuenta elementos que coinciden |

### Sección 4 — Datos y formateo
| Función | Descripción |
|---|---|
| `extraer_precio(texto)` | Convierte `'$29.99'` → `29.99` (float) |
| `formatear_nombre_producto_a_id(nombre)` | Convierte nombre a formato data-test |
| `obtener_timestamp_legible()` | Retorna fecha/hora formateada |
| `generar_datos_usuario_invalido(caso)` | Datos para tests parametrizados de login |

### Sección 5 — Navegación
| Función | Descripción |
|---|---|
| `hacer_scroll_al_fondo(driver)` | Scroll al final de la página |
| `hacer_scroll_al_inicio(driver)` | Scroll al inicio de la página |
| `obtener_texto_todos_elementos(driver, by, locator)` | Lista de textos de múltiples elementos |

---

## Patrón de diseño: Page Object Model

El proyecto aplica el patrón **Page Object Model (POM)**, un estándar en la industria del testing automatizado:

```
┌─────────────────────────────────────────────────────┐
│                    TESTS (qué verificar)             │
│  test_login.py · test_inventory.py · test_checkout.py│
└──────────────────────┬──────────────────────────────┘
                       │ usan
┌──────────────────────▼──────────────────────────────┐
│              PAGE OBJECTS (cómo interactuar)         │
│  LoginPage · InventoryPage · CartPage · CheckoutPage │
│              (heredan de BasePage)                   │
└──────────────────────┬──────────────────────────────┘
                       │ usan
┌──────────────────────▼──────────────────────────────┐
│           SELENIUM WEBDRIVER (navegador)             │
│                  Chrome Browser                      │
└─────────────────────────────────────────────────────┘
```

**Ventajas del POM en este proyecto:**
- Los **localizadores** (By.ID, By.CLASS_NAME, etc.) están en un solo lugar.
- Si la app cambia un ID o class, solo se edita el Page Object, no todos los tests.
- Los tests se leen como acciones humanas: `login_page.login(user, password)`.
- Facilita agregar nuevos tests sin duplicar código de interacción.

---

## Usuarios de prueba disponibles

SauceDemo provee distintos usuarios para simular escenarios:

| Usuario | Contraseña | Comportamiento |
|---|---|---|
| `standard_user` | `secret_sauce` | Flujo normal, todos los tests pasan ✅ |
| `locked_out_user` | `secret_sauce` | Bloqueado, no puede hacer login ❌ |
| `problem_user` | `secret_sauce` | Imágenes rotas, bugs visuales ⚠️ |
| `performance_glitch_user` | `secret_sauce` | Carga lenta del servidor 🐢 |
| `error_user` | `secret_sauce` | Errores al modificar el carrito 🔴 |
| `visual_user` | `secret_sauce` | Diferencias visuales en el layout 👁️ |

---

## Reporte de resultados

Al ejecutar `pytest`, se genera automáticamente:

```
reports/
├── reporte.html          # Abrí en el navegador para ver resultados detallados
└── screenshots/          # Capturas PNG de tests fallidos (automáticas)
    └── FALLA_test_nombre_20241210_143022.png
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
- ❌ Tests fallidos (FAILED) con detalle del error
- ⚠️ Tests con advertencias (WARNING)
- ⏭️ Tests omitidos (SKIPPED)
- Tiempo de ejecución de cada test y total
