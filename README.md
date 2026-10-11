# Inteligencia Artificial en Python y R

Material académico de Laura Lorena Forero Romero.

## Actividad 2: búsqueda de rutas

Requiere Python 3.10 o posterior. Utiliza únicamente la biblioteca estándar:
no necesita instalar paquetes ni servicios.
Desde la carpeta del repositorio:

```sh
python rutas.py --estaciones
python rutas.py Portal Sur
python rutas.py Portal Centro
python rutas.py Portal Sur --penalizacion 0
python -m unittest discover -s tests -v
```

En Windows puedes sustituir `python` por `py`.
Portal → Sur devuelve Portal - Norte - Occidente - Parque - Hospital - Sur,
con líneas Azul, Verde, Verde, Verde, Verde y 18 minutos simulados.
Portal → Centro tarda 8 minutos. Sin penalización, Portal → Sur tarda 16.

### Hechos, reglas y búsqueda

`ESTACIONES` define coordenadas abstractas y `CONEXIONES` define estaciones
vecinas, minutos y líneas. Las conexiones son bidireccionales. El primer abordaje
no tiene penalización; cada cambio de línea añade 2 minutos por defecto.
A* explora estados `(estación, línea actual)` y utiliza `f = g + h`.
La heurística es la distancia euclidiana; cuando un grafo modificado tiene un tramo
más barato que esa distancia, el programa usa `h = 0` para mantener la optimalidad.
Los costos deben ser finitos y no negativos. Una estación desconocida genera
`ValueError`; un destino registrado pero desconectado devuelve `None`.

Las seis pruebas cubren ruta directa, ruta óptima con transbordo, origen igual al
destino, estación desconocida, destino aislado y cambio de penalización.

**La red es simulada: no representa rutas ni tiempos reales de TransMilenio.**

## Actividad 1: clasificación

Python y Scikit-learn:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install scikit-learn
python actividad1/ejemplo_python.py
```

Resultado esperado: `Predicción: Alto`.

Para R, instala R y RStudio Desktop desde sus sitios oficiales. En la consola de
RStudio ejecuta `install.packages("rpart")` si es necesario, abre
`actividad1/ejemplo_r.R` y ejecútalo. La predicción esperada es `setosa`.
También puedes usar `Rscript actividad1/ejemplo_r.R` desde una terminal con R.

El guion y la lista de entrega están en `entrega/GUIA_ENTREGA.md`.
El ejemplo R debe comprobarse en un equipo con R; este entorno no incluye RStudio.
