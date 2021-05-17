from playhouse.db_url import connect

USER_NAME = "amir"

PASSWORD = "1234"

db = connect(f"mysql://{USER_NAME}:{PASSWORD}@127.0.0.1:3306/jobinja")


