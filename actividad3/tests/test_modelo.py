import csv
import sys
import tempfile
import unittest
from pathlib import Path
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from generar_datos import generar
from modelo_transporte import cargar_datos, entrenar

class PruebasModelo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modelo, cls.resumen, cls.reales, cls.predicciones = entrenar(
            Path(__file__).resolve().parents[1] / 'datos/viajes_simulados.csv')

    def test_particion_y_variables(self):
        self.assertEqual(self.resumen['filas_entrenamiento'], 480)
        self.assertEqual(self.resumen['filas_prueba'], 120)
        self.assertEqual(self.modelo.n_features_in_, 6)
        self.assertNotIn('tiempo_min', self.resumen['variables'])
        self.assertNotIn('id_viaje', self.resumen['variables'])

    def test_supera_baseline(self):
        self.assertLess(self.resumen['arbol_prueba']['mae_min'],
                        self.resumen['baseline_prueba']['mae_min'])

    def test_predicciones_validas(self):
        self.assertEqual(len(self.predicciones), 120)
        self.assertTrue(np.all(np.isfinite(self.predicciones)))
        self.assertTrue(np.all(self.predicciones > 0))

    def test_generacion_reproducible(self):
        with tempfile.TemporaryDirectory() as d:
            a = generar(Path(d)/'a.csv')
            b = generar(Path(d)/'b.csv')
            self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_rechaza_columna_faltante(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = Path(d)/'invalido.csv'
            ruta.write_text('distancia_km,tiempo_min\n10,20\n')
            with self.assertRaisesRegex(ValueError, 'columnas'):
                cargar_datos(ruta)

    def test_rechaza_valor_invalido(self):
        with tempfile.TemporaryDirectory() as d:
            ruta = generar(Path(d)/'invalido.csv')
            with ruta.open(newline='') as f:
                reader = csv.DictReader(f)
                campos = reader.fieldnames
                filas = list(reader)
            filas[0]['hora_pico'] = '2'
            with ruta.open('w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader(); writer.writerows(filas)
            with self.assertRaisesRegex(ValueError, 'dominio'):
                cargar_datos(ruta)

if __name__ == '__main__':
    unittest.main()
