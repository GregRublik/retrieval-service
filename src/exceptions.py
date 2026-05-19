class APIException(Exception):
    def __init__(self, status_code: int, error: str):
        self.status_code = status_code
        self.error = error

class QdrantCollectionNotFoundException(Exception):
    """Коллекция не найдена"""

    detail = "Collection not found exception"
