from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Simple Todo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=500)
    done: bool | None = None
    


class Todo(BaseModel):
    id: int
    title: str
    done: bool


_todos: list[Todo] = []
_next_id = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/todos", response_model=list[Todo])
def list_todos():
    return list(_todos)


@app.post("/todos", response_model=Todo, status_code=201)
def create_todo(body: TodoCreate):
    global _next_id
    todo = Todo(id=_next_id, title=body.title.strip(), done=False)
    _next_id += 1
    _todos.append(todo)
    return todo


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, body: TodoUpdate):
    for i, t in enumerate(_todos):
        if t.id == todo_id:
            data = t.model_dump()
            if body.title is not None:
                data["title"] = body.title.strip()
            if body.done is not None:
                data["done"] = body.done
            updated = Todo(**data)
            _todos[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    for i, t in enumerate(_todos):
        if t.id == todo_id:
            _todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")

@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for t in _todos:
        if t.id == todo_id:
            return t
    raise HTTPException(status_code=404, detail="Todo not found")
