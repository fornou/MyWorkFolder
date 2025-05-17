from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    INIT_DB_AT_STARTUP:  bool = Field(default=True)
    METABASE_SITE_URL: str 
    METABASE_SECRET_KEY: str
    UPLOAD_FOLDER: str = "uploads" 

    @property
    def db_url(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = "allow"

# istanza condivisa
settings = Settings()
