from typing import List, Optional
from pydantic import BaseModel


class MsgPayload(BaseModel):
    msg_id: Optional[int]
    msg_name: str

class Buzz(BaseModel):
    Title: Optional[str] = None
    Description: Optional[str] = None
    Content: Optional[str] = None

class KeywordExtractRequest(BaseModel):
    data: List[Buzz]
    category: str
    min_freq: Optional[int] = 10