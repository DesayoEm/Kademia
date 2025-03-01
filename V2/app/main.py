from fastapi import Depends, FastAPI
from .routers.staff_organization import educator_qualifications

version = "v1"
app = FastAPI(
    version = version,
    title = "TraKademik"
)

app.include_router(educator_qualifications.router, prefix=f"/api/{version}/staff/qualifications",
                   tags=["Qualifications"])


@app.get("/")
async def root():
    return {"message": "Welcome to TraKademik!"}