from fastapi import Depends, FastAPI
from .routers.students import students
from .routers.students import students_archive
from .routers import parents
from .routers import staff

version = "v1"
app = FastAPI(
    version = version,
    title = "TraKademik"
)

app.include_router(students.router, prefix=f"/api/{version}/students",tags=["Students"])
app.include_router(students_archive.router, prefix=f"/api/{version}/students/archives",
                   tags=["Student Archives"])

app.include_router(parents.router, prefix=f"/api/{version}/parents",tags=["Parents"])
app.include_router(staff.router, prefix=f"/api/{version}/staff",tags=["Staff"])

@app.get("/")
async def root():
    return {"message": "Welcome to TraKademik!"}