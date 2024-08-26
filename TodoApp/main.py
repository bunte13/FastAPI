from tempfile import template
from urllib import request

from fastapi import FastAPI,Request,status
from starlette.status import HTTP_302_FOUND

from TodoApp.routers import auth,todos,admin,users

from fastapi.staticfiles import StaticFiles
import TodoApp.models
from TodoApp.database import engine
from fastapi.responses import RedirectResponse
app = FastAPI()

TodoApp.models.Base.metadata.create_all(bind=engine)



app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page",status_code=HTTP_302_FOUND)


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
