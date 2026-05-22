# Los datos de aquí son de la URI que nos da Supabase
import os 

DB_HOST     = os.getenv("DB_HOST", "db.beswgvmlplhdcoihwbyk.supabase.co")
DB_PORT     = os.getenv("DB_PORT", "5432")
DB_USER     = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "API.Kegovc.")
DB_NAME     = os.getenv("DB_NAME", "postgres")

DB_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"