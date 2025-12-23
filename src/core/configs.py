import logging
from typing import List, Optional

from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DEBUG: Optional[bool] = False
    TEST: Optional[bool] = False

    PROJECT_NAME: str = "Radis RetailCRM test task"
    API_V1_STR: str = "/api"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = ["http://localhost"]
    DOCS_URL: str = "/docs"
    ROOT_PATH: str = ""

    RETAIL_CRM_API_KEY: str
    # key from https://retailcrm.ru/admin/api-keys
    RETAIL_CRM_HOST: str

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


configs = Settings()

if configs.DEBUG:
    logging.basicConfig(level=logging.DEBUG)


tags_metadata = [
    {
        "name": "Client",
        "description": "Client endpoints for RetailCRM",
    },
    {
        "name": "Order",
        "description": "Order endpoints for RetailCRM",
    },
    {
        "name": "Payment",
        "description": "Payment endpoints for RetailCRM",
    },
]
