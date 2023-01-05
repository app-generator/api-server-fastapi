from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str = 'dbhostname'
    database_port: int = 5432
    database_password: str = 'dbpassword'
    database_name: str = 'dbname'
    database_username: str = 'dbuser'

    github_secret_key: str = None
    github_client_id: str = None
    github_is_active: bool = False

    secret_key: str = 'sup3r_secr3t'
    algorithm: str = 'HS256'
    debugging: bool = True
    access_token_expire_minutes: int = 30


    def __init__(self):
        super().__init__()
        self.check_github()

    def check_github(self):
        if self.github_secret_key and self.github_client_id:
            self.github_is_active = True


    class Config:
        env_file = "./.env"


settings = Settings()