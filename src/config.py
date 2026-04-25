from pydantic_settings import SettingsConfigDict, BaseSettings

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

    model_config = SettingsConfigDict(env_file=".env", env_prefix="APP_", extra="ignore")


settings = Settings(
    vdb=VDBSettings(),
)
