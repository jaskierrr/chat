from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseModel):
    host: str
    port: int = 8080


class PostgresDBSettings(BaseModel):
    dsn: PostgresDsn


class RedisSettings(BaseModel):
    host: str
    port: int
    db: int


class PasswordSettings(BaseModel):
    salt: str


class AuthSettings(BaseModel):
    secret: str
    ttl: int


class Config(BaseSettings):
    db: PostgresDBSettings
    cache: RedisSettings
    server: ServerSettings
    password: PasswordSettings
    auth: AuthSettings
    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=[".env"])


config = Config()
