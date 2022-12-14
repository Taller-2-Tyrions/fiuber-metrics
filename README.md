[![codecov](https://codecov.io/gh/Taller-2-Tyrions/fiuber-metrics/branch/main/graph/badge.svg?token=pqpC5Y9JiG)](https://codecov.io/gh/Taller-2-Tyrions/fiuber-metrics)

# Fiuber-Metrics
Microservicio para obtener metricas de la plataforma.

Los mensajes sobre uso de la plataforma son encolados en una cola de Rabbit. Los mismos son consumidos por el microservicio quien los procesa e inserta en una base de datos Mongo. Se accede a los datos mediante consultas a la API.

# Documentación
Documentación técnica: https://taller-2-tyrions.github.io/fiuber-documentation-tecnica/

## Uso del API

### Obtener metricas de usuarios
```
curl --location --request GET 'http://localhost:8000/metrics/users' \
--data-raw ''
```

### Obtener metricas de viajes
```
curl --location --request GET 'http://localhost:5001/metrics/voyages' \
--data-raw ''
```
### Obtener metricas de pagos
```
curl --location --request GET 'http://localhost:8000/metrics/payments' \
--data-raw ''
```
