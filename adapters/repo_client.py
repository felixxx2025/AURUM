"""Client responsible for interacting with a git repository."""
from __future__ import annotations

from pathlib import Path


class RepoClientError(Exception):
    """Raised when an operation with the repository fails."""


class RepoClient:
    def __init__(self, repo_path: str | Path) -> None:
        self.repo_path = Path(repo_path)
        if not self.repo_path.exists():
            raise RepoClientError(f"Repository path '{self.repo_path}' does not exist")

    def apply_patch(self, patch_content: str) -> None:
        """Apply a raw patch to the repository.

        This is a very small stub implementation that simply writes the patch
        to a file named ``applied.patch`` inside the repository.  Real
        implementations would invoke `git apply` or similar.
        """
        if not patch_content:
            raise RepoClientError("Empty patch content")
        try:
            (self.repo_path / "applied.patch").write_text(patch_content)
        except OSError as exc:
            raise RepoClientError(f"Failed to apply patch: {exc}") from exc

    def open_pull_request(self, branch: str, title: str, body: str) -> str:
        """Open a pull request and return its URL.

        This implementation is a stub that returns a fake URL. Real
        implementations would interact with the hosting provider API.
        """
        if not branch or not title:
            raise RepoClientError("branch and title are required to open a PR")
        return f"https://example.com/pr/{branch}"

