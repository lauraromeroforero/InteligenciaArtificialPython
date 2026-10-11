import unittest
from rutas import crear_grafo, mejor_ruta

class PruebasRutas(unittest.TestCase):
    def test_ruta_directa(self):
        ruta = mejor_ruta('Portal', 'Centro')
        self.assertEqual(ruta.estaciones, ['Portal', 'Norte', 'Centro'])
        self.assertEqual(ruta.lineas, ['Azul', 'Azul'])
        self.assertEqual(ruta.minutos, 8)

    def test_transbordo_y_optimo(self):
        ruta = mejor_ruta('Portal', 'Sur')
        self.assertEqual(ruta.estaciones, ['Portal', 'Norte', 'Occidente', 'Parque', 'Hospital', 'Sur'])
        self.assertEqual(ruta.lineas, ['Azul', 'Verde', 'Verde', 'Verde', 'Verde'])
        self.assertEqual(ruta.minutos, 18)

    def test_mismo_origen_destino(self):
        ruta = mejor_ruta('Centro', 'Centro')
        self.assertEqual(ruta.estaciones, ['Centro'])
        self.assertEqual(ruta.lineas, [])
        self.assertEqual(ruta.minutos, 0)

    def test_desconocida(self):
        with self.assertRaisesRegex(ValueError, 'Estación desconocida'):
            mejor_ruta('Inventada', 'Centro')

    def test_inalcanzable(self):
        grafo = crear_grafo()
        grafo['Sur'] = []
        for estacion in grafo:
            grafo[estacion] = [tramo for tramo in grafo[estacion] if tramo[0] != 'Sur']
        self.assertIsNone(mejor_ruta('Portal', 'Sur', grafo=grafo))

    def test_penalizacion(self):
        self.assertEqual(mejor_ruta('Portal', 'Sur', penalizacion=0).minutos, 16)

if __name__ == '__main__':
    unittest.main()
