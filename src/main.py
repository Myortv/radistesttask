from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware


from src.core.configs import configs, tags_metadata

app = FastAPI(
    title=configs.PROJECT_NAME,
    version='0.0.1',
    docs_url=configs.DOCS_URL,
    openapi_tags=tags_metadata,
    openapi_url=f'{configs.API_V1_STR}/openapi.json',
)

if configs.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in configs.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


from src.api import (
    client,
    order,
    payment,
)

app.include_router(
    client.api,
    prefix=configs.API_V1_STR + '/client',
    tags=["Client"]
)

app.include_router(
    order.api,
    prefix=configs.API_V1_STR + '/order',
    tags=["Order"]
)
app.include_router(
    payment.api,
    prefix=configs.API_V1_STR + '/payment',
    tags=["Payment"]
)


