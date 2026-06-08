# TP Integrador – Módulo 3

Trabajo Práctico Integrador del Módulo 3. Contiene ejercicios de Python, desde lógica básica hasta automatización de pruebas con Selenium y testing de APIs REST.

---

## Estructura del proyecto

```
TPIntegrador/
├── punto1.py          # Verificación de número primo
├── punto2.py          # Raíces de ecuación cuadrática
├── punto3.py          # Tests de UI con Selenium (SauceDemo)
├── punto4.py          # Tests de API REST (PokéAPI)
├── reporte_punto3.html
└── reporte_punto4.html
```

---

## Ejercicios

### Punto 1 – Verificación de número primo

Script interactivo que recibe un número entero por consola y determina si es primo o no.

**Lógica:** verifica divisibilidad hasta la raíz cuadrada del número para optimizar el proceso.

**Ejecución:**
```bash
python punto1.py
```

**Ejemplo:**
```
Ingrese un número: 17
17 es primo.
```

---

### Punto 2 – Raíces de ecuación cuadrática

Script interactivo que recibe los coeficientes `a`, `b` y `c` de una ecuación cuadrática `ax² + bx + c = 0` y calcula sus raíces reales.

**Casos contemplados:**
- Discriminante positivo → dos soluciones reales distintas
- Discriminante igual a cero → una solución real (raíz doble)
- Discriminante negativo → sin solución real

**Ejecución:**
```bash
python punto2.py
```

**Ejemplo:**
```
Ingrese el valor de a: 1
Ingrese el valor de b: -5
Ingrese el valor de c: 6
Dos soluciones: x1 = 3.0, x2 = 2.0
```

---

### Punto 3 – Tests de UI con Selenium (SauceDemo)

Suite de pruebas automatizadas sobre [https://www.saucedemo.com](https://www.saucedemo.com) usando `pytest` y `selenium`.

**Casos de prueba:**

| Clase | Test | Descripción |
|---|---|---|
| `TestCaso1` | `test_ordenar_precio_low_to_high` | Verifica que el ordenamiento "Price (low to high)" ordene correctamente los productos |
| `TestCaso2` | `test_checkout_validaciones` | Agrega todos los productos al carrito y valida los mensajes de error al omitir campos requeridos en el checkout |
| `TestCaso3` | `test_flujo_compra_completo` | Flujo completo: agrega producto, lo elimina, verifica carrito vacío, agrega 2 productos y finaliza la compra |

**Requisitos:**
- Google Chrome instalado
- ChromeDriver compatible con la versión de Chrome
- Dependencias: `selenium`, `pytest`, `pytest-html`

**Instalación de dependencias:**
```bash
pip install selenium pytest pytest-html
```

**Ejecución:**
```bash
pytest punto3.py -v --html=reporte_punto3.html --self-contained-html --log-cli-level=INFO
```

---

### Punto 4 – Tests de API REST (PokéAPI)

Suite de pruebas sobre la [PokéAPI](https://pokeapi.co/) usando `pytest` y `requests`. No requiere navegador.

**Casos de prueba:**

| Clase | Test | Descripción |
|---|---|---|
| `TestCaso1` | `test_berry_1` | Consulta `berry/1` y verifica `size == 20`, `soil_dryness == 15` y `firmness == "soft"` |
| `TestCaso2` | `test_berry_2` | Consulta `berry/2`, verifica `firmness == "super-hard"`, que su `size` sea mayor al de `berry/1` y que tengan el mismo `soil_dryness` |
| `TestCaso3` | `test_pikachu` | Consulta los datos de Pikachu y verifica que `base_experience` esté entre 10 y 1000, y que su tipo sea `"electric"` |

**Requisitos:**
- Dependencias: `requests`, `pytest`, `pytest-html`

**Instalación de dependencias:**
```bash
pip install requests pytest pytest-html
```

**Ejecución:**
```bash
pytest punto4.py -v --html=reporte_punto4.html --self-contained-html --log-cli-level=INFO
```

---

## Tecnologías utilizadas

- Python 3.x
- [Selenium](https://www.selenium.dev/) – automatización de navegador
- [pytest](https://pytest.org/) – framework de testing
- [pytest-html](https://pytest-html.readthedocs.io/) – generación de reportes HTML
- [requests](https://docs.python-requests.org/) – cliente HTTP para APIs REST
- [PokéAPI](https://pokeapi.co/) – API REST pública de Pokémon
- [SauceDemo](https://www.saucedemo.com/) – sitio de demo para pruebas de UI

---

## Autor

**Martín Cerati**
