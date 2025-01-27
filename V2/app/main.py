from fastapi import Depends, FastAPI
from .routers import students
from .routers import parents
from .routers import staff

version = "v1"
app = FastAPI(
    version = version,
    title = "TraKademik"
)

app.include_router(students.router, prefix=f"/api/{version}/students",tags=["students"])
app.include_router(parents.router, prefix=f"/api/{version}/parents",tags=["parents"])
app.include_router(staff.router, prefix=f"/api/{version}/staff",tags=["staff"])

@app.get("/")
async def root():
    return {"message": "Welcome to TraKademik!"}