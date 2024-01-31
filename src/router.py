import traceback
from typing import Any, Annotated

from fastapi import APIRouter, HTTPException, Response, status, Depends
from starlette.requests import Request

from src.services import serialize, deserialize

router = APIRouter()


class OctetStreamResponse(Response):
    media_type = "application/octet-stream"


@router.post(
    '/serialize',
    description='Receives any valid json like object. Returns bytes.',
    response_class=OctetStreamResponse
)
async def serialize_data(json: dict[str, Any]) -> OctetStreamResponse:
    try:
        serialized_data = serialize(json)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return OctetStreamResponse(serialized_data)


async def parse_body(request: Request) -> bytes:
    return await request.body()


@router.post(
    '/deserialize',
    description='Receives bytes. Returns json.'
)
def deserialize_data(data: Annotated[bytes, Depends(parse_body)]) -> dict:
    try:
        deserialized_data = deserialize(data)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return deserialized_data
