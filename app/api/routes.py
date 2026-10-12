
from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.assistant_service import process_command

router = APIRouter()


class CommandRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "assistant": "REX",
    }


@router.post("/command")
async def handle_command(request: CommandRequest):
    result = await process_command(request.text)
    return result.model_dump()
