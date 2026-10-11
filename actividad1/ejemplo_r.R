# Instalar previamente con install.packages("rpart") si no está disponible.
library(rpart)
modelo <- rpart(
  Species ~ Sepal.Length + Sepal.Width + Petal.Length + Petal.Width,
  data = iris,
  method = "class"
)
print(modelo)
prediccion <- predict(modelo, iris[1, , drop = FALSE], type = "class")
print(prediccion)
stopifnot(as.character(prediccion[1]) == "setosa")
