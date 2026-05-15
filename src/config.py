from pydantic_settings import SettingsConfigDict, BaseSettings


class SearXNGSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SEARXNG_", extra="ignore")


class VDBSettings(BaseSettings):
    host: str
    port: int
    embedding_model: str
    device: str
    collection_name: str

    model_config = SettingsConfigDict(env_file=".env", env_prefix="VDB_", extra="ignore")


class Settings(BaseSettings):
    port: int
    host: str

    vdb: VDBSettings
    searxng: SearXNGSettings

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")


settings = Settings(
    vdb=VDBSettings(),
    searxng=SearXNGSettings(),
)
