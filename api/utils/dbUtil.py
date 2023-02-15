import databases
import sqlalchemy
from api.models import metadata
from starlette.config import Config



# 2. using starlette to load .env config file
def database_pgsql_url_config():
    conf = Config(".env")
    return str(conf("DB_CONNECTION") + "://" + conf("DB_USERNAME") + ":" + conf("DB_PASSWORD") +
               "@" + conf("DB_HOST") + ":" + conf("DB_PORT") + "/" + conf("DB_DATABASE"))

database = databases.Database(database_pgsql_url_config())
engine = sqlalchemy.create_engine(database_pgsql_url_config())
metadata.create_all(engine)
