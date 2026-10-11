# Preparación de la entrega

## GitHub

Publicar este proyecto en:
https://github.com/lauraromeroforero/InteligenciaArtificialPython

Archivos principales: `rutas.py`, `tests/test_rutas.py`, `README.md`.
Como complemento: `actividad1/ejemplo_python.py` y `actividad1/ejemplo_r.R`.
Antes de entregar, ejecutar los comandos del README y conservar su salida real.
Los documentos afirman ejecuciones: comprobar personalmente las evidencias
antes de mantener esas afirmaciones en la entrega final.

## Google Drive

Carpeta indicada en los documentos:
https://drive.google.com/drive/folders/1C9uXlLQ2zHUr_G8TTDZYv0uYEjdvPgQk

Subir los dos PDF y el video grabado. Comprobar que el docente pueda acceder a
los archivos con los permisos que exige el curso. Estos materiales no están
subidos automáticamente por crear el proyecto.

## Guion sugerido para el video de actividad 1 (máximo 5 minutos)

- 0:00–0:20: presentación, nombre y objetivo: conocer Python y R para clasificación.
- 0:20–1:10: mostrar instalación desde python.org, opción Add Python to PATH
  en Windows y verificación con `python --version`.
- 1:10–2:10: mostrar instalación de Scikit-learn, abrir `ejemplo_python.py`,
  explicar los seis datos de entrenamiento y ejecutar la predicción `Alto`.
- 2:10–3:10: mostrar instalación de R desde r-project.org y de RStudio Desktop
  desde posit.co. Explicar que R es el lenguaje y RStudio su entorno de desarrollo.
- 3:10–4:20: mostrar `install.packages("rpart")`, abrir `ejemplo_r.R`, explicar
  el conjunto iris y ejecutar el árbol de decisión y la predicción `setosa`.
- 4:20–4:50: explicar que KNN compara vecinos y el árbol aprende reglas de
  clasificación; mencionar que los ejemplos son una introducción al aprendizaje automático.
- 4:50–5:00: cierre y ubicación del código y de las evidencias.

Grabar las ejecuciones reales. Si la entrega es grupal, distribuir intervenciones
entre quienes realmente participan. No afirmar que una instalación o prueba se
realizó si todavía está pendiente.

## Evidencia opcional de actividad 2

Mostrar `python rutas.py --estaciones`, `python rutas.py Portal Sur`,
`python rutas.py Portal Centro` y `python -m unittest discover -s tests -v`.
Explicar los 16 minutos de recorrido más 2 minutos de transbordo del caso principal.
