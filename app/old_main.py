import os
from fastapi import FastAPI
from .routers import recipes, main
from .repo import create_repository
from dotenv import load_dotenv


class SmallAPI(FastAPI):

    def __init__(self):
        super().__init__()
        self._repository = None

    def setup_repository(self) -> None:
        self._repository = create_repository()

    def setup_config(self) -> None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        load_dotenv(os.path.join(basedir, "../.env"))

    def add_router(self):
        self.include_router(recipes.router)
        self.include_router(main.router)

    def connect_db(self):
        return self._repository

    def setup(self) -> None:
        super().setup()
        self.setup_config()
        self.setup_repository()
        self.add_router()


def create_app() -> SmallAPI:
    smallApi = SmallAPI()
    smallApi.setup()
    return smallApi


app = create_app()

