from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class CaseRepository(ABC):
    """Abstract repository interface for NutriOK cases, reviews, payments, events, and sessions."""

    @abstractmethod
    def save_case(self, submission_id: str, payload: dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_case(self, submission_id: str) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    def list_cases(
        self,
        *,
        user_id: int | None = None,
        status: str | None = None,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def append_review(
        self,
        submission_id: str,
        *,
        reviewer_id: int,
        decision: str,
        decided_at: str,
        artifact_sha256: str = "",
        notes: str = "",
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def list_reviews(self, submission_id: str) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def append_payment(
        self,
        submission_id: str,
        *,
        amount_rub: int,
        mode: str,
        status: str,
        at: str,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def append_event(
        self,
        *,
        actor_id: int,
        submission_id: str | None,
        kind: str,
        data: dict[str, Any] | None = None,
        at: str | None = None,
    ) -> int:
        raise NotImplementedError

    @abstractmethod
    def save_sessions(
        self,
        user_sessions: dict[int, dict[str, Any]],
        chat_sessions: dict[int, list[dict[str, str]]],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_sessions(self) -> dict[str, Any]:
        raise NotImplementedError
