import os 

# Configuración por defecto para MySQL local en XAMPP
DB_HOST     = os.getenv("DB_HOST", "localhost")
DB_PORT     = os.getenv("DB_PORT", "3306")       # El puerto por defecto de MySQL es 3306
DB_USER     = os.getenv("DB_USER", "root")        # Usuario administrador de XAMPP por defecto
DB_PASSWORD = os.getenv("DB_PASSWORD", "")        # XAMPP viene sin contraseña por defecto
DB_NAME     = os.getenv("DB_NAME", "hotel_local")

# Cambiamos la URL para usar el driver mysql+pymysql
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"