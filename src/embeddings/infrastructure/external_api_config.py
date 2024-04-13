from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ExternalApiConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='EXTERNAL_API_')

    OPENAI_TOKEN: str = Field(...)
    OPENAI_MODEL: str = Field("text-embedding-3-large")


external_api_config = ExternalApiConfig()
