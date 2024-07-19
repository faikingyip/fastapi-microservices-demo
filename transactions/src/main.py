from src.app import app, config_db, config_rmq, load_env

load_env()
config_db()
config_rmq()
