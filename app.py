from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List
import json
import os

## Base de datos
DATABASE_FILE = "tareas.txt"

class Tarea(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    due_date: str

def load_tareas():
    if not os.path.exists(DATABASE_FILE):
        return []
    with open(DATABASE_FILE, "r") as file:
        try:
            return [Tarea(**json.loads(line)) for line in file.readlines()]
        except json.JSONDecodeError:
            return []

def save_tareas(tareas: List[Tarea]):
    with open(DATABASE_FILE, "w") as file:
        for tarea in tareas:
            file.write(tarea.json() + "\n")

def add_tarea(tarea: Tarea):
    tareas = load_tareas()
    tareas.append(tarea)
    save_tareas(tareas)

def update_tarea(id: int, updated_tarea: Tarea):
    tareas = load_tareas()
    for index, tarea in enumerate(tareas):
        if tarea.id == id:
            tareas[index] = updated_tarea
            save_tareas(tareas)
            return True
    return False

## Servidor Web
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def tareas(request: Request):
    tareas = load_tareas()
    return templates.TemplateResponse(name="index.html", context={"request": request, "tareas": tareas})

@app.get("/crear", response_class=HTMLResponse)
async def tareas_crear(request: Request):
    return templates.TemplateResponse(name="modulos/tareas/crear_tarea.html", context={"request": request})

@app.post("/crear/guardar")
async def tareas_crear_guardar(
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    due_date: str = Form(...)
):
    tareas = load_tareas()
    new_tarea = Tarea(
        id=len(tareas) + 1,
        title=title,
        description=description,
        completed=(status == "completed"),
        due_date=due_date
    )
    add_tarea(new_tarea)
    return RedirectResponse(url="/", status_code=303)

## Nuevo endpoint para actualizar tarea
@app.get("/{id}/actualizar", response_class=HTMLResponse)
async def tareas_actualizar(request: Request, id: int):
    tareas = load_tareas()
    tarea = next((t for t in tareas if t.id == id), None)
    if not tarea:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse(
        name="modulos/tareas/actualizar_tarea.html", 
        context={"request": request, "tarea": tarea}
    )

@app.post("/{id}/actualizar/guardar")
async def tareas_actualizar_guardar(
    id: int,
    title: str = Form(...),
    description: str = Form(...),
    status: str = Form(...),
    due_date: str = Form(...)
):
    updated_tarea = Tarea(
        id=id,
        title=title,
        description=description,
        completed=(status == "completed"),
        due_date=due_date
    )
    if update_tarea(id, updated_tarea):
        return RedirectResponse(url="/", status_code=303)
    return {"error": "Tarea no encontrada"}

@app.get("/{id}/leer")
async def tareas_leer(request: Request, id: int):
    # Load tasks from the database
    tareas = load_tareas()
    
    # Find the task with the given id
    tarea = next((t for t in tareas if t.id == id), None)
    
    if tarea is None:
        return RedirectResponse(url="/", status_code=303)
    
    # Render the 'leer_tarea.html' template with the task data
    return templates.TemplateResponse("modulos/tareas/ver_tarea.html", {
        "request": request,
        "tarea": tarea
    })