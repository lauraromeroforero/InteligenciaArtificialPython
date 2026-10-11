"""Ejemplo KNN descrito en la actividad 1."""
from sklearn.neighbors import KNeighborsClassifier

X = [[1], [2], [3], [8], [9], [10]]
y = ['Bajo', 'Bajo', 'Bajo', 'Alto', 'Alto', 'Alto']
modelo = KNeighborsClassifier(n_neighbors=3)
modelo.fit(X, y)
resultado = modelo.predict([[7]])
print('Predicción:', resultado[0])
assert resultado[0] == 'Alto'
