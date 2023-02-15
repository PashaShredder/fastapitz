from fastapi import FastAPI
from api.utils.dbUtil import database
from api.auth import router as auth_router
from api.otps import router as otp_router
from api.report import report_users, report_otps

app = FastAPI(
    docs_url="/docs",
    redoc_url="/redocs",
    title="FastAPI",
    version="1.0",
    openapi_url="/openapi.json"
)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(auth_router.router, tags=["Auth"])
app.include_router(otp_router.router, tags=["OTPs"])
app.include_router(report_users.report, tags=["Report"])
app.include_router(report_otps.report, tags=["Report"])
