import csv
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from agrupamiento import agrupar, cargar_datos
BASE = Path(__file__).resolve().parents[1]

class PruebasAgrupamiento(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ids, cls.X, cls.etiquetas, cls.resumen = agrupar(BASE/'datos/viajes_sin_etiquetas.csv')

    def test_datos_sin_etiquetas(self):
        self.assertEqual(self.X.shape, (600, 6))
        self.assertEqual(len(set(self.ids)), 600)
        self.assertNotIn('tiempo_min', self.resumen['variables'])
        self.assertNotIn('id_viaje', self.resumen['variables'])

    def test_asignacion_y_perfiles(self):
        self.assertEqual(len(self.etiquetas), 600)
        self.assertEqual(len(np.unique(self.etiquetas)), self.resumen['k_elegido'])
        self.assertEqual(sum(p['cantidad'] for p in self.resumen['perfiles']), 600)
        self.assertTrue(all(p['cantidad'] > 0 for p in self.resumen['perfiles']))

    def test_seleccion_silueta(self):
        mejor = max(self.resumen['candidatos'], key=lambda c: c['silueta'])
        self.assertEqual(self.resumen['k_elegido'], mejor['k'])
        self.assertTrue(-1 <= self.resumen['silueta_elegida'] <= 1)

    def test_reproducibilidad(self):
        _, _, etiquetas, _ = agrupar(BASE/'datos/viajes_sin_etiquetas.csv')
        np.testing.assert_array_equal(self.etiquetas, etiquetas)

    def test_rechaza_columnas_faltantes(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'invalido.csv'; p.write_text('id_viaje\n1\n')
            with self.assertRaisesRegex(ValueError, 'columnas'):
                cargar_datos(p)

    def test_rechaza_valor_invalido(self):
        with tempfile.TemporaryDirectory() as d:
            with (BASE/'datos/viajes_sin_etiquetas.csv').open(newline='') as f:
                r = csv.DictReader(f); campos = r.fieldnames; filas = list(r)
            filas[0]['ocupacion_pct'] = '120'
            p = Path(d)/'invalido.csv'
            with p.open('w', newline='') as f:
                w = csv.DictWriter(f, fieldnames=campos); w.writeheader(); w.writerows(filas)
            with self.assertRaisesRegex(ValueError, 'dominio'):
                cargar_datos(p)

if __name__ == '__main__':
    unittest.main()
