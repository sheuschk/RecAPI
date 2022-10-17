import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join("../", basedir, "../.env"))
if os.environ.get("TEST") == "False":
    DATABASE_META = {
        "TYPE": os.environ.get("DB_TYPE", "sqlite"),
        "URL": os.environ.get("DB_URL", "mydb.db")
    }
else:
    DATABASE_META = {
        "TYPE": "sqlite",
        "URL": "test.db"
    }

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"
