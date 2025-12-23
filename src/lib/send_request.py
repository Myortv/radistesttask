import logging

from typing import (
    Optional,
    Protocol,
    ParamSpec,
    Any,
    Union,
    List,
    Dict
)


import httpx

from fastapi.exceptions import HTTPException


from src.core.configs import configs


P = ParamSpec("P")


def setup_headers() -> dict:
    return {
        "X-API-KEY": configs.RETAIL_CRM_API_KEY,
    }


def build_params(
    *args,
    **kwargs,
) -> dict:
    output_params = dict()
    for arg in args:
        for key, value in arg.items():
            if value:
                output_params[key] = value
    for key, value in kwargs.items():
        if value:
            output_params[key] = value

    return output_params


class Client(Protocol):
    @staticmethod
    async def request(
        *args,
        params: Optional[dict] = ...,
        headers: Optional[dict] = ...,
        data: Optional[dict] = ...,
        **kwargs,
    ) -> Union[Dict[str, Any], List[Any]]:
        ...


class HttpxClient(Client):
    @staticmethod
    async def request(
        *args,
        params: Optional[dict] = None,
        headers: Optional[dict] = None,
        **kwargs,
    ) -> Union[Dict[str, Any], List[Any]]:
        default_headers = setup_headers()
        if headers:
            default_headers.update(headers)

        async with httpx.AsyncClient() as client:
            response = await client.request(
                *args,
                params=params,
                headers=default_headers,
                **kwargs,
            )
            if response.status_code not in {200, 201}:
                logging.debug(response.text)
                raise HTTPException(
                    status_code=response.status_code,
                )
            json_output = response.json()
            return json_output


def client_dependency():
    return HttpxClient
