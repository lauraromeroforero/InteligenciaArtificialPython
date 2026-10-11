"""Búsqueda A* en una red académica simulada, no en rutas reales de Bogotá."""
import argparse
import heapq
import math
from dataclasses import dataclass
from itertools import count

ESTACIONES = {
    'Portal': (0, 0), 'Norte': (1, 0), 'Centro': (2, 0),
    'Universidad': (3, 0), 'Occidente': (1, 1), 'Parque': (2, 1),
    'Hospital': (3, 1), 'Sur': (4, 1),
}
CONEXIONES = [
    ('Portal', 'Norte', 4, 'Azul'), ('Norte', 'Centro', 4, 'Azul'),
    ('Centro', 'Universidad', 3, 'Roja'),
    ('Universidad', 'Hospital', 4, 'Roja'),
    ('Norte', 'Occidente', 3, 'Verde'), ('Occidente', 'Parque', 3, 'Verde'),
    ('Parque', 'Hospital', 3, 'Verde'), ('Hospital', 'Sur', 3, 'Verde'),
]

@dataclass(frozen=True)
class Ruta:
    estaciones: list[str]
    lineas: list[str]
    minutos: float


def crear_grafo(conexiones=CONEXIONES):
    grafo = {estacion: [] for estacion in ESTACIONES}
    for origen, destino, minutos, linea in conexiones:
        if origen not in ESTACIONES or destino not in ESTACIONES:
            raise ValueError('Estación desconocida en las conexiones')
        if not math.isfinite(minutos) or minutos < 0:
            raise ValueError('Los tiempos deben ser finitos y no negativos')
        grafo[origen].append((destino, minutos, linea))
        grafo[destino].append((origen, minutos, linea))
    return grafo


def mejor_ruta(origen, destino, penalizacion=2, grafo=None):
    """Devuelve una Ruta mínima o None si el destino está desconectado.

    Usa distancia euclidiana cuando todos los tramos la acotan por debajo.
    Si un grafo modificado incumple esa condición, usa h=0 (Dijkstra).
    """
    if origen not in ESTACIONES or destino not in ESTACIONES:
        raise ValueError('Estación desconocida; consulta --estaciones')
    if not math.isfinite(penalizacion) or penalizacion < 0:
        raise ValueError('La penalización debe ser finita y no negativa')
    if grafo is None:
        grafo = crear_grafo()
    geometrica = True
    for estacion, vecinos in grafo.items():
        if estacion not in ESTACIONES:
            raise ValueError('Estación desconocida en el grafo')
        for vecino, minutos, _ in vecinos:
            if vecino not in ESTACIONES:
                raise ValueError('Estación desconocida en el grafo')
            if not math.isfinite(minutos) or minutos < 0:
                raise ValueError('Los tiempos deben ser finitos y no negativos')
            if minutos < math.dist(ESTACIONES[estacion], ESTACIONES[vecino]):
                geometrica = False
    def heuristica(estacion):
        return math.dist(ESTACIONES[estacion], ESTACIONES[destino]) if geometrica else 0
    inicial = (origen, None)
    costos = {inicial: 0}
    anteriores = {}
    orden = count()
    pendientes = [(heuristica(origen), next(orden), 0, inicial)]
    while pendientes:
        _, _, costo, estado = heapq.heappop(pendientes)
        if costo != costos[estado]:
            continue
        estacion, linea_actual = estado
        if estacion == destino:
            estados = [estado]
            while estados[-1] in anteriores:
                estados.append(anteriores[estados[-1]])
            estados.reverse()
            return Ruta([e[0] for e in estados], [e[1] for e in estados[1:]], costo)
        for vecino, minutos, linea in grafo.get(estacion, []):
            cambio = penalizacion if linea_actual is not None and linea_actual != linea else 0
            nuevo_costo = costo + minutos + cambio
            siguiente = (vecino, linea)
            if nuevo_costo < costos.get(siguiente, math.inf):
                costos[siguiente] = nuevo_costo
                anteriores[siguiente] = estado
                heapq.heappush(pendientes, (nuevo_costo + heuristica(vecino), next(orden), nuevo_costo, siguiente))
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('origen', nargs='?')
    parser.add_argument('destino', nargs='?')
    parser.add_argument('--estaciones', action='store_true')
    parser.add_argument('--penalizacion', type=float, default=2)
    args = parser.parse_args()
    if args.estaciones:
        print('\n'.join(ESTACIONES))
        return
    if args.origen is None or args.destino is None:
        parser.error('Debes indicar origen y destino')
    try:
        ruta = mejor_ruta(args.origen, args.destino, args.penalizacion)
    except ValueError as error:
        parser.error(str(error))
    if ruta is None:
        print('Sin ruta')
    else:
        print('Ruta: ' + ' - '.join(ruta.estaciones))
        print('Líneas: ' + (', '.join(ruta.lineas) or 'Sin recorrido'))
        print(f'Tiempo simulado: {ruta.minutos:g} minutos')

if __name__ == '__main__':
    main()
