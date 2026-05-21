from pydantic import BaseModel

class Chunk(BaseModel):
    text: str
    source_url: str
    title: str
