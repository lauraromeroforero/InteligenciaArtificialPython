"""Árbol de regresión supervisado para tiempos de viajes simulados."""
import argparse
import csv
import json
import math
from pathlib import Path

import numpy as np
from sklearn.dummy import DummyRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeRegressor, export_text

BASE = Path(__file__).resolve().parent
VARIABLES = ['distancia_km', 'paradas', 'hora_pico', 'lluvia',
             'ocupacion_pct', 'transbordos']
OBJETIVO = 'tiempo_min'


def cargar_datos(ruta):
    X, y = [], []
    with Path(ruta).open(encoding='utf-8', newline='') as archivo:
        reader = csv.DictReader(archivo)
        if not set(['id_viaje', *VARIABLES, OBJETIVO]).issubset(reader.fieldnames or []):
            raise ValueError('Faltan columnas requeridas en el CSV')
        ids = set()
        for numero, fila in enumerate(reader, start=2):
            try:
                valores = [float(fila[nombre]) for nombre in VARIABLES]
                objetivo = float(fila[OBJETIVO])
                identidad = int(fila['id_viaje'])
            except (ValueError, TypeError) as error:
                raise ValueError(f'Fila {numero}: datos no numéricos') from error
            if identidad in ids:
                raise ValueError(f'Fila {numero}: id duplicado')
            ids.add(identidad)
            if not all(math.isfinite(v) for v in [*valores, objetivo]):
                raise ValueError(f'Fila {numero}: valores no finitos')
            distancia, paradas, pico, lluvia, ocupacion, cambios = valores
            if (distancia <= 0 or paradas < 0 or paradas != int(paradas)
                or pico not in (0, 1) or lluvia not in (0, 1)
                or not 0 <= ocupacion <= 100 or cambios < 0
                or cambios != int(cambios) or objetivo <= 0):
                raise ValueError(f'Fila {numero}: valores fuera de dominio')
            X.append(valores)
            y.append(objetivo)
    if len(y) < 30:
        raise ValueError('Se requieren al menos 30 viajes')
    return np.array(X), np.array(y)


def metricas(reales, predichos):
    return {'mae_min': float(mean_absolute_error(reales, predichos)),
            'rmse_min': float(np.sqrt(mean_squared_error(reales, predichos))),
            'r2': float(r2_score(reales, predichos))}


def entrenar(ruta):
    X, y = cargar_datos(ruta)
    # Reservar prueba ANTES de elegir hiperparámetros. ID y objetivo no entran en X.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42)
    busqueda = GridSearchCV(
        DecisionTreeRegressor(random_state=42),
        {'max_depth': [3, 5, 7, 9, None], 'min_samples_leaf': [3, 5, 10]},
        scoring='neg_mean_absolute_error', cv=5, n_jobs=1)
    busqueda.fit(X_train, y_train)
    modelo = busqueda.best_estimator_
    baseline = DummyRegressor(strategy='mean').fit(X_train, y_train)
    predicciones = modelo.predict(X_test)
    resumen = {
        'origen_datos': 'SINTETICOS; no son observaciones reales',
        'semilla': 42, 'filas_total': len(y),
        'filas_entrenamiento': len(y_train), 'filas_prueba': len(y_test),
        'variables': VARIABLES, 'objetivo': OBJETIVO,
        'mejores_parametros': busqueda.best_params_,
        'mae_validacion_cruzada_min': float(-busqueda.best_score_),
        'arbol_prueba': metricas(y_test, predicciones),
        'baseline_prueba': metricas(y_test, baseline.predict(X_test)),
        'importancias': dict(zip(VARIABLES, modelo.feature_importances_.tolist())),
        'ejemplo_entrada': dict(zip(VARIABLES, [10, 12, 1, 0, 80, 1])),
        'ejemplo_prediccion_min': float(modelo.predict([[10, 12, 1, 0, 80, 1]])[0]),
    }
    return modelo, resumen, y_test, predicciones


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, default=BASE / 'datos/viajes_simulados.csv')
    parser.add_argument('--salida', type=Path, default=BASE / 'resultados')
    args = parser.parse_args()
    modelo, resumen, reales, predicciones = entrenar(args.datos)
    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida / 'metricas.json').write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding='utf-8')
    (args.salida / 'reglas_arbol.txt').write_text(
        export_text(modelo, feature_names=VARIABLES, max_depth=20), encoding='utf-8')
    with (args.salida / 'predicciones_prueba.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['tiempo_real_simulado_min', 'tiempo_predicho_min', 'error_absoluto_min'])
        for real, pred in zip(reales, predicciones):
            writer.writerow([round(real, 4), round(pred, 4), round(abs(real-pred), 4)])
    print('DATOS SIMULADOS: no usar para planificar viajes reales.')
    print(f"Viajes: {resumen['filas_total']}; entrenamiento: {resumen['filas_entrenamiento']}; prueba: {resumen['filas_prueba']}")
    print('Parámetros:', resumen['mejores_parametros'])
    print('Árbol:', resumen['arbol_prueba'])
    print('Baseline (media):', resumen['baseline_prueba'])
    print(f"Ejemplo de 10 km: {resumen['ejemplo_prediccion_min']:.2f} minutos simulados")
    print(f'Resultados guardados en: {args.salida}')

if __name__ == '__main__':
    main()
