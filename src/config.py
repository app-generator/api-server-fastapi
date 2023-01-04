from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = 'dbhostname'
    database_port: int = 5432
    database_password: str = 'dbpassword'
    database_name: str = 'dbname'
    database_username: str = 'dbuser'
    secret_key: str = 'sup3r_secr3t'
    algorithm: str = 'HS256'
    debugging: bool = True
    access_token_expire_minutes: int = 30

    class Config:
        env_file = "./.env"


settings = Settings()