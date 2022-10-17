from fastapi import FastAPI, Request, Response

from .repo import create_repository
from .routers import recipes, main
from .config import DATABASE_META

# TODO's
# Input validation
# Logging
# Database connection improvement (asynchronous, stable, safe)
# datetime Format without milliseconds
# SQL Server Repo Interface Implementation additionally to sqlite
# (flask 8 checks)

app = FastAPI()


# Database Handling
db = create_repository(DATABASE_META)
app.db = db


@app.on_event("startup")
async def startup():
    db.connect()


@app.on_event("shutdown")
async def shutdown():
    db.disconnect()


# Global Application error Handling
async def catch_exceptions_middleware(request: Request, call_next):
    # Alternative: Define a Custom Router, which extends the requested route with a try except
    try:
        return await call_next(request)
    except Exception as e:
        print(f"Global Error: {e}")
        return Response("Internal server error", status_code=500)
app.middleware('http')(catch_exceptions_middleware)


# Router
app.include_router(recipes.router)
app.include_router(main.router)
