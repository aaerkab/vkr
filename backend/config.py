import os

class Config:
    # Можно задать одной переменной окружения, например:
    # DATABASE_URL=sqlite:///security.db
    # DATABASE_URL=mysql+pymysql://user:pass@host:3306/dbname
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        (
            f"mysql+pymysql://{os.getenv('DB_USER', 'root')}:"
            f"{os.getenv('DB_PASSWORD', '12345')}@"
            f"{os.getenv('DB_HOST', 'localhost')}:"
            f"{os.getenv('DB_PORT', '3306')}/"
            f"{os.getenv('DB_NAME', 'security_analysis')}"
        ),
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
