from typing import List, Protocol, TypeVar


class ScoredItem(Protocol):
    score: float


T = TypeVar("T", bound=ScoredItem)


class RerankerService:

    @staticmethod
    def rerank(items: List[T], top_k: int | None = None) -> List[T]:
        """Re-rank items by score descending."""
        ranked = sorted(items, key=lambda x: x.score, reverse=True)
        if top_k is not None:
            return ranked[:top_k]
        return ranked
