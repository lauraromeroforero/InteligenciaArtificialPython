"""Deriva una muestra SIN etiquetas a partir de los viajes sintéticos de actividad 3."""
import csv
from pathlib import Path
BASE = Path(__file__).resolve().parent
CAMPOS = ['id_viaje', 'distancia_km', 'paradas', 'hora_pico', 'lluvia', 'ocupacion_pct', 'transbordos']

def preparar(origen, destino):
    destino = Path(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    with Path(origen).open(newline='', encoding='utf-8') as entrada, destino.open('w', newline='', encoding='utf-8') as salida:
        reader = csv.DictReader(entrada)
        writer = csv.DictWriter(salida, fieldnames=CAMPOS)
        writer.writeheader()
        for fila in reader:
            writer.writerow({campo: fila[campo] for campo in CAMPOS})
    return destino

if __name__ == '__main__':
    ruta = preparar(BASE.parent/'actividad3/datos/viajes_simulados.csv', BASE/'datos/viajes_sin_etiquetas.csv')
    print('Dataset sintético sin etiquetas:', ruta)
