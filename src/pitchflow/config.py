from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="PITCHFLOW_")

    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "pitchflow"
    db_user: str = "pitchflow"
    db_password: str = ""
    data_dir: str = "data"
    log_level: str = "INFO"

    @property
    def db_dsn(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
