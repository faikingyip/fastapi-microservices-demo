from src.app import app, config_db, config_rmq, load_env

# from src import app

load_env()
config_db()
config_rmq()
