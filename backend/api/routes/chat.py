from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=10000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    application: str
    message: str
    response: str
    status: str


@router.post("/")
async def chat(request: ChatRequest):

    return ChatResponse(
        application="NEXUS AI",
        message=request.message,
        response=(
            "Your message has been received successfully. "
            "The OpenAI intelligence engine will be connected "
            "in the next integration phase."
        ),
        status="received"
    )
