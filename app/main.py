from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from .repo import create_repository
from .routers import main
from .config import DATABASE_META

# start vie CLI in small API folder: uvicorn app.main:app --reload
# --> otherwise relative imports don't work

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


# TODO: connections in db commands
# @app.on_event("startup")
# async def startup():
    # db.connect()


# @app.on_event("shutdown")
# async def shutdown():
#    db.disconnect()


# Global Application error Handling
async def catch_exceptions_middleware(request: Request, call_next):
    # Alternative: Define a Custom Router, which extends the requested route with a try except
    try:
        return await call_next(request)
    except Exception as e:
        print(f"Global Error: {e}")
        return Response("Internal server error", status_code=500)
# app.middleware('http')(catch_exceptions_middleware)

origins = ["http://127.0.0.1:5173", "http://localhost", "http://localhost:8080"]
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_headers=["*"],
                   allow_methods=["*"])

# Router
app.include_router(main.router)
