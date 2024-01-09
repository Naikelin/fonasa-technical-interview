# README

## Fonasa Inexoos API

### Introducción

Bienvenido a la API Fonasa Inexoos, una Flask RESTful API para gestionar registros de pacientes, información hospitalaria, consultas y una cola de espera. Esta API proporciona puntos finales para manipular pacientes, consultas, hospitales y una cola de espera global.

### Ejecución

```bash
docker compose up -d
```

## Funcionalidades de la API Fonasa

1. **Pacientes:**

   - Obtener todos los pacientes.
   - Agregar un nuevo paciente.

2. **Consultas:**

   - Obtener todas las consultas.
   - Agregar una nueva consulta.
   - Liberar consulta por ID.
   - Liberar todas las consultas.
   - Obtener consultas activas.

3. **Hospitales:**

   - Obtener todos los hospitales.
   - Agregar un nuevo hospital.

4. **Cola de Espera:**
   - Obtener la cola de espera.
   - Atender a un paciente.
   - Optimizar atención.

Para más detalles sobre los parámetros y formatos de solicitud, consulta la documentación de la API generada por Swagger en `http://localhost:5000/swagger` cuando la aplicación esté en ejecución.

## Comentarios

- Lo más común es utilizar una cola para los pacientes. El problema se pensó como que los pacientes recolectan sus datos a lo largo del tiempo en la tabla, mientras que su espera en las salas se realiza a través de una cola que en este caso es volatil, pero que podría ser persistente utilizando otras tecnologías.
- El problema es muy largo, por lo que no está optimizado de manera general, pero se le dio enfasis a los modelos del ORM.
