# tareas_crud
# Task Management API with FastAPI
Aplicacion para el manejo de una base de datos de tareas

## Endpoints
### Lista de tareas
- **URL**: `/`
- **Descripcion**: Muestra la lista de tareas desde el txt.

### Crear
- **URL**: `/crear`
- **Descripcion**: Permite crear una nueva tarea llenando los campos.

### Guardar Tarea
- **URL**: `/crear/guardar`
- **Descripcion**: Guarda la tarea creada.

### Actualizar Tarea
- **URL**: `/{id}/actualizar`
- **Descripcion**: Permite actualizar una tarea seleccionada.

### Actualizar Tarea Guardar
- **URL**: `/{id}/actualizar/guardar`
- **Descripcion**: Actualiza las tareas con las modificaciones.

### Ver Tarea
- **URL**: `/{id}/leer`
- **Descripcion**: Permite ver la descripcion de la tarea.

## Correar la aplicacion

Clonar el repositorio con el siguiente comando
git clone https://github.com/MAlvites/tareas_crud.git
Ejecutar el siguiente comando en la carpeta del repositorio
uvicorn app:app --reload

## Requerimientos
fastapi 

