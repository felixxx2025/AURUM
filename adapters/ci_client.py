"""Client responsible for interacting with a CI system."""
from __future__ import annotations


class CIClientError(Exception):
    """Raised when an operation with the CI system fails."""


class CIClient:
    def get_status(self, pr_id: str) -> str:
        """Return the status of a pull request.

        This stub implementation simply returns ``"unknown"``.
        """
        if not pr_id:
            raise CIClientError("pr_id is required")
        return "unknown"
