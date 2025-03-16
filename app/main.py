from fastapi import FastAPI, Request
from sqlmodel import SQLModel
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles


import api, auth, kontrol
from database import engine



middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

templates = Jinja2Templates(directory="templates")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

app = FastAPI(middleware=middleware, title='Face Recognition', description='Face recognition using OpenCV and FastAPI', docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(api.router, tags=["API"], prefix="/api")
app.include_router(auth.router, tags=["AUTH"], prefix="/auth")
app.include_router(kontrol.router, tags=["kontrol"], prefix="/kontrol")

create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/ports", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("ports.html", {"request": request})


@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, reload=True)
