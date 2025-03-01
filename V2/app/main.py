from fastapi import Depends, FastAPI
from .routers.staff_organization import (
    educator_qualifications, staff_departments, staff_roles
)

version = "v1"
app = FastAPI(
    version = version,
    title = "TraKademik"
)

app.include_router(educator_qualifications.router, prefix=f"/api/{version}/staff/qualifications",
                   tags=["Qualifications"])
app.include_router(staff_departments.router, prefix=f"/api/{version}/staff/departments",
                   tags=["Staff Departments"])
app.include_router(staff_roles.router, prefix=f"/api/{version}/staff/roles",
                   tags=["Staff Roles"])


@app.get("/")
async def root():
    return {"message": "Welcome to TraKademik!"}