from playhouse.db_url import connect
from mysql_config import USER_NAME, PASSWORD, DATABASE_NAME

db = connect(f"mysql://{USER_NAME}:{PASSWORD}@127.0.0.1:3306/{DATABASE_NAME}")
