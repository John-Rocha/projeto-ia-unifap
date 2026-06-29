from fastapi import HTTPException


class TopicNotFoundError(HTTPException):
    def __init__(self, topic_id: str):
        super().__init__(status_code=404, detail=f"Topic '{topic_id}' not found")
