"""Agrupa viajes sintéticos mediante K-means; no predice una etiqueta conocida."""
import argparse
import csv
import json
import math
from pathlib import Path
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

BASE = Path(__file__).resolve().parent
VARIABLES = ['distancia_km', 'paradas', 'hora_pico', 'lluvia', 'ocupacion_pct', 'transbordos']

def cargar_datos(ruta):
    ids, filas = [], []
    with Path(ruta).open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        if not set(['id_viaje', *VARIABLES]).issubset(reader.fieldnames or []):
            raise ValueError('Faltan columnas requeridas')
        if 'tiempo_min' in (reader.fieldnames or []) or 'grupo' in (reader.fieldnames or []):
            raise ValueError('Usar un dataset sin etiquetas ni grupos preasignados')
        for numero, fila in enumerate(reader, 2):
            try:
                identidad = int(fila['id_viaje'])
                valores = [float(fila[v]) for v in VARIABLES]
            except (ValueError, TypeError) as error:
                raise ValueError(f'Fila {numero}: datos no numéricos') from error
            if identidad in ids:
                raise ValueError(f'Fila {numero}: identificador duplicado')
            if not all(math.isfinite(v) for v in valores):
                raise ValueError(f'Fila {numero}: valores no finitos')
            distancia, paradas, pico, lluvia, ocupacion, transbordos = valores
            if (distancia <= 0 or paradas < 0 or paradas != int(paradas)
                or pico not in (0, 1) or lluvia not in (0, 1)
                or not 0 <= ocupacion <= 100 or transbordos < 0
                or transbordos != int(transbordos)):
                raise ValueError(f'Fila {numero}: valores fuera de dominio')
            ids.append(identidad); filas.append(valores)
    if len(filas) < 20:
        raise ValueError('Se requieren al menos 20 viajes')
    return ids, np.array(filas)


def agrupar(ruta):
    ids, X = cargar_datos(ruta)
    # Evitar que unidades grandes dominen la distancia euclidiana.
    escalador = StandardScaler()
    Z = escalador.fit_transform(X)
    candidatos = []
    modelos = {}
    for k in range(2, 7):
        modelo = KMeans(n_clusters=k, random_state=42, n_init=20)
        etiquetas = modelo.fit_predict(Z)
        if len(np.unique(etiquetas)) != k:
            continue
        silueta = float(silhouette_score(Z, etiquetas))
        candidatos.append({'k': k, 'silueta': silueta, 'inercia': float(modelo.inertia_)})
        modelos[k] = modelo
    if not candidatos:
        raise ValueError('No hay grupos suficientes para evaluar silueta')
    elegido = max(candidatos, key=lambda candidato: candidato['silueta'])
    modelo = modelos[elegido['k']]
    etiquetas = modelo.labels_
    perfiles = []
    for grupo in range(modelo.n_clusters):
        mascara = etiquetas == grupo
        perfiles.append({'grupo': grupo, 'cantidad': int(mascara.sum()),
            'medias_unidades_originales': dict(zip(VARIABLES, X[mascara].mean(axis=0).tolist()))})
    resumen = {
        'fuente': '600 viajes SINTETICOS derivados de actividad 3; etiqueta eliminada',
        'filas': len(ids), 'variables': VARIABLES, 'semilla': 42, 'n_init': 20,
        'metodo': 'StandardScaler + KMeans', 'candidatos': candidatos,
        'k_elegido': modelo.n_clusters, 'silueta_elegida': elegido['silueta'],
        'perfiles': perfiles,
        'limitacion': 'Seleccion y evaluacion descriptivas sobre la misma muestra; sin validacion externa ni clases reales.'}
    return ids, X, etiquetas, resumen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--datos', type=Path, default=BASE/'datos/viajes_sin_etiquetas.csv')
    parser.add_argument('--salida', type=Path, default=BASE/'resultados')
    args = parser.parse_args()
    ids, X, etiquetas, resumen = agrupar(args.datos)
    args.salida.mkdir(parents=True, exist_ok=True)
    (args.salida/'metricas.json').write_text(json.dumps(resumen, ensure_ascii=False, indent=2), encoding='utf-8')
    with (args.salida/'viajes_agrupados.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f); writer.writerow(['id_viaje', *VARIABLES, 'grupo'])
        for identidad, fila, etiqueta in zip(ids, X, etiquetas):
            writer.writerow([identidad, *fila, int(etiqueta)])
    print('DATOS SIMULADOS; no son segmentos verificados de transporte real.')
    for candidato in resumen['candidatos']:
        print(f"k={candidato['k']}: silueta={candidato['silueta']:.4f}, inercia={candidato['inercia']:.2f}")
    print(f"k elegido: {resumen['k_elegido']}; silueta: {resumen['silueta_elegida']:.4f}")
    for perfil in resumen['perfiles']:
        print(f"Grupo {perfil['grupo']}: {perfil['cantidad']} viajes; medias: {perfil['medias_unidades_originales']}")
    print('Los números de grupo son identificadores arbitrarios, no niveles de calidad.')

if __name__ == '__main__':
    main()
