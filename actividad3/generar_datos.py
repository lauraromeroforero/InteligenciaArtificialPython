"""Genera datos académicos sintéticos; no son mediciones de TransMilenio."""
import csv
import random
from pathlib import Path

CAMPOS = ['id_viaje', 'distancia_km', 'paradas', 'hora_pico', 'lluvia',
          'ocupacion_pct', 'transbordos', 'tiempo_min']

def generar(ruta, cantidad=600, semilla=42):
    rng = random.Random(semilla)
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open('w', newline='', encoding='utf-8') as archivo:
        writer = csv.DictWriter(archivo, fieldnames=CAMPOS)
        writer.writeheader()
        for i in range(cantidad):
            distancia = round(rng.uniform(2, 25), 2)
            paradas = rng.randint(3, 24)
            pico = rng.randint(0, 1)
            lluvia = rng.randint(0, 1)
            ocupacion = rng.randint(15, 100)
            transbordos = rng.randint(0, 2)
            # Regla sintética con ruido independiente. No es una ley del transporte.
            tiempo = (distancia * 2 + paradas * 0.8 + pico * 10 + lluvia * 5
                      + ocupacion * 0.04 + transbordos * 4 + rng.gauss(0, 2))
            writer.writerow(dict(zip(CAMPOS, [i + 1, distancia, paradas, pico,
                lluvia, ocupacion, transbordos, round(max(1, tiempo), 2)])))
    return ruta

if __name__ == '__main__':
    ruta = generar(Path(__file__).parent / 'datos' / 'viajes_simulados.csv')
    print(f'Dataset simulado creado: {ruta}')
